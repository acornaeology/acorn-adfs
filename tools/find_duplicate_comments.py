#!/usr/bin/env python3
"""Find doubled inline comments in the ADFS disassembly output.

Analyses the assembly output to find lines where multiple comments
are joined with ';', indicating a manual comment() call duplicates
or conflicts with an auto-generated py8dis annotation (subroutine
title at JSR sites, on_exit register annotations, etc.).

Usage:
    python3 tools/find_duplicate_comments.py             # show all
    python3 tools/find_duplicate_comments.py --removable # show only safe-to-remove
"""

import re
import sys


def main():
    show_removable = "--removable" in sys.argv

    asm_path = "versions/adfs-1.30/output/adfs-1.30.asm"
    driver_path = "versions/adfs-1.30/disassemble/disasm_adfs_130.py"

    # Read assembly output and find all doubled comments
    doubled = {}
    with open(asm_path) as f:
        for line in f:
            m = re.search(r'; ([0-9a-f]{4}): [0-9a-f ]{2,}\.{0,3}\s+; (.+)', line)
            if m and ';' in m.group(2):
                addr = int(m.group(1), 16)
                doubled[addr] = m.group(2)

    # Read driver and find manual comment() calls at those addresses
    driver_comments = {}
    with open(driver_path) as f:
        for i, line in enumerate(f, 1):
            m = re.match(r'\s*comment\(0x([0-9A-Fa-f]+),\s*["\'](.+?)["\']\s*,\s*inline=True\)', line)
            if m:
                addr = int(m.group(1), 16)
                if addr in doubled:
                    driver_comments.setdefault(addr, []).append((i, m.group(2)))

    # Analyse each doubled comment
    for addr in sorted(doubled.keys()):
        parts = [p.strip() for p in doubled[addr].split(';')]
        manual = driver_comments.get(addr, [])

        if not manual:
            continue

        # Check if any manual comment is a near-duplicate of an auto comment
        for line_no, manual_text in manual:
            auto_parts = [p for p in parts if p != manual_text]
            is_redundant = False
            for auto in auto_parts:
                # Check if manual comment is redundant given auto text
                ml = manual_text.lower().strip()
                al = auto.lower().strip()
                if ml == al:
                    is_redundant = True
                    break
                if ml in al or al in ml:
                    is_redundant = True
                    break

            if show_removable:
                if is_redundant:
                    print(f"  {line_no:5d}: REMOVE  0x{addr:04X} \"{manual_text}\"")
                    print(f"         AUTO            \"{'; '.join(auto_parts)}\"")
            else:
                status = "REDUNDANT" if is_redundant else "KEEP?"
                print(f"  {line_no:5d}: {status:9s} 0x{addr:04X}")
                print(f"         manual: \"{manual_text}\"")
                print(f"         output: \"{doubled[addr]}\"")

    if not show_removable:
        print(f"\nTotal addresses with doubled comments: {len(doubled)}")
        print(f"Driver comment() calls at those addresses: {sum(len(v) for v in driver_comments.values())}")


if __name__ == "__main__":
    main()
