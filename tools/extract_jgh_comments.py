#!/usr/bin/env python3
"""Extract block comments from J.G. Harston's ADFS 1.30 disassembly.

JGH's source is a BBC BASIC program with assembly language in [OPT...] blocks.
Block comments (lines starting with ;) are associated with the next code label.
Labels are .LXXXX format, giving us direct address mapping.

Outputs a list of (address, comment_text) pairs for integration into our driver.
"""

import re
import sys
from pathlib import Path

JGH_SRC = Path("/Users/rjs/Code/ADFS130-JGH/adfs130.src")


def extract_comments_with_addresses(filepath):
    """Extract block comments and associate them with the next code address.

    Returns list of (address, [comment_lines]) pairs.
    """
    results = []
    current_comment = []
    lines = filepath.read_text().splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Collect comment lines
        if stripped.startswith(";"):
            comment_text = stripped.lstrip("; ").rstrip()
            if comment_text and not all(c in "-=~" for c in comment_text):
                current_comment.append(comment_text)
            continue

        # Check for a label following comments
        if current_comment:
            m = re.match(r'\.L([0-9A-Fa-f]{4})', stripped)
            if m:
                addr = int(m.group(1), 16)
                results.append((addr, current_comment))
                current_comment = []
            elif stripped and not stripped.startswith("\\"):
                # Non-label, non-comment line - discard accumulated comments
                current_comment = []

    return results


def main():
    if not JGH_SRC.exists():
        print(f"Error: {JGH_SRC} not found", file=sys.stderr)
        sys.exit(1)

    comments = extract_comments_with_addresses(JGH_SRC)

    print(f"# {len(comments)} commented code sections from JGH disassembly")
    print()

    for addr, lines in sorted(comments):
        # Only show comments with real content (not just noise)
        text = " ".join(lines)
        if len(text) < 5:
            continue
        print(f"# &{addr:04X}: {text}")
        # Output as py8dis comment() calls (truncated to 62 chars)
        for line in lines:
            if len(line) > 62:
                line = line[:59] + "..."
            print(f'comment(0x{addr:04X}, "{line}")')
        print()


if __name__ == "__main__":
    main()
