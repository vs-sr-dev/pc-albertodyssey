# The game on saturnkit's Saturn

`python tools/run.py` boots the disc into the recompiled programs on
saturnkit's runtime, headless, with a pad script; `--play` opens the
window. The run is deterministic: virtual time, so the same script reaches
the same place every time.

## How far it runs (session 2)

From the boot to the first house, with the default script (START in the
prologue at VBlank 1600, START twice on the title at 3600 and 3624):

| VBlank | Time | What |
|---|---|---|
| 140 | 2.3 s | `main` calls overlay 1, `WDLOGO` |
| 194 | 3.2 s | CD-DA track 16 (the logo's music) |
| ~700 | | the Working Designs logo |
| 990 | 16.5 s | overlay 2, `OPNDEMO`; CD-DA track 3 at 17.8 s: the prologue |
| 1600 | | START: the prologue ends |
| 1747 | 29.1 s | overlay 3, `LOGO`, the title; CD-DA track 5 |
| 2040 | | the world in perspective, then the logo out of white |
| 3600, 3624 | | START twice |
| 3655 | 60.9 s | the game writes its first save, `ALBERT_G_00` (796 bytes) |
| 3742 | 62.4 s | overlay 4, `TWN`; CD-DA track 4 in a loop (repeat 15) |
| ~4100–6000 | | the burning village: the ogre, the fallen man, the smoke |
| ~6200 | | the first house, two people at the table |

Against Beetle (`tools/oracle.py`, same route, `build/oracle/start`,
`build/oracle/intro`, `build/oracle/twostart`): the same sequence of
screens. The title's perspective frame (VBlank 2040) has the colours of
Beetle's at 46.5 s down the picture, pixel rows compared at the top
(169,189,205 / 172,193,210), the middle (0,105,73) and the bottom
(9,89,0); the house is the same picture. The sound: `tools/cdda_match.py`
on the run's WAV finds track 16 from 3.4 s and track 3 from 17.8 s at
correlations of 0.91–0.99.

## What the runtime had to learn

Each a saturnkit commit, checked on the other three ports
(`10-saturnkit.md`):

1. **Overlays called and returned from** (67c6e38). `main` calls each
   overlay with `jsr 0x06090000`; before, any call to a module's base was
   a program start that unwinds the host stack.
2. **The 1st read entered with the CPU's interrupts open** (67c6e38). The
   first run waited forever in `main`'s set-up: SBL's frame wait
   (0x060806CC) waits for the VBlank-IN handler to clear a flag, and the
   runtime started the program with SR's mask at 15. On the Saturn the
   IP.BIN's initial program (run by the BIOS; the runtime does not run it)
   installs VBlank handlers, waits on a counter its VBlank-IN handler
   (level 15) counts, masks VBlank at the SCU again and calls the 1st read
   with `jsr 0x06010000`, SR untouched: the mask is below 15 there. This
   program never writes SR before that wait.
3. **Discovery: the short entries of SHC's unrolled copy** (c5e70c9).
4. **VDP2's rotation screen RBG0**: the title's clouds are RBG0, a 256-
   colour bitmap with a coefficient table (one word a coefficient, a
   coefficient a line) and colour calculation at half. Rotation
   parameters A and B, coefficients per line or per dot from VRAM or colour
   RAM, cells or bitmap, screen-over.
5. **NBG0/NBG1 line scroll**: the title's ground is NBG0 with an X scroll,
   a Y scroll and an X zoom for every line, which is what puts it in
   perspective.
6. **Raster effects**: the title's HBlank-IN handler (`LOGO`
   0x06092940, installed with `SYS_SETUINT(0x42)`) writes VDP2's colour
   offset B on every line from a table (0xFF at the top down to 0 by line
   58): the haze at the horizon. The runtime now takes every line's
   HBlank while the SCU lets it through, records the VDP2 register writes
   made in that handler with their line, and composes each line with the
   registers it had.
7. **VDP1: a command it does not know ends the draw**. The towns' list
   runs into stale slots (CMDCTRL 0x060F, a stack address written there)
   before a 24×48 sprite whose data are not its own; on the Saturn (and in
   Mednafen) a command of kind 0xC–0xF stops the drawing there, so the
   sprite never shows. The runtime drew past it: a block of noise at the
   bottom right of every town screen.

## Still noted by the runtime

* `VDP2: RBG1, or rotation parameters chosen by window` (BGON 0x0030) in
  the Working Designs logo, at 12.7 s: RBG1 is not done. The logo looks as
  in Beetle in the frames looked at; to compare frame by frame.
* `VDP2: extended colour calculation or gradation (CCCTL 0x0403)` in the
  prologue: the picture matches Beetle's frames looked at so far.
* `VDP2: special priority, line colour or special colour calculation` in
  the town: SFPRMD or SFCCMD is set; nothing seen wrong yet.

## Tools for looking

* `tools/sheet.py DIR`: the shots of a run (or the oracle's) on one sheet.
* `tools/vdp1list.py DUMP [--near X,Y] [--path]`: VDP1's command list in
  a `--dump`, walked as VDP1 does.
* `SATURNKIT_VDP2_HIDE=MASK` (an environment variable of saturnkit's
  runtime): leaves out layers when composing (1 sprite, 2 RBG0, 4–32
  NBG0–NBG3), to tell which layer draws what.
