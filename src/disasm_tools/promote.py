"""Find labels that should be promoted to entry points or subroutines.

Analyzes all labeled code items and scores them based on:
  - Whether preceded by a terminal instruction (RTS, JMP, BRK)
  - In-degree (number of references from other instructions)
  - Come-from distance (how far away the referencing code is)
  - Whether referenced by JSR (call) vs branch (local)

Higher scores indicate stronger candidates for promotion to entry()
or subroutine() declarations, which add visual separator blocks to
the assembly output.
"""

import json
import sys
from pathlib import Path

# Mnemonics that unconditionally terminate control flow
TERMINAL_MNEMONICS = {"rts", "jmp", "brk", "rti"}

# Call mnemonics (as opposed to branches)
CALL_MNEMONICS = {"jsr", "jmp"}


def analyze_labels(json_filepath):
    """Analyze all labeled code items for promotion candidacy.

    Returns a list of dicts sorted by score (descending), each with:
      addr, name, score, refs, jsr_refs, max_distance, mean_distance,
      after_terminal, is_entry, is_subroutine
    """
    data = json.load(open(json_filepath))
    items = data["items"]
    sub_addrs = {s["addr"] for s in data["subroutines"]}

    # Build address-to-item index
    addr_map = {i["addr"]: i for i in items}

    # Build list of all code items sorted by address
    code_items = sorted(
        [i for i in items if i["type"] == "code"],
        key=lambda i: i["addr"],
    )

    # Build predecessor map: for each address, what is the previous code item?
    prev_map = {}
    for i in range(1, len(code_items)):
        prev_map[code_items[i]["addr"]] = code_items[i - 1]

    # Build set of addresses that have data items between them and their
    # predecessor code item. If data separates two code regions, there
    # is no fall-through path regardless of the predecessor's mnemonic.
    data_separated = set()
    all_items_sorted = sorted(items, key=lambda i: i["addr"])
    for i, item in enumerate(all_items_sorted):
        if item["type"] != "code" or not item.get("labels"):
            continue
        # Walk backwards from this item to find data between it and prev code
        for j in range(i - 1, max(i - 20, -1), -1):
            prev_item = all_items_sorted[j]
            if prev_item["type"] == "code":
                break  # reached previous code with no data gap
            if prev_item["type"] in ("byte", "string", "word"):
                data_separated.add(item["addr"])
                break

    # Collect entry() addresses from the JSON (items with comments_before
    # containing the reference line indicate entry points)
    entry_addrs = set()
    for item in items:
        if item.get("comments_before"):
            for cb in item["comments_before"]:
                if cb.startswith("*****"):
                    entry_addrs.add(item["addr"])
                    break

    # Build reference index: for each target address, collect source addrs
    ref_sources = {}
    for item in code_items:
        target = item.get("target")
        if target and target != item["addr"]:
            ref_sources.setdefault(target, []).append(item)

    # Analyze each labeled code item
    candidates = []
    for item in code_items:
        labels = item.get("labels", [])
        if not labels:
            continue

        addr = item["addr"]
        name = labels[0]

        # Skip items that are already subroutines
        is_subroutine = addr in sub_addrs
        is_entry = addr in entry_addrs

        # Check if preceded by terminal instruction OR separated by data
        prev = prev_map.get(addr)
        after_terminal = (
            addr in data_separated
            or prev is not None and prev.get("mnemonic") in TERMINAL_MNEMONICS
        )

        # Count references by type
        sources = ref_sources.get(addr, [])
        # Also check the 'references' field on the item itself (from py8dis)
        refs_from_json = item.get("references", [])

        jsr_refs = sum(
            1 for s in sources if s.get("mnemonic") in CALL_MNEMONICS
        )
        branch_refs = len(sources) - jsr_refs
        total_refs = len(sources)

        # Also count references from the JSON references field that
        # may not appear in our source scan (e.g. data table references)
        extra_refs = len(refs_from_json) - total_refs
        if extra_refs > 0:
            total_refs += extra_refs

        # Compute come-from distances
        distances = [abs(s["addr"] - addr) for s in sources]
        if refs_from_json:
            distances.extend(abs(r - addr) for r in refs_from_json)
        distances = sorted(set(distances))  # deduplicate

        max_distance = max(distances) if distances else 0
        mean_distance = (
            sum(distances) / len(distances) if distances else 0
        )

        # Score: weighted combination of signals
        score = 0.0

        # Definite promotion: after terminal + multiple references
        # is conclusive evidence of a standalone routine. Any code
        # unreachable by fall-through that is independently called
        # from 3+ sites (or 2+ with a JSR) is a routine, period.
        if after_terminal and (total_refs >= 3 or
                               (total_refs >= 2 and jsr_refs >= 1)):
            score += 50

        # After terminal instruction: strong signal
        if after_terminal:
            score += 20

        # References: each ref adds points
        score += total_refs * 3

        # JSR references worth more than branch references
        score += jsr_refs * 5

        # Come-from distance: continuous scaling rather than
        # coarse thresholds. Each 256 bytes of max distance
        # adds 1 point, capped at 20.
        score += min(20, max_distance // 0x100)

        # Mean distance bonus: each 256 bytes adds 0.5 points
        score += min(10, mean_distance // 0x200)

        candidates.append({
            "addr": addr,
            "name": name,
            "score": score,
            "total_refs": total_refs,
            "jsr_refs": jsr_refs,
            "branch_refs": branch_refs,
            "max_distance": max_distance,
            "mean_distance": int(mean_distance),
            "after_terminal": after_terminal,
            "is_entry": is_entry,
            "is_subroutine": is_subroutine,
        })

    # Sort by score descending
    candidates.sort(key=lambda c: (-c["score"], c["addr"]))
    return candidates


def format_promote_report(candidates, threshold=25, show_all=False,
                          not_entry_only=False):
    """Print the promotion report."""
    filtered = candidates
    if not show_all:
        filtered = [c for c in candidates if c["score"] >= threshold]
    if not_entry_only:
        filtered = [c for c in filtered
                    if not c["is_entry"] and not c["is_subroutine"]]

    print(f"{'ADDR':>6} {'SCORE':>5} {'REFS':>4} {'JSR':>3} "
          f"{'MAX_DIST':>8} {'MEAN':>6} "
          f"{'TERM':>4} {'ENT':>3} {'SUB':>3}  NAME")
    print(f"{'─'*6} {'─'*5} {'─'*4} {'─'*3} "
          f"{'─'*8} {'─'*6} "
          f"{'─'*4} {'─'*3} {'─'*3}  {'─'*30}")

    for c in filtered:
        term = "Y" if c["after_terminal"] else ""
        ent = "Y" if c["is_entry"] else ""
        sub = "Y" if c["is_subroutine"] else ""
        max_d = f"&{c['max_distance']:04X}" if c["max_distance"] else ""
        mean_d = f"&{c['mean_distance']:04X}" if c["mean_distance"] else ""
        print(f"&{c['addr']:04X} {c['score']:>5.0f} {c['total_refs']:>4} "
              f"{c['jsr_refs']:>3} {max_d:>8} {mean_d:>6} "
              f"{term:>4} {ent:>3} {sub:>3}  {c['name']}")

    # Summary
    total = len(filtered)
    new_entries = sum(
        1 for c in filtered
        if not c["is_entry"] and not c["is_subroutine"]
    )
    print(f"\n{total} candidates shown (threshold={threshold})")
    if new_entries:
        print(f"{new_entries} not yet declared as entry/subroutine")


def promote(version_dirpath, version, threshold=25, show_all=False,
            not_entry_only=False):
    """Main entry point. Returns exit code 0."""
    from disasm_tools.paths import rom_prefix
    pfx = rom_prefix(version_dirpath)
    json_filepath = version_dirpath / "output" / f"{pfx}-{version}.json"

    if not json_filepath.exists():
        print(f"Error: {json_filepath} not found (run disassemble first)",
              file=sys.stderr)
        return 1

    candidates = analyze_labels(json_filepath)
    format_promote_report(candidates, threshold=threshold,
                          show_all=show_all,
                          not_entry_only=not_entry_only)
    return 0
