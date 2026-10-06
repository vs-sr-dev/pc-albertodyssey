# pc-albertodyssey

Toward a native PC port of **Albert Odyssey: Legend of Eldean** (Sega
Saturn, 1996 in Japan as *Albert Odyssey Gaiden* by Sunsoft; 1997 in North
America, translated and published by Working Designs), a 2D role-playing
game, the legend of the Eldean clan and its holy sword (the disc's own
abstract): towns, dungeons and a world map seen in perspective, with
turn-based battles, story scenes and music on CD. It came out on the Saturn
only and was never re-released. The goal is the game running natively on
PC: without the CD's waits between towns, maps and battles, its world map
drawn sharp at the window's resolution, and its CD music as it is on the
disc.

This repository documents the disc, its formats and its code, and grows
the tooling for the port. It is the fourth port built on **saturnkit**,
the game-agnostic toolkit for Saturn reverse engineering that grew out
of [pc-virtualhydlide](https://github.com/vs-sr-dev/pc-virtualhydlide).
Albert Odyssey is where saturnkit meets overlays called as functions at
one address, CD-DA music and VDP2's rotation planes. saturnkit is a
submodule here: clone with `--recursive`, or run
`git submodule update --init`.

## BYOA: Bring Your Own Assets

This repository contains **documentation and tools only**. No game data,
no executables, no assets. You need your own original disc. The work is
done on the North American release, T-12705H V1.010 (1997-06-12), one
disc, as a Redump-style .cue with its 22 .bin files in `iso/`.

## Layout

    docs/            disc, format and code analysis, and the plan
    tools/           Albert Odyssey-specific tools: recomp.py, run.py, oracle.py, sheet.py,
                     cdda_match.py, vdp1list.py, hwlits.py
    saturnkit/       game-agnostic Saturn toolkit (submodule)
    iso/, build/     your disc and everything derived from it (ignored by git)

## Tools

The Python tools need only Python 3.8+; `sheet.py` needs PIL and
`cdda_match.py` numpy. Building the recompiled C++ needs CMake, Ninja,
clang and SDL3 (MSYS2's mingw64, found at `C:\msys64\mingw64\bin`). The
oracle needs RetroArch with the Beetle Saturn core and the US/European
BIOS (`mpr-17933.bin`), and ffmpeg for its recordings. Run everything from
the repository root.

```sh
C="iso/Albert Odyssey - Legend of Eldean (USA).cue"

# the disc: IP.BIN, the volume, the 22 tracks; the files; the CD-DA tracks as WAV
python -m saturnkit.disc "$C" --info
python -m saturnkit.disc "$C" --list
python -m saturnkit.disc "$C" --extract build/extract
python -m saturnkit.disc "$C" --audio build/audio

# the code: the resident program, its state machine, an overlay
python -m saturnkit.sh2 build/extract/0 --find-base
python -m saturnkit.sh2 build/extract/0 --base 06010000 --at 060100B4 --count 120    # main
python -m saturnkit.recomp.discover build/extract/0 --base 06010000 --report
python -m saturnkit.recomp.discover build/extract/TWN.BIN --base 06090000 --report
python tools/hwlits.py build/extract/0@06010000 build/extract/FLD.BIN@06090000

# the programs to C++, built with clang (MSYS2) and checked against the interpreter
python tools/recomp.py --build --test

# run it on saturnkit's runtime: headless to the first house, pictures at chosen VBlanks
python tools/run.py -- --shot 2040,3200,4800,6600
python tools/run.py --play                 # a window, the keyboard or a gamepad
python tools/vdp1list.py build/run/dump-6600.bin --near 260,200   # after -- --dump 6600

# the oracle: Beetle Saturn in RetroArch, pressed and photographed from here
python tools/oracle.py --at 40:START,80:START,80.4:START --every 3 --quit 135 --record
python tools/sheet.py build/oracle                                  # the shots on one sheet
python tools/cdda_match.py build/oracle/record.wav                  # which CD-DA track plays when
```

## Status

Session 1: the survey. One disc: a data track and 21 CD-DA tracks of
music. A resident program, `0`, at 0x06010000 (SHC, SBL: GFS 2.10, PCM
1.15) whose `main` is a state machine loading eleven overlays to
0x06090000 and calling them as functions: logos, prologue, title, towns,
world map, battles, scenes, credits. 672 AIFF files hold 55 minutes of
sound effects; each map has its own copy of Sega's sound driver 1.28
and its banks. Discovery finds 2 232 functions in the eleven programs
with no problem. Beetle Saturn driven from the boot through the prologue
and the title (a rotation plane in perspective) to the first house. The
disc also carries the Japanese build of the program, the Japanese
master's disc script and a function of the game's C source
(`docs/04-curiosities.md`).

Session 2: the programs as C++ (2 193 functions in ten modules, the nine
overlays marked as called and returned from; self-test 15 532 of 15 532
vectors) on saturnkit's runtime, from the boot through the Working
Designs logo and the prologue with their CD-DA music, the title, the
burning village and the first house, the same pictures as Beetle's.
saturnkit learned overlays called as functions, the 1st read entered with
interrupts open, VDP2's rotation screen RBG0, line scroll, raster effects
from an HBlank handler, and VDP1 stopping on a command it does not know
(`docs/11-runtime.md`).

## Playing it

The game is playable as far as it has been played: through the whole
introduction to the harpies' forest village. Battles, the world map and
everything after have not been reached yet.

```sh
python tools/run.py --play            # the game in a window
```

Keys (in `saturnkit/runtime/host.cpp`): the arrows, Enter for START,
Z X C for A B C, A S D for X Y Z, Q W for L R; F11 fullscreen, F12 a
picture. A gamepad works too. Each game is recorded to
`build/run/play-DATE-TIME.txt`; `python tools/run.py --input @that-file`
plays it again, headless.

## Documentation

* [00-sessions.md](docs/00-sessions.md): what each session did
* [01-disc-layout.md](docs/01-disc-layout.md): IP.BIN, tracks, the files
* [02-data-formats.md](docs/02-data-formats.md): sound, pictures, overlays at a glance
* [03-executables.md](docs/03-executables.md): the resident program, `main`'s states, the overlays, discovery
* [04-curiosities.md](docs/04-curiosities.md): things found on the way
* [05-open-questions.md](docs/05-open-questions.md): what is not known yet
* [06-attack-plan.md](docs/06-attack-plan.md): feasibility, what saturnkit has and lacks, the phases, what a better Albert Odyssey means
* [07-next-session.md](docs/07-next-session.md): the next session's list
* [09-recompiler.md](docs/09-recompiler.md): the programs as C++, discovery's seeds and fix, the self-test
* [10-saturnkit.md](docs/10-saturnkit.md): what this port gives saturnkit
* [11-runtime.md](docs/11-runtime.md): the game on saturnkit's Saturn, how far it runs, what the runtime learned

## Licence

MIT: see [LICENSE](LICENSE). Albert Odyssey: Legend of Eldean is © 1996
Sun Corporation / Sunsoft, English translation © 1997 Working Designs;
this project contains none of it.
