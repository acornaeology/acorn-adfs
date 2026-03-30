#!/usr/bin/env python3
"""Identify basic blocks and their annotation status.

A basic block is a straight-line sequence of instructions with:
- One entry point (the first instruction)
- One exit point (the last instruction: branch, jump, or fall-through)
- No branches into the middle

For each uncommented basic block, shows:
- Predecessor blocks (what leads here) and their annotation status
- Successor blocks (what follows) and their annotation status
- Instructions in the block

Usage:
    python3 tools/basic_blocks.py [subroutine_addr]

If subroutine_addr given, shows blocks for that subroutine only.
Otherwise shows a summary of all subroutines with uncommented blocks.
"""

import json
import sys
from pathlib import Path

OUTPUT_JSON = Path("/Users/rjs/Code/acornaeology/acorn-adfs/versions/adfs-1.30/output/adfs-1.30.json")

BRANCH_MNEMONICS = {'bcc', 'bcs', 'beq', 'bne', 'bmi', 'bpl', 'bvc', 'bvs'}
JUMP_MNEMONICS = {'jmp', 'rts', 'rti', 'brk'}
CALL_MNEMONIC = 'jsr'


def find_basic_blocks(items):
    """Identify basic blocks from a list of code items.

    Returns list of blocks, each a dict with:
      addr: start address
      items: list of items in the block
      exits: list of (target_addr, type) where type is 'branch', 'fall', 'jump'
      entries: list of source addrs (filled in later)
      commented: count of commented items
    """
    if not items:
        return []

    # Find block-starting addresses
    # A block starts at:
    # 1. The first instruction
    # 2. Any branch target
    # 3. The instruction after a branch/jump
    block_starts = {items[0]['addr']}

    item_by_addr = {it['addr']: it for it in items}
    item_addrs = [it['addr'] for it in items]
    addr_set = set(item_addrs)

    for i, item in enumerate(items):
        mnemonic = item.get('mnemonic', '')
        target = item.get('target')

        if mnemonic in BRANCH_MNEMONICS:
            if target and target in addr_set:
                block_starts.add(target)
            # Instruction after branch starts a new block
            if i + 1 < len(items):
                block_starts.add(items[i+1]['addr'])

        elif mnemonic in JUMP_MNEMONICS or mnemonic == CALL_MNEMONIC:
            if i + 1 < len(items):
                block_starts.add(items[i+1]['addr'])

    # Also add addresses that are referenced (branch targets from outside)
    # by checking the 'referenced' info - any address with references is a block start
    for item in items:
        for lbl in item.get('labels', []):
            block_starts.add(item['addr'])

    # Sort block starts
    sorted_starts = sorted(block_starts & addr_set)

    # Build blocks
    blocks = []
    for bi, start in enumerate(sorted_starts):
        end = sorted_starts[bi + 1] if bi + 1 < len(sorted_starts) else items[-1]['addr'] + 1
        block_items = [it for it in items if start <= it['addr'] < end]
        if not block_items:
            continue

        commented = sum(1 for it in block_items if it.get('comment_inline'))

        # Determine exits
        exits = []
        last = block_items[-1]
        last_mnemonic = last.get('mnemonic', '')
        last_target = last.get('target')

        if last_mnemonic in BRANCH_MNEMONICS:
            if last_target:
                exits.append((last_target, 'branch'))
            # Fall-through
            if bi + 1 < len(sorted_starts):
                exits.append((sorted_starts[bi + 1], 'fall'))
        elif last_mnemonic == 'jmp':
            if last_target:
                exits.append((last_target, 'jump'))
        elif last_mnemonic == 'rts':
            exits.append((None, 'return'))
        elif last_mnemonic == CALL_MNEMONIC:
            # JSR returns to next instruction
            if bi + 1 < len(sorted_starts):
                exits.append((sorted_starts[bi + 1], 'fall'))
        else:
            # Fall-through
            if bi + 1 < len(sorted_starts):
                exits.append((sorted_starts[bi + 1], 'fall'))

        blocks.append({
            'addr': start,
            'items': block_items,
            'exits': exits,
            'entries': [],
            'commented': commented,
            'total': len(block_items),
        })

    # Fill in entries (predecessors)
    block_by_addr = {b['addr']: b for b in blocks}
    for block in blocks:
        for target, etype in block['exits']:
            if target and target in block_by_addr:
                block_by_addr[target]['entries'].append((block['addr'], etype))

    return blocks


def main():
    target_sub = None
    if len(sys.argv) > 1:
        target_sub = int(sys.argv[1].lstrip('&$').removeprefix('0x'), 16)

    data = json.load(OUTPUT_JSON.open())
    items = data['items']
    subs = sorted(data.get('subroutines', []), key=lambda s: s['addr'])

    for i, sub in enumerate(subs):
        start = sub['addr']
        end = subs[i+1]['addr'] if i+1 < len(subs) else 0xC000

        if target_sub is not None and start != target_sub:
            continue

        sub_items = [it for it in items if start <= it['addr'] < end and it['type'] == 'code']
        if len(sub_items) < 5:
            continue

        blocks = find_basic_blocks(sub_items)
        if not blocks:
            continue

        uncommented_blocks = [b for b in blocks if b['commented'] == 0 and b['total'] >= 2]

        if target_sub is not None:
            # Detailed view for one subroutine
            name = sub.get('name', f'sub_{start:04x}')
            total_commented = sum(b['commented'] for b in blocks)
            total_items = sum(b['total'] for b in blocks)
            print(f"Subroutine: {name} (&{start:04X})")
            print(f"Blocks: {len(blocks)}, Uncommented blocks (>=2 items): {len(uncommented_blocks)}")
            print(f"Items: {total_commented}/{total_items} commented")
            print()

            block_by_addr = {b['addr']: b for b in blocks}

            for block in uncommented_blocks:
                addr = block['addr']
                print(f"  Block &{addr:04X} ({block['total']} items, 0 comments)")

                # Show predecessors
                for pred_addr, etype in block['entries']:
                    pred = block_by_addr.get(pred_addr)
                    if pred:
                        status = 'COMMENTED' if pred['commented'] > 0 else 'uncommented'
                        print(f"    <- &{pred_addr:04X} ({etype}, {status})")

                # Show successors
                for succ_addr, etype in block['exits']:
                    if succ_addr and succ_addr in block_by_addr:
                        succ = block_by_addr[succ_addr]
                        status = 'COMMENTED' if succ['commented'] > 0 else 'uncommented'
                        print(f"    -> &{succ_addr:04X} ({etype}, {status})")

                # Show instructions
                for it in block['items']:
                    mnemonic = it.get('mnemonic', '???')
                    operand = it.get('operand', '')
                    print(f"      &{it['addr']:04X}  {mnemonic:4s} {operand}")
                print()
        else:
            # Summary view
            if not uncommented_blocks:
                continue
            name = sub.get('name', f'sub_{start:04x}')
            total_commented = sum(b['commented'] for b in blocks)
            total_items = sum(b['total'] for b in blocks)
            pct = 100 * total_commented / total_items if total_items else 0
            if pct >= 50:
                continue
            print(f"&{start:04X} {name}: {len(uncommented_blocks)} uncommented blocks, {total_commented}/{total_items} ({pct:.0f}%)")


if __name__ == "__main__":
    main()
