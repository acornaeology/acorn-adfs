#!/usr/bin/env python3
"""Remove manual comment() calls that duplicate py8dis auto-generated text.

Reads the assembly output to find doubled comments (two parts joined by ';'),
then checks which manual comment() calls in the driver are redundant because
py8dis auto-generates equivalent text (subroutine titles at JSR sites,
on_entry/on_exit annotations, ALWAYS branch notes, etc.).

Usage:
    python3 tools/remove_duplicate_comments.py --dry-run   # show what would be removed
    python3 tools/remove_duplicate_comments.py              # remove and rewrite driver
"""

import re
import sys


def main():
    dry_run = "--dry-run" in sys.argv

    asm_path = "versions/adfs-1.30/output/adfs-1.30.asm"
    driver_path = "versions/adfs-1.30/disassemble/disasm_adfs_130.py"

    # 1. Find all addresses with doubled comments in assembly output
    doubled = {}
    with open(asm_path) as f:
        for line in f:
            m = re.search(r'; ([0-9a-f]{4}): [0-9a-f ]{2,}\.{0,3}\s+; (.+)', line)
            if m and ';' in m.group(2):
                addr = int(m.group(1), 16)
                doubled[addr] = m.group(2)

    # 2. Read driver file
    with open(driver_path) as f:
        driver_lines = f.readlines()

    # 3. Find manual comment() calls at doubled addresses and mark for removal
    lines_to_remove = set()
    for i, line in enumerate(driver_lines):
        m = re.match(r'\s*comment\(0x([0-9A-Fa-f]+),\s*["\'](.+?)["\']\s*,\s*inline=True\)', line)
        if not m:
            continue
        addr = int(m.group(1), 16)
        manual_text = m.group(2)
        if addr not in doubled:
            continue

        # Check if this manual comment is one of the doubled parts
        output_text = doubled[addr]
        parts = [p.strip() for p in output_text.split(';')]

        if len(parts) < 2:
            continue

        # The manual comment should appear as one of the parts.
        # The OTHER part is the auto-generated one.
        # Remove the manual comment if the auto part is adequate.
        manual_in_output = manual_text in parts
        if not manual_in_output:
            continue

        other_parts = [p for p in parts if p != manual_text]
        if not other_parts:
            # Both parts are the same manual comment (exact duplicate)
            lines_to_remove.add(i)
            continue

        # Heuristic: remove the manual comment if it's less informative
        # than the auto-generated text, or if they say the same thing
        auto_text = other_parts[0]
        ml = manual_text.lower().strip()
        al = auto_text.lower().strip()

        should_remove = False

        # Exact match
        if ml == al:
            should_remove = True
        # Manual is substring of auto (auto is more detailed)
        elif ml in al:
            should_remove = True
        # Auto is substring of manual (manual is more detailed) - KEEP manual
        elif al in ml:
            should_remove = False
        # Auto is a subroutine title or on_exit annotation - remove manual
        # if manual just restates what auto says differently
        else:
            # Check for common patterns of auto-generated text
            # on_exit: "A=result code...", "X=control block..."
            # title: capitalized description matching subroutine name
            # ALWAYS branch
            if al == "always branch":
                should_remove = True
            elif re.match(r'^[axy]=', al):
                # on_entry/on_exit annotation
                should_remove = True

        if should_remove:
            lines_to_remove.add(i)

    # 4. Report or apply
    print(f"Found {len(lines_to_remove)} redundant comment() calls to remove")

    if dry_run:
        for i in sorted(lines_to_remove):
            print(f"  {i+1:5d}: {driver_lines[i].rstrip()}")
        return

    # Write updated driver
    with open(driver_path, 'w') as f:
        for i, line in enumerate(driver_lines):
            if i not in lines_to_remove:
                f.write(line)

    print(f"Removed {len(lines_to_remove)} lines from {driver_path}")


if __name__ == "__main__":
    main()
