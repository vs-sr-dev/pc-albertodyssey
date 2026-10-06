# Next session: the recompiler and the overlays

Where things stand: the disc, the programs and `main`'s state machine
are mapped (`01`–`03`); discovery holds on all eleven programs; Beetle
is driven from here to the first house. Nothing is built yet.

## 1. The programs as C++

* `tools/recomp.py` in X JAPAN's shape, with eleven modules: `MAIN`
  (`0`@0x06010000) and the ten overlays @0x06090000 (`EVENT1` and
  `BTL_DEB` can be left out: nothing loads them).
* Seeds for discovery: 0x0601F158 (called by every overlay), 0x0607833E,
  0x06083556, 0x06086ED6. Then Ghidra 12's function list
  (`saturnkit/ghidra/ExportFuncs.java`) against discovery for `0`, `TWN`
  and `BATTLE`.
* The self-test (`recomp.selftest --auto`) on each module; 0 differences.

## 2. Overlays called as functions (saturnkit)

The runtime's `sh2_call` sends any call to a module base to
`sh2_program_start`, which throws. Design the generic form first, then
check it on the three other ports:

* which modules are "called" rather than "started": a mark in the
  recompiler's spec (`NAME=FILE@BASE` plus a flag), or a rule (a `jsr`
  to a base whose module does not reset `r15` in its first instructions);
* the call identifies the image at the base (crc32), activates it
  (replacing the overlay before), then runs it on the same host stack and
  returns;
* what happens when the image matches no module: a clear message naming
  the base and the crc, so a new overlay is easy to add.

## 3. The first run

`tools/run.py` in X JAPAN's shape, headless, pictures at chosen VBlanks:

* the boot, `WDLOGO` (VDP1 polygons), its CD-DA track 16;
* `OPNDEMO` and track 3: here saturnkit's CD block needs **Play over audio
  tracks**, with the samples into the SCSP;
* `LOGO`: the first **rotation plane**; RBG0 in saturnkit's VDP2;
* START twice quickly at the title (in Beetle, `tools/oracle.py --at
  40:START,80:START,80.4:START` reaches the village at 88 s and the
  house at 130 s); the burning village, the first house.

The oracle's pictures to compare with are in `build/oracle/twostart/`
(t92–t120 the village, t130 the house) and `build/oracle/start/` (t48,
t87 the title).

## Keep in mind

* `--peek ADDR:N` takes N in decimal; `--dump N` ends with VDP2's
  registers.
* Bash heredocs feeding `python -` mangle `\n` inside strings and
  non-ASCII: use files.
* Every saturnkit change: Virtual Hydlide (`tools/recomp.py --build
  --test`, `tools/run.py` to the field), Deep Fear and X JAPAN (their
  self-tests and headless runs byte-identical), then bump all three.
