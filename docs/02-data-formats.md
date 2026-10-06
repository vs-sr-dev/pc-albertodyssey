# The data formats, at a glance

Session 1 looked at each kind of file's first bytes and at what the
code does with a few of them. What was read is said as such; the rest
is marked as inferred from names and headers.

## Sound

* **CD-DA, tracks 2–22**: the music. Checked in Beetle with
  `tools/cdda_match.py` (a recording's windows against every track,
  correlated on a 2 kHz envelope): the Working Designs logo plays
  **track 16**, the prologue **track 3** from its start, both at a
  correlation of 0.95–1.00, so nothing else plays over them.
* **`*.AIF`**: 672 plain AIFF files (`FORM`…`AIFF`, `COMM`, `INST`,
  `SSND`), mono, 16-bit, 22 050 Hz (five at 44 100 Hz), 55 minutes in
  all. The program carries SBL's PCM library (`PCM Version 1.15
  1995-02-21`), which plays AIFF from memory or a stream. Heard by the
  user, and by name:
  * `IVENTnnn` (354 files, 35 minutes): **the events' sound effects**
    (heard: drills, hens, magic; `IVENT075` is the screech films give the
    bald eagle, a red-tailed hawk's). Not speech, among the files heard
    so far.
  * `AXZnnnn` (39): attacks (heard);
  * `AC*`, `AO*`, `AX*` + `PAIK`, `EKA`, `REOS`, `AMON`, `CARO`, `ERD`:
    each party member's sounds in battle, by name (Pike, Eka, Leos, Amon,
    Carro, Elder; `A_TAM.C` gives five of these names in katakana, all
    but Carro); by the `AXZ` files, `AX` would be their attacks;
  * `MOZ`, `MOF`, `AOZ`, `DAZ`, `VC`, `IT`: monsters, spells, items
    (inferred from names, not yet heard).
* **`MAPnnn.SNF`** (73): a table of 16-byte records (a type word, the
  offset in the file, the size, 0) ending in zeros, then the parts.
  `MAP000.SNF` holds ten parts, of types 0x30, 0x38, 0x31 (5), 0x32 (2),
  0x33, and Sega's 68000 sound driver, `ver1.28 94/12/29 SATURN(S)
  master`. The types look like those of Sega's sound area map (tone
  banks, sequences, DSP); the program walks the driver's area map at
  0x25A00400 (`0x06021C1C`). So each map loads its own driver, banks and
  sequences: the sound effects, and perhaps music that is not on CD
  (open question 3).

## Pictures (inferred from headers, to be decoded)

* `*.VD2` (71) and `*.BGD` (13): start `A0 00 00 08` or `A0 00 00 20`,
  then a size and Saturn RGB555 colours: a palette, then cells for VDP2.
* `*.MGC` (71): the same `A0 00 …` header, then 4-bit pixels: the
  spells' effects.
* `MAPnnn.V1N` (76), `*.MST` (48), `*.CHR` (17), `*.OBJ` (8),
  `CREDIT.SPR`: a word count or kind, a size, then 4-bit pixels (`0777
  7700`, `0067 7888 8877 6000`): VDP1 sprites for the maps, the monsters,
  the menus, the battles, the staff roll.
* `*.PTY` (4): a count and a table of pointers into 0x2022xxxx: the
  party's battle sprites with their animation (the base is not an address
  of the Saturn: offsets to rebase).
* `*.GRP` (242): small (8 KB) records, a word `0x00C0`, `0x0520`:
  enemy groups or their placements.
* `MAPnnn.TWN` (58): a header of words, then data: a town's or a
  dungeon's map (cells, collision, events?).
* `*.BBG`, `*.BGP`, `MAP084.MAP`: pattern-name words (`0C06 0C17 …`):
  VDP2 maps of 16-bit cell names. `*.BGC`: a CRAM palette (RGB555).

No movies: there is no Sega FILM, no Cinepak, no MPEG on the disc. The
prologue and the scenes are drawn by the program (`OPNDEMO.BIN` reads
`OPNDEMO2.BIN`).

## Overlays

`TWN.BIN` starts with `bra 0x06091000` and a table of pointers into
itself; the other overlays start with an ordinary function prologue
(`03-executables.md`).

## Next

Decoders for the pictures belong in saturnkit's layer 2 (VDP1/VDP2
image decoders, 4/8/16 bpp with CLUT and CRAM), which no port has needed
yet; for the port itself they are not on the critical path, since the
game draws them.
