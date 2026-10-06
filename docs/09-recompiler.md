# The programs as C++

`python tools/recomp.py [--build] [--test]` turns the resident program
and the overlays into C++ through saturnkit's recompiler, builds them
with clang from MSYS2 and checks them against saturnkit's interpreter.

## The modules

| Module | File | Base | Functions | Instructions |
|---|---|---|---|---|
| MAIN | `0` | 0x06010000 | 958 | 93 854 |
| WDLOGO | `WDLOGO.BIN` | 0x06090000 | 14 | 3 597 |
| OPNDEMO | `OPNDEMO.BIN` | 0x06090000 | 56 | 3 845 |
| LOGO | `LOGO.BIN` | 0x06090000 | 59 | 6 064 |
| TWN | `TWN.BIN` | 0x06090000 | 552 | 61 188 |
| FLD | `FLD.BIN` | 0x06090000 | 106 | 18 875 |
| BATTLE | `BATTLE.BIN` | 0x06090000 | 325 | 106 784 |
| CREDIT | `CREDIT.BIN` | 0x06090000 | 28 | 2 597 |
| BEVENT1, BEVENT2 | `BEVENT1.BIN`, `BEVENT2.BIN` | 0x06090000 | 49, 46 | 9 493, 8 351 |

2 193 functions of the game and 316 778 instructions with saturnkit's
instruction test (775 functions), in 58 files; generated in about 10 s,
built in about 30 s. `EVENT1.BIN` and `BTL_DEB.BIN` are left out:
nothing loads them (`03-executables.md`).

The nine overlays are marked `--overlay`: `main` calls each at
0x06090000 as a function and gets it back, which saturnkit learned this
session (`10-saturnkit.md`). The runtime recognises which one is there by
the crc32 of its image when it is called.

## Discovery

Four seeds for MAIN, entries that the overlays call and nothing in `0`
reaches: 0x0601F158 (the shared tail of 0x0601F142, which every overlay
calls as a function of its own), 0x0607833E, 0x06083556 and 0x06086ED6
(leaves after an `rts`).

The first run stopped on a call to 0x060238AE: SHC's structure copy
(0x0602385C/0x06023868) jumps through a table at 0x060238BC into an
unrolled run of `mov.l` pairs, entry by the number of words left.
Discovery had taken the table's longer entries and left out the last
four (0x060238AE, B2, B6, B8: 7, 5, 3 and 2 instructions), since a
pointer taken only for its table had to descend at least 8 instructions.
saturnkit now takes such a pointer at any length when its descent lies
wholly in code already found (c5e70c9). MAIN gained exactly those four
entries, TWN one; no other program changed.

## The self-test

`recomp.selftest --auto` on each module, MAIN loaded beside each overlay
(they call into it): the functions that run alone on their stack or on
what their pointer arguments point at.

| Module | Functions | Vectors |
|---|---|---|
| saturnkit's instruction test | 775 | 9 300 |
| MAIN | 181 | 2 880 |
| TWN | 107 | 1 712 |
| BATTLE | 39 | 603 |
| FLD | 28 | 448 |
| LOGO | 14 | 224 |
| BEVENT1, BEVENT2 | 8, 8 | 128, 125 |
| OPNDEMO, CREDIT, WDLOGO | 3, 3, 1 | 48, 48, 16 |

**15 532 vectors, 0 failures.**
