#!/usr/bin/env python3
"""Analyse uncommented code regions using cross-reference context.

For each large uncommented region, reports:
- Named callees (JSR/JMP targets with labels)
- Named callers (who references addresses in this region)
- Workspace locations accessed (named labels in operands)
- Inline error messages found nearby

This helps infer the purpose of unannotated code from its
relationships with already-understood code.
"""

import json
import re
import sys
from pathlib import Path

OUTPUT_JSON = Path("/Users/rjs/Code/acornaeology/acorn-adfs/versions/adfs-1.30/output/adfs-1.30.json")
OUTPUT_ASM = Path("/Users/rjs/Code/acornaeology/acorn-adfs/versions/adfs-1.30/output/adfs-1.30.asm")


def main():
    data = json.load(OUTPUT_JSON.open())
    items = data['items']
    subs = sorted(data.get('subroutines', []), key=lambda s: s['addr'])

    # Build address-to-item map
    addr_map = {it['addr']: it for it in items}

    # Build named labels map
    named = {}
    for s in subs:
        named[s['addr']] = s.get('name', f"sub_{s['addr']:04x}")
    for lbl_addr_str, lbl_addr in data.get('external_labels', {}).items():
        named[lbl_addr] = lbl_addr_str

    # Find subroutines with < 30% comment coverage and > 20 items
    for i, sub in enumerate(subs):
        start = sub['addr']
        end = subs[i+1]['addr'] if i+1 < len(subs) else 0xC000
        sub_items = [it for it in items if start <= it['addr'] < end and it['type'] == 'code']
        commented = [it for it in sub_items if it.get('comment_inline')]
        total = len(sub_items)
        if total < 20:
            continue
        pct = 100*len(commented)/total if total else 0
        if pct >= 30:
            continue

        name = sub.get('name', f'sub_{start:04x}')
        title = sub.get('title', '')

        # Collect callees (JSR/JMP targets)
        callees = set()
        for it in sub_items:
            if it.get('target') and it['mnemonic'] in ('jsr', 'jmp'):
                tgt = it['target']
                if tgt in named:
                    callees.add(named[tgt])

        # Collect workspace refs (operand labels containing 'wksp' or 'fsm' or 'dir')
        wksp_refs = set()
        for it in sub_items:
            # Check if any label in this item references workspace
            for lbl in it.get('labels', []):
                if any(w in lbl for w in ('wksp_', 'fsm_', 'dir_', 'nmi_', 'zp_')):
                    wksp_refs.add(lbl)

        print(f"\n{'='*60}")
        print(f"&{start:04X} {name} ({title})")
        print(f"  {len(commented)}/{total} commented ({pct:.0f}%)")
        if callees:
            print(f"  Calls: {', '.join(sorted(callees)[:10])}")
        if wksp_refs:
            print(f"  Workspace: {', '.join(sorted(wksp_refs)[:10])}")


if __name__ == "__main__":
    main()
