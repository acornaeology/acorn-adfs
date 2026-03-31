#!/usr/bin/env python3
"""Extract usage context for auto-generated labels.

For each lXXXX label, shows all assembly lines that reference it,
helping to infer the label's purpose for renaming.

Usage:
    python3 tools/label_context.py [label_name]
    python3 tools/label_context.py          # all auto-generated labels
    python3 tools/label_context.py l1017    # specific label
"""

import re
import sys


def main():
    asm_path = "versions/adfs-1.30/output/adfs-1.30.asm"
    lines = open(asm_path).readlines()

    # Find all auto-generated labels
    auto_labels = []
    for line in lines:
        m = re.match(r"^(l[0-9a-f]{4})\s+=\s+&([0-9a-f]{4})$", line)
        if m:
            auto_labels.append((m.group(1), int(m.group(2), 16)))

    # Filter to specific label if given
    if len(sys.argv) > 1:
        target = sys.argv[1]
        auto_labels = [(n, a) for n, a in auto_labels if n == target]
        if not auto_labels:
            print(f"Label '{target}' not found")
            return

    for name, addr in auto_labels:
        # Find all lines referencing this label
        refs = []
        for i, line in enumerate(lines):
            # Skip the definition line itself
            if line.startswith(f"{name} "):
                continue
            # Check for the label name as a word boundary
            if re.search(rf'\b{name}\b', line):
                refs.append((i + 1, line.rstrip()))

        print(f"=== {name} (&{addr:04X}) — {len(refs)} references ===")
        for lineno, text in refs[:10]:  # limit to 10 refs
            # Trim to reasonable width
            print(f"  {lineno:5d}: {text[:100]}")
        if len(refs) > 10:
            print(f"  ... and {len(refs) - 10} more")
        print()


if __name__ == "__main__":
    main()
