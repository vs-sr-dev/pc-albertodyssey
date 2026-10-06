# The disc

North American release (Working Designs), one disc, as a Redump .cue
with 22 .bin files in `iso/`. Everything here is from
`python -m saturnkit.disc … --info`, `--list` and `--extract`, with the
files read where it says so.

## IP.BIN

| Field | Value |
|---|---|
| Maker | `SEGA TP T-127` (a third party: Working Designs' licensee code) |
| Product | T-12705H |
| Version | V1.010 |
| Date | 1997-06-12 |
| Device | `CD-1/1` |
| Areas | U (North America only); the area block at 0x0E04 reads `For USA` |
| Peripherals | J (control pad) |
| Title | `ALBERT ODYSSEY` |
| IP size | 0x1800 |
| Stacks | master 0, slave 0 (the defaults) |
| 1st read | 0x06010000, the whole file: `/0` |

The ISO 9660 volume is `ALBERT_ODYSSEY_GAIDEN`, 274 394 sectors,
created 1997-07-01 16:52:32, publisher and preparer `WORKING DESIGNS`.
The volume name is the Japanese title's (*Albert Odyssey Gaiden: Legend
of Eldean*, Sunsoft, 1996). `ALB_CPY.TXT` says `Copyright(C) SUNSOFT /
SUN CORPORATION 1996`, `English Translation Copyright (C) 1997 Working
Designs, Inc.`; `ALB_ABS.TXT` is the prologue's story in English;
`ALB_BIB.TXT` lists the series (*Albert Odyssey*, *Albert Odyssey 2*,
*Albert Odyssey Gaiden*, and this one).

## Tracks

| Track | Mode | LBA | Length | |
|---|---|---|---|---|
| 1 | MODE1/2352 | 0 | 107 888 sectors (23:58) | IP.BIN, the file system, every file |
| 2–22 | AUDIO | 108 038 – 267 376 | 21 tracks, 11 s to 3:49 each, about 40 minutes together | the music (CD-DA) |

The pregaps are 150 sectors, or 152 for tracks 3, 4, 6, 10, 11, 13 and 15.
The files end at LBA 107 738 (`IVENT488.AIF`), inside track 1. Each audio
track has a record in the root directory, `CDDA2` to `CDDA22`, pointing at
it; `--extract` lists them and leaves them out.

## Files

1 404 files and 21 CD-DA records, all in the root directory. The roles
below come from the names, the headers and the code where it says so;
`02-data-formats.md` and `03-executables.md` have what was read.

| Kind | Count | Size | |
|---|---|---|---|
| `0` | 1 | 518 172 | the program, the 1st read file, resident at 0x06010000 (`03-executables.md`) |
| `*.BIN` | 27 | 3.5 MB | eleven overlays run at 0x06090000 (`WDLOGO`, `OPNDEMO`, `LOGO`, `TWN`, `FLD`, `BATTLE`, `CREDIT`, `BEVENT1`, `BEVENT2`, and `EVENT1`, `BTL_DEB` which nothing names), and data (`OPNDEMO2`, `SUNBG`, `LOGOBG`, `SCLMAP`, `ALG_TBL`, `MAPATARI`, `OBJFIELD`, `FLD_POLY`, `FIGHTNUM`, `HERO`, `BG2_*`, `MOYA1`, …) |
| `ALG.GIN` | 1 | 487 048 | another build of the program: the Japanese one (`04-curiosities.md`) |
| `*.AIF` | 672 | 147 MB | AIFF sound, 16-bit mono, 22 050 Hz (5 at 44 100 Hz), 55 minutes in all: 354 `IVENT*` (35 minutes, the events' sound effects, heard), the attacks (`AXZ*`, heard), the party's and the monsters' sounds (by name) |
| `MAPnnn.SNF` | 73 | 22 MB | a map's sound: Sega's sound driver 1.28 and its banks, in a table of parts |
| `MAPnnn.TWN` | 58 | 17 MB | a town's or a dungeon's map (by name) |
| `MAPnnn.V1N` | 76 | 13 MB | a map's VDP1 sprites, 4-bit (by the first bytes) |
| `*.VD2` | 71 | 5.1 MB | VDP2 pictures with their palette (by name and header) |
| `*.GRP` | 242 | 3.9 MB | enemy groups (`ENEMY000.GRP` …) |
| `*.MGC` | 71 | 1.1 MB | the spells' effects (`ACD_BRTH`, `AIRARROW`, …) |
| `*.MST` | 48 | 0.8 MB | the monsters' pictures (`AINE`, `AMAZONES`, …) |
| `*.CHR` | 17 | 1.4 MB | menus and shops (`MENUDATA`, `SHOPDAT*`) and their error screens |
| `*.OBJ`, `*.PTY`, `*.BGD`, `*.BBG` | 30 | 2.7 MB | the battles' graphics: party, backgrounds |
| `MAP084.*`, `ASAHI.*` | 6 | 25 KB | one map in an older set of formats (`.MAP`, `.HIT`, `.BGC`, `.BGP`, `.CGP`) |
| `CREDIT.SPR` | 1 | 106 072 | the staff roll's sprites |
| `ALG.SCR`, `A_TAM.C`, `TMP.LST`, `CHKLIST.MS`, `IVENT327.IF` | 5 | | left from the making of the disc (`04-curiosities.md`) |
| `*.TXT` | 6 | 4.6 KB | the volume's copyright, abstract and bibliography files, twice (`ALB_*.TXT` and `COPYRIGH`, `ABSTRACT`, `BIBLIOGR.TXT`, identical) |

There are no movies (no Sega FILM, no Cinepak). The music is the 21 CD-DA
tracks; the sound effects and the music that is not on CD come from the
sound driver in the `.SNF` files (to be confirmed by listening: open
question 3).
