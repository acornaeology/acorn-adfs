# Auto-Generated Label Rename Progress

Tracking renaming of ~150 auto-generated `lXXXX` labels to semantic names.

## Statistics
- Total: ~150
- Renamed: 0
- Remaining: ~150

## Zero page (&00-&FF): 8 labels
- [ ] l0000-l0003: used as (zp),X indexed — OSARGS zero page pointer
- [ ] l00ef-l00f1: MOS workspace
- [ ] l00ff: Escape flag

## Stack page (&100-&1FF): 5 labels
- [ ] l0100-l0104: error block construction on stack page

## System (&400, &600): 2 labels
- [ ] l0406: Tube host entry point
- [ ] l06a9: IRQ workspace

## NMI workspace (&D00): 1 label
- [ ] l0d18: NMI handler continuation address

## FSM (&E00): 1 label
- [ ] l0e03: FSM sector 0 offset

## Workspace page 1 (&1000-&10FF): 111 labels
- [ ] Disc op block fields (&1015-&1024)
- [ ] Workspace variables (&1024-&10FF)

## Workspace page 2 (&1100-&11FF): 21 labels
- [ ] CSD/lib info (&1114-&111F)
- [ ] Per-channel tables (&1183-&11F2)

## Other: 1 label
- [ ] lffff: self-modifying code target
