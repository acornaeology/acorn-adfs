#!/usr/bin/env python3
"""Import label names from Hoglet's ADFS 1.30 disassembly.

Parses Hoglet's BeebAsm source to extract label-to-address mappings,
then outputs py8dis label() calls that can be added to the driver script.

Skips labels that are just address-based names (L8019, LFC40, etc.)
as these have no semantic value.
"""

import re
import sys
from pathlib import Path

HOGLET_SRC = Path("/Users/rjs/Code/ADFS130/src/ADFS130.asm")


def parse_hoglet_labels(filepath):
    """Extract labels from Hoglet's BeebAsm source.

    Returns dict of {address: label_name}.
    """
    labels = {}

    # Parse EQU-style definitions: LXXXX = $XXXX
    # and code labels: .LXXXX
    equ_re = re.compile(r'^(\w+)\s*=\s*\$([0-9A-Fa-f]+)\s*$')
    code_label_re = re.compile(r'^\.(\w+)\s*$')

    current_addr = None

    for line in filepath.read_text().splitlines():
        stripped = line.strip()

        # EQU definitions
        m = equ_re.match(stripped)
        if m:
            name = m.group(1)
            addr = int(m.group(2), 16)
            labels[addr] = name
            continue

        # Track ORG
        m = re.match(r'ORG\s+\$([0-9A-Fa-f]+)', stripped)
        if m:
            current_addr = int(m.group(1), 16)
            continue

        # Code labels
        m = code_label_re.match(stripped)
        if m:
            name = m.group(1)
            # We don't know the exact address without tracking P%
            # But we can extract them from the label name if it's Lxxxx
            if re.match(r'^L[0-9A-Fa-f]{4}$', name):
                addr = int(name[1:], 16)
                labels[addr] = name

    return labels


def is_opaque_label(name):
    """Check if a label is just an address-based name with no semantic value."""
    return bool(re.match(r'^L[0-9A-Fa-f]{4}$', name))


def main():
    if not HOGLET_SRC.exists():
        print(f"Error: {HOGLET_SRC} not found", file=sys.stderr)
        sys.exit(1)

    labels = parse_hoglet_labels(HOGLET_SRC)

    # Filter out opaque address-based labels
    meaningful = {addr: name for addr, name in labels.items()
                  if not is_opaque_label(name)}

    # Report
    print(f"Total labels from Hoglet: {len(labels)}")
    print(f"Meaningful (non-Lxxxx) labels: {len(meaningful)}")

    if meaningful:
        print("\nMeaningful labels:")
        for addr in sorted(meaningful):
            name = meaningful[addr]
            print(f"  label(0x{addr:04X}, \"{name}\")")


if __name__ == "__main__":
    main()
