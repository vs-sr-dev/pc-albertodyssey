# The plan

## What the game is, for a port

A 2D role-playing game of 1996–97 on SBL: towns and dungeons drawn as
VDP2 scroll planes with VDP1 sprites over them (`TWN`), a world map that
is a VDP2 rotation plane seen in perspective (`FLD`; the title already
shows one), turn-based battles (`BATTLE`), story scenes (`BEVENT*`, events in
`TWN`), music on 21 CD-DA tracks, and 55 minutes of sound effects in
AIFF files. A resident
program of 518 KB swaps eleven overlays at one address and calls them
as functions.

## Feasibility: static recompilation, on saturnkit

The same route as the three ports before it: every program to C++
through saturnkit's recompiler, run on saturnkit's runtime. What speaks
for it:

* **SHC and SBL**, the compiler and library family saturnkit was built on
  (Virtual Hydlide, X JAPAN). Discovery finds 2 232 functions in the
  eleven programs with **no problem**, and the recompiler emits all of
  them as they are (`03-executables.md`).
* **No movies, no SGL, no SCU DSP** (none found so far).
* The sound driver is Sega's 68000 driver (1.28 here, 1.27 in X JAPAN),
  which saturnkit's 68000 and SCSP already run.

What saturnkit has, and what this game asks of it:

| Need | saturnkit now | To do |
|---|---|---|
| A resident program that **calls overlays at a shared base and gets them back** | a call to a module's base is a program start: the runtime unwinds the host stack (`ProgramStart`), as Virtual Hydlide's programs need | a call to an overlay's base that identifies and activates the module, then returns to the caller (by a mark on the module in the recompiler's spec, or by telling a start from a call); the previous overlay deactivated |
| The overlay copied in from low work RAM (states 5 and 6) | modules are found by the crc32 of their image at their base, when they are started | check at run time that the copy is the file as read (open question 2); if not, identify by the code's range only |
| **CD-DA**: the WD logo plays track 16, the prologue track 3 (checked in Beetle) | the CD block reads data; CD-DA reaches the SCSP's external input, but no game has played a track | the CD block's Play over audio tracks (FAD ranges, repeat, the status and the pickup's place), the samples into the SCSP's EXTS at 44.1 kHz, the volume through the SCSP's EFREG/EXTS levels |
| **VDP2 rotation planes**: the title's world, and the world map (inferred) | NBG0–3, the sprite layer, windows; "rotation planes not done" | RBG0 (and RBG1 if used): the rotation parameter tables, the coefficient tables (per-line or per-dot perspective), screen-over, with the priorities and colour calculation already there |
| AIFF effects through SBL's PCM library 1.15 | Virtual Hydlide's movie sound used SBL's PCM path | the effects loaded or streamed while a scene or a battle runs, mixed with the CD-DA; to be heard against Beetle |
| The slave SH-2 in `TWN`, `FLD`, `BATTLE` | the slave as a deterministic coroutine | what jobs it gets (the runtime's trace will tell) |
| Saves (`BUP_INIT`, internal RAM or a cartridge) | BUP services in a host file | check the save and load screens |
| Discovery's seeds | `--seeds` | 0x0601F158, 0x0607833E, 0x06083556, 0x06086ED6, and what the runtime stops on |
| `ZMCTL`, colour offsets, VDP1 polygons (the WD logo) | the colour offsets and VDP1 are done; reduction (`ZMCTL`) is part of NBG zoom | check |

## What a better Albert Odyssey on PC means

* **No waiting.** Every town, map and battle is a CD load at double speed
  (states 5 and 6 above load or copy a whole overlay, then its maps and
  banks). From files on a PC drive these can be immediate; the runtime can
  serve the CD block without the drive's delays once the game is known to
  run right at real speed.
* **A sharp world map.** The rotation plane is computed per pixel from
  the game's own parameters; drawn at the window's resolution instead of
  320×224 it keeps its perspective without the blocky texels of the
  horizon. This is honest: the game gives the transform, the port samples
  it finer. The 2D towns and battles stay pixel art, scaled cleanly
  (integer, or smooth at the user's choice).
* **The CD-DA as it is**, straight from the disc's tracks at 44.1 kHz,
  with no drive noise or seek gaps between loops.
* **The frame rate**: to be measured. If the world map or battles run at
  30 fps on the Saturn, `--interp`-style in-between fields may apply to
  the rotation plane (its parameters interpolate well); the user decides.
* Later, if wanted: widescreen for the world map (the plane extends
  naturally; the sprites and the HUD would need placing).

## Phases

1. **The survey** (session 1, done): the disc, the formats, the programs
   and `main`'s states, discovery, the oracle to the first house.
2. **The recompiler**: discovery's seeds and Ghidra's cross-check, all
   eleven programs as modules, the self-test against the interpreter
   (`tools/recomp.py`); saturnkit's overlay calls.
3. **The first run**: the boot, the WD logo with CD-DA track 16, the
   prologue with track 3, the title (the first rotation plane), START
   twice, the burning village, the first house (`tools/run.py`, headless,
   pictures against Beetle's). saturnkit: CD-DA, RBG0.
4. **The game**: walking in town, the menus, the first battle, the world
   map, the scenes with their sound effects, saving and loading, the dungeons,
   to the end; against Beetle and played by the user.
5. **The PC gains**: no waiting, the world map at the window's resolution,
   the scaling, the frame rate.
6. **The release**: a build and a README for players (BYOA).
