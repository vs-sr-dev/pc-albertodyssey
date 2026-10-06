# What this port gave saturnkit

saturnkit (`saturnkit/`, a submodule from
https://github.com/vs-sr-dev/saturnkit) was started by Virtual Hydlide's
port and grew through Deep Fear's and X JAPAN's. Albert Odyssey is its
fourth game: SHC and SBL like the first and the third, but with overlays
called as functions at one address, music on CD-DA, VDP2 rotation and
raster effects. Each entry is a saturnkit commit and what this game asked
of it.

| Session | saturnkit | What |
|---|---|---|
| 1 | 8d877e0 (unchanged) | the port starts at saturnkit's current head |
| 2 | c5e70c9 | `recomp.discover`: a pointer whose descent lies wholly in code already found is an entry at any length (the short tail entries of SHC's unrolled structure copy) |
| 2 | 67c6e38 | `recomp --overlay NAME,...` (SH2Module.flags): a call to an overlay's base identifies, activates and calls it, and it returns; the runtime enters the 1st read with the CPU's interrupt mask at 0, as the IP.BIN's initial program leaves it |
| 2 | 66e1e66 | runtime: VDP1 stops at a command of kind 0xC–0xF, with no end status (Mednafen's behaviour) |
| 2 | e2ef3f4 | runtime: VDP2's RBG0 (parameters A and B, coefficient tables, bitmap or cells, screen-over); NBG0/NBG1 line scroll; raster effects (every line's HBlank taken while unmasked, VDP2 writes from the HBlank handler composed line by line); `SATURNKIT_VDP2_HIDE` |
| 2 | c6057ea | README brought up to them |
| 2 | c70abfc | runtime: VDP2's special priority and special colour calculation (SFPRMD, SFCCMD: per character, per dot by the special function codes, by the colour's MSB); the towns' table tops and tree crowns over the characters |
| 2 | 64acac3 | README |

## Session 1: what held as it was

Nothing in saturnkit had to change for the survey:

* `disc --info`, `--list`, `--extract`, `--audio`: one MODE1 track and 21
  audio tracks with pregaps of 150 and 152 sectors; 1 404 files and IP.BIN
  extracted, the 21 `CDDAn` records listed and left out, 21 WAV files.
* `sh2 --find-base`: the resident program at 0x06010000, every overlay at
  0x06090000; `--refs`, the disassembly and `hw`'s names as they are.
* `recomp.discover`: 2 232 functions in eleven programs, none with a
  problem.

## Session 2: the checks on the other ports

Each change was applied to the three other ports' submodules, which were
regenerated, rebuilt, self-tested and run headless against a run made
just before with the previous saturnkit (pictures at three or four
VBlanks and the whole run's sound compared byte for byte):

* **c5e70c9 and 67c6e38**: Virtual Hydlide (51 542 vectors), Deep Fear
  (16 527) and X JAPAN (11 632) pass their self-tests; all three runs
  byte-identical in pictures and sound, with the same frame and
  program-start counts.
* **66e1e66 and e2ef3f4**: Virtual Hydlide and X JAPAN byte-identical.
  Deep Fear unmasks HBlank-IN, so it now takes every line's HBlank
  (752 929 in 3 000 VBlanks against 465 157); the virtual time its
  handler spends moves its frames slightly (964 VDP1 frames in 3 000
  VBlanks against 972, its "presents" title a few frames on at VBlank
  2000, its sound shifted with it). Its first room at VBlank 2900 is
  pixel-identical.

* **c70abfc**: all three byte-identical (none of them sets SFPRMD or
  SFCCMD).

All three ports moved to 67c6e38, then to c6057ea, then to 64acac3, with a commit each
("saturnkit at …: … (from Albert Odyssey)").

## What this game will ask next

* RBG1 (the Working Designs logo enables it for a moment) and perhaps
  rotation parameters chosen by window, if the world map uses them.
* The AIFF effects through SBL's PCM library, mixed with the CD-DA.
* Whatever the world map, the battles and the menus need.
