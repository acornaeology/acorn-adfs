#!/usr/bin/env python3
"""Generate comment suggestions for uncommented code.

Uses operand labels and instruction patterns to suggest
comments for each uncommented instruction. Output format
is ready to paste into the driver script.

Usage:
    python3 tools/suggest_comments.py <start_addr> <end_addr>
"""

import json
import sys
from pathlib import Path

OUTPUT_JSON = Path("/Users/rjs/Code/acornaeology/acorn-adfs/versions/adfs-1.30/output/adfs-1.30.json")

# Known label patterns and their likely meanings
WORKSPACE_HINTS = {
    'wksp_ch_flags': 'channel flags',
    'wksp_ch_ext': 'channel EXT (file extent)',
    'wksp_ch_ptr': 'channel PTR (file pointer)',
    'wksp_current_drive': 'current drive number',
    'wksp_saved_drive': 'saved drive number',
    'wksp_disc_op': 'disc operation control block',
    'wksp_object_sector': 'object sector address',
    'wksp_object_name': 'object name buffer',
    'wksp_osfile_block': 'OSFILE control block',
    'wksp_csd': 'current selected directory',
    'wksp_lib': 'library directory',
    'wksp_err': 'error workspace',
    'wksp_cur_channel': 'current channel number',
    'fsm_sector_0': 'FSM sector 0 (addresses)',
    'fsm_sector_1': 'FSM sector 1 (lengths)',
    'dir_buffer': 'directory buffer',
    'dir_first_entry': 'first directory entry',
    'dir_name': 'directory name',
    'dir_title': 'directory title',
    'dir_parent_sector': 'parent directory sector',
    'dir_master_sequence': 'directory sequence number',
    'zp_flags': 'ADFS status flags',
    'zp_channel_offset': 'channel table index',
    'zp_retry_count': 'disc operation retry counter',
}


def suggest_comment(item, addr_map, label_map):
    """Generate a comment suggestion for an instruction."""
    mnemonic = item.get('mnemonic', '')
    operand = item.get('operand', '')
    target = item.get('target')

    # Check for calls to named subroutines
    if mnemonic in ('jsr', 'jmp') and target:
        if target in label_map:
            return None  # py8dis already adds the subroutine title

    # Check operand for workspace labels
    for label, hint in WORKSPACE_HINTS.items():
        if label in operand:
            if mnemonic == 'lda':
                return f"Get {hint}"
            elif mnemonic == 'sta':
                return f"Store in {hint}"
            elif mnemonic == 'cmp':
                return f"Compare with {hint}"
            elif mnemonic == 'ldx':
                return f"X = {hint}"
            elif mnemonic == 'ldy':
                return f"Y = {hint}"
            elif mnemonic in ('inc', 'dec'):
                return f"{'Increment' if mnemonic == 'inc' else 'Decrement'} {hint}"
            elif mnemonic in ('ora', 'and', 'eor'):
                return f"Modify {hint}"

    # Pattern-based suggestions
    if mnemonic == 'rts':
        return None  # RTS is obvious
    if mnemonic == 'pha':
        return "Save A on stack"
    if mnemonic == 'pla':
        return "Restore A from stack"
    if mnemonic == 'php':
        return "Save processor flags"
    if mnemonic == 'plp':
        return "Restore processor flags"
    if mnemonic == 'tax':
        return "Transfer A to X"
    if mnemonic == 'tay':
        return "Transfer A to Y"
    if mnemonic == 'txa':
        return "Transfer X to A"
    if mnemonic == 'tya':
        return "Transfer Y to A"
    if mnemonic == 'clc':
        return "Clear carry"
    if mnemonic == 'sec':
        return "Set carry"
    if mnemonic == 'cli':
        return "Enable interrupts"
    if mnemonic == 'sei':
        return "Disable interrupts"

    return None  # No suggestion


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <start_addr> <end_addr>")
        print(f"  Addresses in hex (e.g. 8D21 8D70)")
        sys.exit(1)

    start = int(sys.argv[1].lstrip('&$').removeprefix('0x'), 16)
    end = int(sys.argv[2].lstrip('&$').removeprefix('0x'), 16)

    data = json.load(OUTPUT_JSON.open())
    items = data['items']
    addr_map = {it['addr']: it for it in items}

    label_map = {}
    for s in data.get('subroutines', []):
        label_map[s['addr']] = s.get('name', '')

    print(f"# Comment suggestions for &{start:04X}-&{end:04X}")
    print()

    count = 0
    for item in items:
        addr = item['addr']
        if addr < start or addr >= end:
            continue
        if item['type'] != 'code':
            continue
        if item.get('comment_inline'):
            continue  # Already commented

        suggestion = suggest_comment(item, addr_map, label_map)
        if suggestion:
            print(f'comment(0x{addr:04X}, "{suggestion}", inline=True)')
            count += 1

    print(f"\n# {count} suggestions generated")


if __name__ == "__main__":
    main()
