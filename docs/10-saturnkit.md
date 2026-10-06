# What this port gave saturnkit

saturnkit (`saturnkit/`, a submodule from
https://github.com/vs-sr-dev/saturnkit) was started by Virtual Hydlide's
port and grew through Deep Fear's and X JAPAN's. Albert Odyssey is its
fourth game: SHC and SBL like the first and the third, but with overlays
called as functions at one address, music on CD-DA and VDP2 rotation
planes. Each entry is a saturnkit commit and what this game asked of it.

| Session | saturnkit | What |
|---|---|---|
| 1 | 8d877e0 (unchanged) | the port starts at saturnkit's current head |

## Session 1: what held as it was

Nothing in saturnkit had to change for the survey:

* `disc --info`, `--list`, `--extract`, `--audio`: one MODE1 track and 21
  audio tracks with pregaps of 150 and 152 sectors; 1 404 files and IP.BIN
  extracted, the 21 `CDDAn` records listed and left out, 21 WAV files.
* `sh2 --find-base`: the resident program at 0x06010000, every overlay at
  0x06090000; `--refs`, the disassembly and `hw`'s names as they are.
* `recomp.discover`: 2 232 functions in eleven programs, none with a
  problem.
* `recomp`: the eleven programs as eleven modules (ten at one base) emit
  322 621 instructions; not yet built.

## What this game will ask next

In the order the first run will meet them (`06-attack-plan.md`):

1. **Overlays called and returned from.** The runtime takes any call to a
   module's base as a program start and unwinds the host stack. Here
   `main` calls `jsr 0x06090000` in each of its states and expects each
   overlay to return. saturnkit needs a way to call into a module at its
   base as an ordinary function, identifying and activating it first.
2. **CD-DA.** The CD block's Play over audio tracks, their samples into
   the SCSP's external input. No game has used it until now.
3. **VDP2 rotation planes** (RBG0, the coefficient tables, perspective).
4. Possibly: AIFF sound effects through SBL's PCM library, mixed with the
   CD-DA.

Each change will be checked on Virtual Hydlide, Deep Fear and X JAPAN
before it goes in.
