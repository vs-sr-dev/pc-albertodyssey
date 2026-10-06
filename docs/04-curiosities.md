# Curiosities

Things found on the way that the port does not need.

## The Japanese program is still on the disc

`ALG.GIN` (487 048 bytes) begins with the same crt0 as `0`
(`r15 = 0x060FE000`, `jmp 0x06010014`) and is a whole build of the
program. It is the **Japanese** one: its file-name table starts with
`SUNSOFT.BIN` where `0`'s has `WDLOGO.BIN`, and it has none of the English
strings (`CREATE NEW JOURNEY MARKER.`, `DRAGON MAIL`, `SCIMITAR`, the
save screens' `CARTRIDGE`, `INTERNAL`, `FORMATTED!!`). `SUNSOFT.BIN`
itself is not on this disc. Nothing in `0` names `ALG.GIN`.

## The Japanese master's disc script

`ALG.SCR` (88 839 bytes, CR LF text) is the script of the Japanese
disc's mastering: `Disc ALG.DSK`, a commented-out `CatalogNo 060924`, the
volume `ALBERT_ODYSSEY_GAIDEN` by `SUNSOFT,SUN_CORPORATION` (the US disc
says `WORKING DESIGNS`), then every file with its source folder on the
developers' machine: `root\` (the program, `File 0` from `root\ALG.BIN`,
with `;File A.BIN;1` commented out above it), `btl\` (the battles, among
them `BTL_DEB.BIN`), `pcm\` (the AIFF voices), `cdda\track02.cda` …
`track22.cda`. A commented-out track `dmamap` held `root\suncdda` and
`root\eucdda`. Two comment lines in Shift-JIS bracket the volume's identifiers and the
copyright files' entries: `追加文−始まり` and `追加文−終わり`, "added
text, start" and "end".

## A piece of the source

`A_TAM.C` (13 194 bytes, Shift-JIS) is a C function of the game,
`SramImageInit()`: it fills the save structure (`BackUpData_Type`,
`ChrStatus`, SBL's `Uint16`) with a **debug start**. Three `#if` blocks
choose where the hero stands; the one enabled puts him in room 0x42 at
(0x55D0, 0x7DD0) in a town, with a party of two (members 0 and 1). Its
comments name the towns of the town flag (シトナス, トマリ, マイセント,
ルクナート, トランピア, リリカル, ジェッジ), the airship's position and
flag, the menus' remembered cursors, stereo or mono, the save device
("0: CPU RAM, 1: backup cartridge"), 128 treasure flags, 64 event
flags, and the party: `ﾊﾟｲｸ` (Pike), `ｴｶ` (Eka), `ﾚｵｽ` (Leos), `ｴﾙﾀﾞｰ`
(Elder), `ｱﾓﾝ` (Amon), Pike at level 55 with 268 HP. The item loop
`sram->SramItemValue[i];` assigns nothing (a bug: the items keep what was
there).

## Other leftovers

* `TMP.LST`: 27 paths `c:\data\tmp\*.mst`, the monster files on someone's
  PC.
* `CHKLIST.MS` (216 bytes): a packed list of file names, each followed by
  a few bytes (dates and sizes, by their look):
  `ALG.BIN`, `CREDIT.BIN`, `IP.BIN`, `LOGO.BIN`, `OPNDEMO.BIN`,
  `OPNDEMO2.BIN`, `SUNBG.BIN`, `SUNSOFT.BIN`: the Japanese disc's root
  programs.
* `IVENT327.IF` next to `IVENT327.AIF`: both AIFF, 104 200 against 102 920
  bytes, different data: another take of the same line (by name).
* `MAP084.MAP`, `.HIT`, `.BGC`, `.BGP` and `ASAHI.CGP`, `.BGP`: one map
  in a set of formats no other file has (by extension).
* `EVENT1.BIN` and `BTL_DEB.BIN`: two programs nothing loads
  (`03-executables.md`).
* `DEMO1.BIN` to `DEMO4.BIN`: four programs `main` can load (states
  9–12) that are **not on the disc**, in both the US and the Japanese
  builds.
* The volume name stayed `ALBERT_ODYSSEY_GAIDEN`, the Japanese title,
  on the US disc.
