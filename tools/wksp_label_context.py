#!/usr/bin/env python3
"""Extract usage context for workspace labels from the ADFS disassembly.

Shows all assembly lines referencing a given label with surrounding context,
helping to determine the label's actual purpose for renaming.

Usage:
    python3 tools/wksp_label_context.py wksp_1001          # specific label
    python3 tools/wksp_label_context.py wksp_1001 -C 5     # with 5 lines context
    python3 tools/wksp_label_context.py --hex-only          # all wksp_XXXX hex labels
    python3 tools/wksp_label_context.py --all               # all wksp_ labels
"""

import re
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Extract workspace label usage context")
    parser.add_argument("label", nargs="?", help="Label name to search for")
    parser.add_argument("-C", "--context", type=int, default=3,
                        help="Number of context lines before/after (default: 3)")
    parser.add_argument("--hex-only", action="store_true",
                        help="Show only wksp_XXXX hex-address labels")
    parser.add_argument("--all", action="store_true",
                        help="Show all wksp_ labels")
    parser.add_argument("--summary", action="store_true",
                        help="Show summary of reference counts only")
    args = parser.parse_args()

    asm_path = "versions/adfs-1.30/output/adfs-1.30.asm"
    lines = open(asm_path).readlines()

    if args.label:
        labels = [args.label]
    elif args.hex_only:
        labels = find_hex_wksp_labels(lines)
    elif args.all:
        labels = find_all_wksp_labels(lines)
    else:
        parser.print_help()
        return

    for label in labels:
        show_label_context(label, lines, args.context, args.summary)


def find_hex_wksp_labels(lines):
    """Find wksp_ labels that still have hex-address names."""
    labels = []
    for line in lines:
        m = re.match(r"^(wksp_[0-9a-f]{4})\s+=\s+&([0-9a-f]{4})$", line, re.IGNORECASE)
        if m:
            labels.append(m.group(1))
    return labels


def find_all_wksp_labels(lines):
    """Find all wksp_ labels."""
    labels = []
    for line in lines:
        m = re.match(r"^(wksp_\w+)\s+=\s+&([0-9a-f]{4})$", line, re.IGNORECASE)
        if m:
            labels.append(m.group(1))
    return labels


def show_label_context(label, lines, context_lines, summary_only):
    """Show all references to a label with surrounding context."""
    refs = []
    for i, line in enumerate(lines):
        # Skip the definition line
        if line.startswith(f"{label} "):
            continue
        if re.search(rf'\b{re.escape(label)}\b', line):
            refs.append(i)

    print(f"=== {label} — {len(refs)} references ===")

    if summary_only:
        print()
        return

    shown_ranges = set()
    for ref_idx in refs:
        start = max(0, ref_idx - context_lines)
        end = min(len(lines), ref_idx + context_lines + 1)

        # Skip if this range overlaps with an already-shown range
        current_range = set(range(start, end))
        if current_range & shown_ranges:
            # Still show the reference line itself if not shown
            if ref_idx not in shown_ranges:
                print(f"  {ref_idx + 1:5d}: >>> {lines[ref_idx].rstrip()}")
                shown_ranges.add(ref_idx)
            continue

        shown_ranges.update(current_range)
        print(f"  ---")
        for j in range(start, end):
            marker = ">>>" if j == ref_idx else "   "
            print(f"  {j + 1:5d}: {marker} {lines[j].rstrip()}")

    print()


if __name__ == "__main__":
    main()
