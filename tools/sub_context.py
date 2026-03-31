#!/usr/bin/env python3
"""Extract calling convention context for subroutines from the ADFS disassembly.

For a given subroutine label, shows:
  1. The first N lines of the subroutine body (to see what registers are read)
  2. All call sites (JSR label) with context before each (to see what callers set up)
  3. Exit points (RTS/JMP) with context (to see what's returned)
  4. What callers do after the JSR (to see if flags/registers are tested)

Usage:
    python3 tools/sub_context.py claim_tube
    python3 tools/sub_context.py claim_tube --body 30
    python3 tools/sub_context.py --batch 0x8000 0x83FF
    python3 tools/sub_context.py --list
"""

import re
import sys
import argparse

DRIVER_PATH = "versions/adfs-1.30/disassemble/disasm_adfs_130.py"
ASM_PATH = "versions/adfs-1.30/output/adfs-1.30.asm"


def get_subroutine_defs():
    """Extract all subroutine() definitions from the driver script.

    Returns list of (addr, name) tuples.
    """
    subs = []
    with open(DRIVER_PATH) as f:
        for line in f:
            m = re.match(r'\s*subroutine\(\s*0x([0-9A-Fa-f]+)\s*,\s*"([^"]+)"', line)
            if m:
                subs.append((int(m.group(1), 16), m.group(2)))
    return sorted(subs)


def main():
    parser = argparse.ArgumentParser(description="Subroutine calling convention context")
    parser.add_argument("label", nargs="?", help="Subroutine label name")
    parser.add_argument("--body", type=int, default=20,
                        help="Lines of subroutine body to show (default: 20)")
    parser.add_argument("--caller-context", type=int, default=3,
                        help="Lines before each call site (default: 3)")
    parser.add_argument("--after-context", type=int, default=2,
                        help="Lines after each call site (default: 2)")
    parser.add_argument("--batch", nargs=2, metavar=("START", "END"),
                        help="Show summary for subroutines in address range (hex)")
    parser.add_argument("--list", action="store_true",
                        help="List all subroutine labels with addresses")
    args = parser.parse_args()

    lines = open(ASM_PATH).readlines()
    all_subs = get_subroutine_defs()

    if args.list:
        for addr, name in all_subs:
            print(f"  &{addr:04X}  {name}")
        print(f"\nTotal: {len(all_subs)} subroutines")
        return

    if args.batch:
        start = int(args.batch[0], 16)
        end = int(args.batch[1], 16)
        batch_summary(lines, all_subs, start, end)
        return

    if not args.label:
        parser.print_help()
        return

    show_subroutine_context(args.label, lines, all_subs, args.body,
                            args.caller_context, args.after_context)


def find_subroutine_line(label, lines):
    """Find the line number where .label appears."""
    target = f".{label}"
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == target or stripped.startswith(target + " "):
            return i
    return None


def find_next_subroutine_line(label, lines, all_subs):
    """Find the line of the next subroutine after this one."""
    sub_names = [name for _, name in all_subs]
    try:
        idx = sub_names.index(label)
    except ValueError:
        return len(lines)
    if idx + 1 < len(sub_names):
        next_line = find_subroutine_line(sub_names[idx + 1], lines)
        if next_line is not None:
            return next_line
    return len(lines)


def show_subroutine_context(label, lines, all_subs, body_lines, caller_ctx, after_ctx):
    """Show full calling convention context for a subroutine."""
    sub_line = find_subroutine_line(label, lines)
    if sub_line is None:
        print(f"Subroutine '.{label}' not found")
        return

    sub_end = find_next_subroutine_line(label, lines, all_subs)

    # 1. Subroutine body (first N instructions)
    print(f"=== {label} — body (first {body_lines} instructions) ===")
    count = 0
    for i in range(sub_line, min(len(lines), sub_line + body_lines * 3)):
        line = lines[i].rstrip()
        if line:
            print(f"  {i+1:5d}: {line}")
            if re.search(r'; [0-9a-f]{4}:', line):
                count += 1
                if count >= body_lines:
                    break
    print()

    # 2. Call sites (JSR label) with context before and after
    call_pattern = re.compile(rf'\bjsr {re.escape(label)}\b', re.IGNORECASE)
    call_sites = []
    for i, line in enumerate(lines):
        if call_pattern.search(line):
            call_sites.append(i)

    print(f"=== {label} — {len(call_sites)} call sites ===")
    for idx, call_line in enumerate(call_sites):
        start = max(0, call_line - caller_ctx)
        end = min(len(lines), call_line + after_ctx + 1)
        print(f"  --- call site {idx+1}/{len(call_sites)} ---")
        for j in range(start, end):
            marker = ">>>" if j == call_line else "   "
            print(f"  {j+1:5d}: {marker} {lines[j].rstrip()}")
    print()

    # 3. Exit points within the subroutine (RTS only, within subroutine bounds)
    print(f"=== {label} — exit points ===")
    for i in range(sub_line, sub_end):
        line = lines[i].strip()
        if re.search(r'\brts\b', line, re.IGNORECASE):
            start = max(sub_line, i - 3)
            print(f"  --- RTS at line {i+1} ---")
            for j in range(start, min(sub_end, i + 1)):
                marker = ">>>" if j == i else "   "
                print(f"  {j+1:5d}: {marker} {lines[j].rstrip()}")
    print()


def batch_summary(lines, all_subs, start_addr, end_addr):
    """Show brief summary for subroutines in an address range."""
    batch_subs = [(addr, name) for addr, name in all_subs
                  if start_addr <= addr <= end_addr]

    print(f"=== Subroutines in &{start_addr:04X}-&{end_addr:04X}: {len(batch_subs)} found ===")
    for addr, name in batch_subs:
        call_pattern = re.compile(rf'\bjsr {re.escape(name)}\b', re.IGNORECASE)
        call_count = sum(1 for l in lines if call_pattern.search(l))
        print(f"  &{addr:04X}  {name:<45s}  ({call_count} calls)")


if __name__ == "__main__":
    main()
