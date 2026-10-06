# Next session: into the game

Where things stand: the ten programs are C++ and self-tested
(`09-recompiler.md`); on saturnkit's runtime the game boots, plays the
logo and the prologue with their CD-DA music, shows the title as Beetle
does (RBG0, line scroll, the raster haze), starts a new game and reaches
the burning village and the first house (`11-runtime.md`).
`python tools/recomp.py --build --test`, then `python tools/run.py`
(headless, to the house), `--play` for the window.

## Done in session 2 already: the user played to the harpies' village

Recorded as `tools/scripts/to-the-harpies-village.txt`; the
characters-over-scenery bug it showed is fixed (special priority).
Next by play: the first battle, the world map.

## First: what the user sees and hears in the window

`python tools/run.py --play`: the user plays from the title into the
village and the house and reports: the pictures, the music (CD-DA) and the
effects (the AIFF files, the sound driver), the text, anything wrong
against Beetle. Each game is recorded to `build/run/play-*.txt` and can be
given back headless with `--input @FILE`.

## Then

1. The first dialogue: text boxes and the font (`MENUDATA.CHR`?), the
   menus, the shops.
2. Leaving the town: `FLD`, the world map. Open question 1 (rotation:
   RBG0 or RBG1, coefficient mode); the WD logo already asks for RBG1.
3. The first battle: `BATTLE` (and the copies from low work RAM, open
   question 2: does the crc32 still find the overlay?).
4. The AIFF effects: when they play, through what, mixed with the CD-DA
   (open question 4).
5. Saving and loading: `ALBERT_G_00` in the runtime's BUP file, and the
   load screen.
6. The notes the runtime still prints: RBG1 in the WD logo, CCCTL 0x0403
   in the prologue, SFPRMD/SFCCMD in the town.

## Keep in mind

* The title takes START only twice in quick succession (3600 and 3624 in
  the script; the user's finding).
* `SATURNKIT_VDP2_HIDE=MASK` to tell layers apart; `tools/vdp1list.py` on
  a `--dump` for VDP1's list.
* Bash heredocs feeding `python -` (and `python -c "..."` inside double
  quotes) mangle backslashes: `\n`, `\b`. Use files.
* Every saturnkit change: Virtual Hydlide, Deep Fear and X JAPAN
  (self-tests, headless runs byte-identical or the difference explained),
  then bump all three.
