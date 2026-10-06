"""Recompile Albert Odyssey's programs to C++ and check them.

    python tools/recomp.py [--build] [--test] [--no-vectors]

1. `python -m saturnkit.recomp`: the resident program `0` as module MAIN
   and the nine overlays `main` loads at 0x06090000 as one module each,
   and saturnkit's instruction test, into build/recomp; report.txt there
   has the counts. `EVENT1.BIN` and `BTL_DEB.BIN` are left out: nothing
   loads them (docs/03-executables.md).
2. `python -m saturnkit.recomp.selftest`: the vectors of every function of
   each module that runs alone (on its stack, or on what its pointer
   arguments point at), with MAIN loaded beside each overlay, into
   build/recomp/selftest.
3. --build: CMake, Ninja and clang from MSYS2 into build/recomp-build.
4. --test: the self-test executable on every vectors file.

Run from the repository root, after the disc has been extracted
(build/extract).
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
EXTRACT = os.path.join(ROOT, "build", "extract")
OUT = os.path.join(ROOT, "build", "recomp")
BUILD = os.path.join(ROOT, "build", "recomp-build")
MSYS = r"C:\msys64\mingw64\bin"

MAIN_BASE = 0x06010000
OVERLAY_BASE = 0x06090000
# entries discovery does not reach from 0's own code: the overlays call them
# (0x0601F158 is the shared tail of 0x0601F142; the others are leaves after an rts)
MAIN_SEEDS = [0x0601F158, 0x0607833E, 0x06083556, 0x06086ED6]
OVERLAYS = ["WDLOGO", "OPNDEMO", "LOGO", "TWN", "FLD", "BATTLE", "CREDIT", "BEVENT1", "BEVENT2"]


def specs():
    yield "MAIN=%s@%08X+%s" % (os.path.join(EXTRACT, "0"), MAIN_BASE, ",".join("%08X" % s for s in MAIN_SEEDS))
    for name in OVERLAYS:
        yield "%s=%s@%08X" % (name, os.path.join(EXTRACT, name + ".BIN"), OVERLAY_BASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--no-vectors", action="store_true")
    a = ap.parse_args()
    from saturnkit.recomp.__main__ import generate, parse_spec
    from saturnkit.recomp import selftest
    t0 = time.time()
    all_specs = list(specs())
    generate([parse_spec(s) for s in all_specs], OUT, optest=True, overlays=OVERLAYS)
    if not a.no_vectors:
        os.makedirs(os.path.join(OUT, "selftest"), exist_ok=True)
        for s in all_specs:
            name = s.split("=", 1)[0]
            images = [all_specs[0]] if name == "MAIN" else [all_specs[0], s]
            argv = ["--out", os.path.join(OUT, "selftest", name.lower() + ".txt"), "--test", name, "--auto"]
            for img in images:
                argv += ["--image", img]
            selftest.main(argv)
    print("generated in %.0f s" % (time.time() - t0))
    env = dict(os.environ, PATH=MSYS + os.pathsep + os.environ["PATH"])
    tool = lambda x: shutil.which(x, path=env["PATH"])      # CreateProcess searches the parent's PATH
    if a.build:
        t = time.time()
        subprocess.run([tool("cmake"), "-S", OUT, "-B", BUILD, "-G", "Ninja", "-DCMAKE_CXX_COMPILER=clang++",
                        "-DCMAKE_C_COMPILER=clang"], env=env, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([tool("ninja"), "-C", BUILD], env=env, check=True)
        print("built in %.0f s" % (time.time() - t))
    if a.test:
        names = ["optest"] + [s.split("=", 1)[0].lower() for s in all_specs]
        files = [os.path.join(OUT, "selftest", n + ".txt") for n in names]
        r = subprocess.run([os.path.join(BUILD, "selftest.exe")] + [f for f in files if os.path.exists(f)], env=env)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
