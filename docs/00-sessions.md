# Sessions

## Session 1 (2026-10-06): the disc, the code, the plan

* **The disc** (`01-disc-layout.md`): the North American release by
  Working Designs, T-12705H V1.010 (1997-06-12), one disc: a Mode 1 data
  track and 21 CD-DA tracks (about 40 minutes of music). 1 404 files, all
  in the root, and 21 `CDDAn` records. saturnkit's `disc` read and
  extracted all of it unchanged.
* **The code** (`03-executables.md`): a resident program, `0`, at
  0x06010000 (SHC's crt0, SBL: GFS 2.10 and PCM 1.15, no SGL). Its `main`
  is a state machine of 16 states that loads an overlay to 0x06090000 and
  **calls it as a function**: `WDLOGO`, `OPNDEMO`, `LOGO`, `TWN`, `FLD`,
  `BATTLE`, `CREDIT`, `BEVENT1`, `BEVENT2`; on the world map and after a
  battle it copies the overlay in from low work RAM instead. Four states
  load `DEMO1`–`DEMO4.BIN`, which are not on the disc; `EVENT1.BIN` and
  `BTL_DEB.BIN` are on it but nothing loads them. Discovery: 2 232
  functions in eleven programs, none with a problem; the recompiler emits
  them all (not yet built).
* **The formats** (`02-data-formats.md`): 672 AIFF files (55 minutes:
  354 event sound effects and the attacks, as the user heard them; the
  party's and the monsters' sounds by name), Sega's sound
  driver 1.28 with each map's banks in `MAPnnn.SNF`, VDP1 sprites and
  VDP2 pictures in a few headed formats. No movies.
* **The oracle** (`tools/oracle.py`, now with `--every` and held
  presses): Beetle Saturn with the US BIOS, from the boot through the
  Working Designs logo (CD-DA track 16), the prologue (track 3, both
  matched to the disc's tracks at correlation 0.95–1.00 by
  `tools/cdda_match.py`), the title, a VDP2 rotation plane in perspective,
  then the burning village and the first house; its recording holds the
  whole sound from the Saturn logo to the title (heard by the user). The
  user found that the
  title wants **two START presses in quick succession**; the oracle
  reproduces it (two presses 0.4 s apart), to the house at 130 s.
* **Curiosities** (`04-curiosities.md`): the Japanese build of the program
  (`ALG.GIN`), the Japanese master's disc script (`ALG.SCR`), and a C
  function of the game's source (`A_TAM.C`: a debug save start, with the
  party's names in katakana).
* **The plan** (`06-attack-plan.md`): static recompilation on saturnkit.
  saturnkit holds for the survey as it is (`10-saturnkit.md`); the run
  will ask it for overlays called as functions, CD-DA playback and VDP2
  rotation planes.
