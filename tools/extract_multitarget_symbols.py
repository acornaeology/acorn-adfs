#!/usr/bin/env python3
"""Extract meaningful symbols from the ADFS-multi-target ld65 debug file.

Parses the bbcSCSI.dbg file to extract symbol names and their resolved
addresses. Filters out opaque L-address labels (L8019, LFC40, etc.)
and outputs the meaningful ones grouped by address range.

The bbcSCSI config produces a byte-identical ROM to ADFS 1.30, so
addresses map directly.
"""

import re
import sys
from pathlib import Path

DBG_FILEPATH = Path("/Users/rjs/Code/ADFS-multi-target/build/bbcSCSI.dbg")


def parse_symbols(filepath):
    """Parse ld65 debug file and extract symbol names and addresses.

    Returns list of (address, name, sym_type) tuples.
    """
    symbols = []
    sym_re = re.compile(
        r'^sym\s+.*name="([^"]+)".*val=(0x[0-9A-Fa-f]+).*type=(\w+)'
    )

    for line in filepath.read_text().splitlines():
        m = sym_re.match(line)
        if m:
            name = m.group(1)
            addr = int(m.group(2), 16)
            sym_type = m.group(3)
            symbols.append((addr, name, sym_type))

    return symbols


def is_opaque_label(name):
    """Check if a label is an opaque address-based name."""
    # L followed by hex digits (L8019, LFC40, LFFDA, etc.)
    if re.match(r'^L[0-9A-Fa-f]{3,5}$', name):
        return True
    # LBA00 style from floppy driver
    if re.match(r'^LB[0-9A-Fa-f]{3}$', name):
        return True
    return False


def main():
    if not DBG_FILEPATH.exists():
        print(f"Error: {DBG_FILEPATH} not found", file=sys.stderr)
        print("Build with: cd /Users/rjs/Code/ADFS-multi-target && make -C src ROMNAME=bbcSCSI",
              file=sys.stderr)
        sys.exit(1)

    symbols = parse_symbols(DBG_FILEPATH)
    print(f"Total symbols: {len(symbols)}", file=sys.stderr)

    # Filter to meaningful labels only
    meaningful = [(addr, name, st) for addr, name, st in symbols
                  if not is_opaque_label(name)]
    print(f"Meaningful (non-Lxxxx) symbols: {len(meaningful)}", file=sys.stderr)

    # Group by address range
    rom_syms = [(a, n, t) for a, n, t in meaningful if 0x8000 <= a < 0xC000]
    zp_syms = [(a, n, t) for a, n, t in meaningful if a < 0x100]
    wksp_syms = [(a, n, t) for a, n, t in meaningful
                 if 0x0E00 <= a < 0x1C00]
    hw_syms = [(a, n, t) for a, n, t in meaningful if 0xFC00 <= a < 0xFF00]
    os_syms = [(a, n, t) for a, n, t in meaningful if a >= 0xFF00]
    const_syms = [(a, n, t) for a, n, t in meaningful
                  if a < 0x100 and not (0x00 <= a <= 0xFF)]
    other_syms = [(a, n, t) for a, n, t in meaningful
                  if not (0x8000 <= a < 0xC000)
                  and not (a < 0x100)
                  and not (0x0E00 <= a < 0x1C00)
                  and not (0xFC00 <= a)
                  and not (0x0100 <= a < 0x0E00)]

    print(f"\nROM code labels ({len(rom_syms)}):", file=sys.stderr)
    print(f"Zero page labels ({len(zp_syms)}):", file=sys.stderr)
    print(f"Workspace labels ({len(wksp_syms)}):", file=sys.stderr)
    print(f"Hardware labels ({len(hw_syms)}):", file=sys.stderr)
    print(f"OS entry labels ({len(os_syms)}):", file=sys.stderr)

    # Output ROM code labels (most useful for our disassembly)
    print("\n# === ROM code labels ===")
    for addr, name, st in sorted(rom_syms):
        print(f"0x{addr:04X}  {name}")

    print("\n# === Zero page labels ===")
    for addr, name, st in sorted(zp_syms):
        print(f"0x{addr:04X}  {name}")

    print("\n# === Workspace labels ===")
    for addr, name, st in sorted(wksp_syms):
        print(f"0x{addr:04X}  {name}")

    print("\n# === Hardware register labels ===")
    for addr, name, st in sorted(hw_syms):
        print(f"0x{addr:04X}  {name}")

    print("\n# === Constants and flags ===")
    # Also extract EQU-style constants (small values that aren't addresses)
    all_small = [(a, n, t) for a, n, t in meaningful if a < 0x100]
    for addr, name, st in sorted(all_small):
        if not name.startswith("ZP_") and not name.startswith("zp_"):
            print(f"0x{addr:02X}  {name}")


if __name__ == "__main__":
    main()
