# Acorn ADFS

[![Verify disassembly](https://github.com/acornaeology/acorn-adfs/actions/workflows/verify.yml/badge.svg)](https://github.com/acornaeology/acorn-adfs/actions/workflows/verify.yml)

ADFS (Advanced Disc Filing System) is a floppy disc and SCSI hard disc filing system for the BBC Micro. It supports hierarchical directories, random access files, and the Acorn free space map format. ADFS plugs into the MOS filing system framework, providing implementations of OSFILE, OSFIND, OSGBPB, OSBGET, OSBPUT, and OSARGS. It also handles disc formatting, defect mapping, and file compaction. The ROM contains both the floppy disc driver (using the WD1770 controller) and the SCSI hard disc driver.

This repository contains annotated disassemblies of the Acorn ADFS ROM, produced by reverse-engineering the original 6502 machine code. Each disassembly includes named labels, comments explaining the logic, and cross-references between subroutines.

## Versions

- **Acorn ADFS 1.30**
  - [Formatted disassembly on acornaeology.uk](https://acornaeology.uk/acorn-adfs/1.30.html)
  - [Disassembly source on GitHub](https://github.com/acornaeology/acorn-adfs/tree/master/versions/adfs-1.30)
  - [ROM in BBC Micro ROM Library](https://tobylobster.github.io/rom_library/?md5=831ee90ac5d49ba5507252faf0c12536)

## How it works

The disassembly is produced by a Python script that drives a custom version of [py8dis](https://github.com/acornaeology/py8dis), a programmable disassembler for 6502 binaries. The script feeds the original ROM image to py8dis along with annotations — entry points, labels, constants, and comments — to produce readable assembly output.

The output is verified by reassembling with [beebasm](https://github.com/stardot/beebasm) and comparing the result byte-for-byte against the original ROM. This round-trip verification runs automatically in CI on every push.

## Disassembling locally

Requires [uv](https://docs.astral.sh/uv/) and [beebasm](https://github.com/stardot/beebasm) (v1.10+).

```sh
uv sync
uv run acorn-adfs-disasm-tool disassemble 1.30
uv run acorn-adfs-disasm-tool verify 1.30
```

## (Re-)Assembling locally

To assemble the `.asm` file back into a ROM image using [beebasm](https://github.com/stardot/beebasm):

```sh
beebasm -i versions/adfs-1.30/output/adfs-1.30.asm -o adfs-1.30.rom
```

## References

- [Hoglet's ADFS 1.30 disassembly](https://github.com/hoglet67/ADFS130)
  A BeebAsm-syntax disassembly that reassembles to byte-identical ROMs for multiple ADFS variants. Provided important structural guidance.
- [Dominic Beesley's ADFS multi-target reassembly](https://github.com/dominicbeesley/ADFS-multi-target)
  A ca65-based multi-target reassembly covering many ADFS versions with well-named labels and modular driver separation.
- [J.G. Harston's ADFS 1.30 disassembly](https://mdfs.net/Info/Comp/BBC/ADFS/)
  A BBC BASIC-embedded disassembly with informative block comments and entry/exit documentation for key routines.
- [Acorn ADFS User Guide](https://stardot.org.uk/forums/viewtopic.php?t=13082)
  Stardot forum thread discussing ADFS 1.30 disassembly with technical details on SCSI protocol, workspace layout, and retry mechanisms.

## Credits

- [py8dis](https://github.com/acornaeology/py8dis) by [SteveF](https://github.com/ZornsLemma), forked for use with acornaeology
- [beebasm](https://github.com/stardot/beebasm) by Rich Mayfield and contributors
- [The BBC Micro ROM Library](https://tobylobster.github.io/rom_library/) by tobylobster

## License

The annotations and disassembly scripts in this repository are released under the [MIT License](LICENSE). The original ROM images remain the property of their respective copyright holders.
