# The executables

## The resident program: `0`

* 518 172 bytes, the 1st read file, at **0x06010000** (IP.BIN's 1st read
  address; `--find-base` agrees, 1 363 prologue hits against 116 for the
  next base). It stays resident: nothing loads over 0x06010000–0x0608E81C.
* **crt0** (SHC's): `r15 = 0x060FE000`, then 0x06010014 clears two BSS
  ranges and copies two initialised-data ranges (bounds read from
  0x06077BB0–0x06077BC0 and 0x06028888–0x06028898), sets 0x060740B0 to 0
  and calls **`main` at 0x060100B4**, then loops on itself.
* **Layout** (from discovery): game code 0x06010000–0x06028886 (950
  functions in all), then 325 KB that discovery leaves unclassified,
  0x06028886–0x060779A0: the file-name table, the item and spell names
  (`SILVER CANDLESTK`, `OVERLORD'S ROBE`, `LIFESAVER`), tables and
  pictures (inferred); then Sega's libraries from about 0x06077B00 to the
  end.
* **Libraries**: SBL. `GFS_SBL Version 2.10 1996-02-01` with GFS's error
  names (`GFS_ERR_CDRD` …), `PCM Version 1.15 1995-02-21` with its
  messages (`S:ERRPCM`, `SDRVCOPY`, `VBL ERR`). No SGL. BIOS services
  used: `SYS_SETUINT`, `SYS_GETUINT`, `SYS_SETSINT`, `SYS_GETSINT`,
  `SYS_CHGSCUIM`, `BUP_INIT`, and the vector at 0x0600026C (called at
  0x06010BA8 when a few flags agree: inferred to be the soft reset).
* **A soft-reset marker** in low work RAM: `main` checks 0x0027FFF0 for
  `0x31415927` (π) and sets 0x060369A0 to 2 if it is there, 0 otherwise,
  then writes it: a reset skips the logos (inferred).

### `main`: a state machine over overlays

`main` (0x060100B4) masks the SCU's interrupts (`SYS_CHGSCUIM(-1,
0xBFFF)`), initialises (0x060105E8, 0x06011190) and loops over a
**state at 0x060369A0** (16 states, a `braf` table at 0x0601015C). Each
state loads a file to **0x06090000** with 0x060104D0 (directory handle at
0x06042F54, name, destination) and **calls it as a function**; when it
returns, the state moves on:

| State | Loads and calls | Then |
|---|---|---|
| 0 | `WDLOGO.BIN` | 1 |
| 1 | `OPNDEMO.BIN` (the prologue; it reads `OPNDEMO2.BIN`) | 2 |
| 2 | `LOGO.BIN` (the title) | set by the title |
| 3 | — | 4 |
| 4 | the new game's set-up (0x0601EF58) | 5 |
| 5 | `TWN.BIN` (towns, dungeons) or `FLD.BIN` (the world map), by the byte at 0x06036672; or, after a battle, 0x60000 bytes copied from 0x00280000 | set by the overlay |
| 6 | `BATTLE.BIN`, or on the world map 0x6F000 bytes copied from 0x00280000 | (marks the next state 5 as a copy) |
| 7, 15 | `CREDIT.BIN` | 0 |
| 8 | — | 0 |
| 9–12 | `DEMO3.BIN`, `DEMO2.BIN`, `DEMO4.BIN`, `DEMO1.BIN`: **not on the disc** | 1, 1, 0, 5 |
| 13, 14 | `BEVENT1.BIN`, `BEVENT2.BIN` (scenes in battle, by name) | 5 |

The copies (states 5 and 6) use a `memmove` (0x06023594, `r4` dst, `r5`
src, `r6` length). No program copies 0x06090000 out to 0x00280000 (no
reference to 0x06090000 in any overlay), so what is copied in is a file
read there earlier, not a saved overlay: inferred to be a preload, so
that battles on the world map start without the CD (open question 2).

## The overlays at 0x06090000

Every overlay loads at 0x06090000 (`--find-base`: the best base for all of
them but the data files) and its first instruction is an ordinary
function's (`sts.l pr,@-r15` or a push of r8–r14), except `TWN.BIN`'s,
a `bra 0x06091000` over a table. **They return to `main`**: they are
subroutines, not programs that reset the stack. They call into the
resident program freely (graphics, CD, sound, the PCM library).

| File | Size | Functions | Code | Notes |
|---|---|---|---|---|
| `WDLOGO.BIN` | 10 504 | 14 | 6.5 KB | the Working Designs logo (VDP1 polygons) |
| `OPNDEMO.BIN` | 73 160 | 56 | 5.5 KB | the prologue |
| `LOGO.BIN` | 349 688 | 59 | 12 KB | the title, a VDP2 rotation plane in perspective |
| `TWN.BIN` | 206 798 | 551 | 120 KB | towns and dungeons |
| `FLD.BIN` | 389 352 | 106 | 38 KB | the world map |
| `BATTLE.BIN` | 351 432 | 325 | 209 KB | battles |
| `CREDIT.BIN` | 310 556 | 28 | 4.5 KB | the staff roll |
| `BEVENT1.BIN`, `BEVENT2.BIN` | 81 140, 69 408 | 49, 46 | 17, 14 KB | scenes |
| `EVENT1.BIN` | 66 584 | 48 | 15 KB | named by no program; its calls into the resident land on 63 places that are not functions of `0` (nor of `ALG.GIN`): built against another build, dead |
| `BTL_DEB.BIN` | 66 404 | | | named by no program; `--find-base` puts it at 0x00200000 (low work RAM): a battle debugger, by name, dead |

The slave SH-2: `TWN`, `FLD`, `BATTLE` and `EVENT1` hold the literal
0x21000000 (SINIT, the slave's wake-up); the resident program does not.
How the slave is used is for the runtime to show.

## Hardware, by literal pools

`python tools/hwlits.py FILE@BASE`, the literals that point at hardware
(VDP2's registers are written through SBL's shadow, so they barely show):

* `0`: SMPC (32), sound RAM (30), low work RAM (28), VDP2 VRAM (24), VDP1
  registers (17), the CD block (12: HIRQ, HIRQMASK, the data port), VDP2
  registers (TVMD, TVSTAT, CLOFEN), SCU registers, CRAM.
* `TWN`: VDP2 VRAM (94), the SCSP's registers (24), CRAM, VDP1 VRAM, the
  colour offset registers (0x25F80110–0x25F8011E: fades).
* `FLD` and `LOGO`: VDP2 VRAM and `ZMCTL` (0x25F80098, the reduction
  control) besides the colour offsets.
* `BATTLE`: low work RAM (487), CRAM (98), VDP2 VRAM, VDP1 VRAM.

## Function discovery

`python -m saturnkit.recomp.discover FILE --base B --report`, unchanged:

| Program | Functions | Problems | Unresolved indirect | Switch tables |
|---|---|---|---|---|
| `0` | 950 | 0 | 68 | 7 |
| `TWN` | 551 | 0 | 26 | 7 |
| `BATTLE` | 325 | 0 | 33 | 40 |
| `FLD` | 106 | 0 | 1 | 0 |
| `LOGO` | 59 | 0 | 2 | 0 |
| `OPNDEMO` | 56 | 0 | 3 | 1 |
| `BEVENT1`, `BEVENT2`, `EVENT1` | 49, 46, 48 | 0 | 1 each | 1 each |
| `CREDIT` | 28 | 0 | 1 | 1 |
| `WDLOGO` | 14 | 0 | 0 | 0 |

2 232 functions, none with a problem. A trial `python -m saturnkit.recomp`
of all eleven programs as eleven modules (ten at 0x06090000) emits
322 621 instructions in 8.5 s. Its report names the static targets that
are not an entry of their module: the overlays' calls into `0` (expected,
dispatched at run time), and among them a handful that are not entries of
`0` either: **0x0601F158**, called by every overlay, and 0x0607833E,
0x06083556, 0x06086ED6 (from `TWN`, `BATTLE`, `BEVENT*`): entries
discovery has not seen, to give as seeds. `ALG.GIN`, the Japanese build,
gives 907 functions, one with a problem (not followed: it is not run).
Ghidra's cross-check is for session 2.
