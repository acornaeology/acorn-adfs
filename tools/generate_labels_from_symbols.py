#!/usr/bin/env python3
"""Generate py8dis label() and entry() calls from multi-target symbols.

Reads the ld65 debug file, filters to meaningful ROM code labels,
converts to snake_case, and outputs py8dis declarations.
"""

import re
import sys
from pathlib import Path

DBG_FILEPATH = Path("/Users/rjs/Code/ADFS-multi-target/build/bbcSCSI.dbg")


def parse_symbols(filepath):
    """Parse ld65 debug file symbols."""
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


def is_opaque(name):
    """Skip opaque or internal labels."""
    if re.match(r'^L[0-9A-Fa-f]{3,5}$', name):
        return True
    if re.match(r'^LB[0-9A-Fa-f]{3}$', name):
        return True
    if name.startswith('_'):  # private/local
        return True
    if name.startswith('@'):  # local
        return True
    if 'rts' in name.lower() and len(name) < 12:  # return labels
        return True
    if re.match(r'^(sk\d|lp)$', name):  # generic skip/loop
        return True
    return False


def to_snake_case(name):
    """Convert CamelCase/mixed label to snake_case."""
    # Handle common prefixes
    name = name.replace('SCSI_', 'scsi_')
    name = name.replace('HD_', 'hd_')
    name = name.replace('FSM', 'fsm')
    name = name.replace('FSC', 'fsc')
    name = name.replace('DIR', 'dir')
    name = name.replace('NMI', 'nmi')
    name = name.replace('VFS_', 'vfs_')

    # Handle star commands
    if name.startswith('star'):
        cmd = name[4:]
        return f"star_{cmd.lower()}"

    # Handle my_ prefix (filing system vector handlers)
    if name.startswith('my_'):
        return name.lower()

    # Handle Serv prefix
    if name.startswith('Serv'):
        return f"service_handler_{name[4:]}"

    # Handle str/strr prefix (string data)
    if name.startswith('strr_') or name.startswith('str_'):
        return name.lower()

    # Handle tbl prefix (tables)
    if name.startswith('tbl_') or name.startswith('tbl'):
        return name.lower() if '_' in name else f"tbl_{name[3:].lower()}"

    # Handle brk prefix (BRK error generators)
    if name.startswith('brk'):
        rest = name[3:]
        # Insert underscore before caps
        result = re.sub(r'([A-Z])', r'_\1', rest).lower().strip('_')
        return f"brk_{result}"

    # General CamelCase to snake_case
    # Insert _ before uppercase letters that follow lowercase
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    # Insert _ before uppercase letter followed by lowercase (acronyms)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    return s.lower()


def main():
    symbols = parse_symbols(DBG_FILEPATH)

    # Filter to meaningful ROM code labels
    rom_syms = [(a, n) for a, n, t in symbols
                if 0x8000 <= a < 0xC000 and not is_opaque(n)]

    # Deduplicate by address (keep first meaningful name)
    seen = {}
    for addr, name in rom_syms:
        if addr not in seen:
            seen[addr] = name

    # Sort by address
    sorted_syms = sorted(seen.items())

    print(f"# {len(sorted_syms)} ROM code labels from ADFS-multi-target bbcSCSI build")
    print(f"# Addresses map directly to ADFS 1.30 (byte-identical ROM)")
    print()

    for addr, name in sorted_syms:
        snake = to_snake_case(name)
        # Emit entry() for subroutine-like labels
        print(f'label(0x{addr:04X}, "{snake}")')

    # Also emit entry() calls for the most important ones
    print()
    print("# Entry points for key subroutines")
    important_prefixes = ('star_', 'my_os', 'service_', 'scsi_', 'hd_',
                          'floppy', 'command', 'generate_error', 'reload',
                          'invalidate', 'load_fsm', 'check')
    for addr, name in sorted_syms:
        snake = to_snake_case(name)
        if any(snake.startswith(p) for p in important_prefixes):
            print(f'entry(0x{addr:04X})')


if __name__ == "__main__":
    main()
