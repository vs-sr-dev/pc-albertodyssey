# Open questions

1. **The world map**: is `FLD` drawn as a VDP2 rotation plane like the
   title (inferred from the title, from `ZMCTL` in `FLD`'s literals and
   from the size of `SCLMAP.BIN`), with RBG0 alone or RBG0 and RBG1, and
   with which coefficient mode? What `FLD_POLY.BIN` (polygons?) adds.
2. **The copies from low work RAM** (`main`'s states 5 and 6): what is at
   0x00280000 when state 6 copies 0x6F000 bytes on the world map, and when
   state 5 copies 0x60000 after a battle? Inferred: `BATTLE.BIN` and
   `FLD.BIN` read there ahead of time. If the copy is not byte for byte
   the file, saturnkit's crc32 will not recognise the module.
3. **Where the music comes from**: the CD-DA tracks for the logo and the
   prologue (checked); for the towns, the world map, the battles? Do the
   `.SNF` sequences play music too, or only effects?
4. **The voices**: when the `IVENT` lines play (every scene, or some), how
   they are read (whole into memory or streamed from the CD while the
   scene runs), and whether the PCM library or the sound driver plays
   them. The user's ears against Beetle.
5. **The frame pacing**: what the town, the world map and the battles
   step per frame, and their rate on the Saturn (a VBlank counter, a
   limiter).
6. **The slave SH-2**: which jobs `TWN`, `FLD` and `BATTLE` hand it.
7. **The title's input**: START is taken only twice in quick succession
   (the user's finding in Beetle; one press, or presses 6 s apart, are
   not; two presses 0.4 s apart at 80 s, from `tools/oracle.py`, reach the
   burning village at 88 s and the first house at 130 s). Is that a "press START" then a menu with a default choice, with
   the second press confirming it? What the menu offers (new game,
   continue).
8. **The soft reset**: is BIOS 0x0600026C (called at 0x06010BA8) the
   reset to the logos, and is the π marker at 0x0027FFF0 what makes a
   reset skip them?
9. **`DEMO1.BIN`–`DEMO4.BIN`**: `main` can load them (states 9–12) but
   they are not on the disc. Can any path reach those states (an attract
   mode, a timeout on the title)? If one does, what happens on a missing
   file (GFS returns an error and the jump goes into whatever is at
   0x06090000).
10. **`EVENT1.BIN`, `BTL_DEB.BIN`**: confirmed dead by the runtime (never
    loaded), or loaded by a GFS file ID rather than by name?
