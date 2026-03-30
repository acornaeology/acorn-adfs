#!/usr/bin/env python3
"""Cross-reference ADFS-multi-target labels against our ADFS 1.30 ROM.

The multi-target repo builds from ca65 source and produces byte-identical
ROMs. We can build it for BBC SCSI (bbcSCSI config = ADFS 1.30) and
extract the symbol table to get meaningful label-to-address mappings.

Alternatively, we can parse the assembly listing to extract labels and
their addresses, then match them against our ROM.

This script takes a simpler approach: parse the ca65 source files to
find labels and their associated functionality descriptions from
comments, then output them for manual integration.
"""

import re
import sys
from pathlib import Path

MULTITARGET_SRC = Path("/Users/rjs/Code/ADFS-multi-target/src")


def extract_labels_from_asm(filepath):
    """Extract labels from ca65 assembly source.

    Returns list of (label_name, context_comment) tuples.
    """
    labels = []
    prev_comment = ""

    for line in filepath.read_text().splitlines():
        stripped = line.strip()

        # Track comments for context
        if stripped.startswith(";"):
            prev_comment = stripped.lstrip("; ").strip()
            continue

        # ca65 labels end with : or start at column 0 without tab
        m = re.match(r'^(\w+):', stripped)
        if m:
            name = m.group(1)
            # Skip private/local labels
            if not name.startswith("@") and not name.startswith("_"):
                labels.append((name, prev_comment))
            prev_comment = ""
        else:
            if stripped and not stripped.startswith("."):
                prev_comment = ""

    return labels


def main():
    if not MULTITARGET_SRC.exists():
        print(f"Error: {MULTITARGET_SRC} not found", file=sys.stderr)
        sys.exit(1)

    # Parse workspace definitions
    workspace_filepath = MULTITARGET_SRC / "includes" / "workspace.inc"
    if workspace_filepath.exists():
        wksp_re = re.compile(
            r'(WKSP_ADFS_\w+)\s*=\s*WKSP_BASE\s*\+\s*\$([0-9A-Fa-f]+)'
        )
        print("=== Workspace labels (WKSP_BASE = $0E00 for BBC) ===")
        print()
        for line in workspace_filepath.read_text().splitlines():
            m = wksp_re.search(line)
            if m:
                name = m.group(1)
                offset = int(m.group(2), 16)
                addr = 0x0E00 + offset  # BBC workspace base
                # Extract inline comment
                comment_m = re.search(r';(.+)$', line)
                comment = comment_m.group(1).strip() if comment_m else ""
                print(f"  0x{addr:04X}  {name:40s}  {comment}")

    # Parse main source for code labels
    adfs_filepath = MULTITARGET_SRC / "adfs.asm"
    if adfs_filepath.exists():
        labels = extract_labels_from_asm(adfs_filepath)
        print(f"\n=== Code labels from adfs.asm ({len(labels)} found) ===")
        print()
        for name, comment in labels[:80]:  # Show first 80
            print(f"  {name:40s}  {comment}")

    # Parse SCSI driver
    scsi_filepath = MULTITARGET_SRC / "SCSI_Driver.asm"
    if scsi_filepath.exists():
        labels = extract_labels_from_asm(scsi_filepath)
        print(f"\n=== SCSI driver labels ({len(labels)} found) ===")
        print()
        for name, comment in labels:
            print(f"  {name:40s}  {comment}")

    # Parse floppy driver
    floppy_filepath = MULTITARGET_SRC / "floppy.asm"
    if floppy_filepath.exists():
        labels = extract_labels_from_asm(floppy_filepath)
        print(f"\n=== Floppy driver labels ({len(labels)} found) ===")
        print()
        for name, comment in labels[:40]:
            print(f"  {name:40s}  {comment}")


if __name__ == "__main__":
    main()
