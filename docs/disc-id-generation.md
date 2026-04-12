# Disc ID Generation in ADFS 1.30

## Overview

ADFS 1.30 maintains a 16-bit disc identifier in the free space map (FSM) as a
lightweight mechanism for detecting disc changes. The identifier is not a
permanent serial number assigned during formatting -- its low byte is
deliberately changed on every directory/FSM flush, so that swapping a floppy
disc between operations will almost certainly produce a detectable mismatch.

## Storage

The disc ID occupies two bytes in each of the two FSM sectors:

| FSM sector | RAM address | Offset within sector |
|------------|-------------|---------------------|
| Sector 0   | `fsm_s0_disc_id_lo` (&0EFB) | &FB |
| Sector 0   | `fsm_s0_disc_id_hi` (&0EFC) | &FC |
| Sector 1   | `fsm_s1_disc_id_lo` (&0FFB) | &FB |
| Sector 1   | `fsm_s1_disc_id_hi` (&0FFC) | &FC |

Only the sector 1 copy is actively read and written by the flush and
disc-change logic. The sector 0 copy is included in the sector 0 checksum but
is not explicitly updated by `write_dir_and_validate`.

Per-drive cached copies are held in workspace at `wksp_disc_id_lo` (&1121) and
`wksp_disc_id_hi` (&1122), indexed by drive slot.

## When the disc ID is updated

The disc ID is updated inside `write_dir_and_validate` (&8F86), which is the
common path for flushing the current directory and FSM back to disc. This
routine is called from 17 sites across the ROM -- after file creation,
deletion, renaming, attribute changes, compaction, and format initialisation.
Any operation that modifies the directory or free space map will trigger a disc
ID update.

## How the disc ID is generated

After writing the directory sectors to disc, `write_dir_and_validate` updates
the disc ID in two steps:

### High byte: preserved

The existing high byte is read from `fsm_s1_disc_id_hi` (&0FFC) and cached
into per-drive workspace, but it is never overwritten with a new value. It
retains whatever was written when the disc was formatted or when the FSM was
last written by another code path.

```
lda fsm_s1_disc_id_hi       ; &8FB7 -- read existing high byte
sta wksp_disc_id_hi,x       ; &8FBA -- cache in per-drive workspace
```

### Low byte: sampled from the VIA timer

The low byte is replaced with the current value of the System VIA Timer 1
counter low byte, read from `system_via_t1c_l` (&FE44):

```
lda system_via_t1c_l         ; &8FBD -- read T1 counter low byte
sta wksp_disc_id_lo,x       ; &8FC0 -- cache in per-drive workspace
sta fsm_s1_disc_id_lo       ; &8FC3 -- write to FSM sector 1
```

Timer 1 on the BBC Micro's System VIA free-runs at 1 MHz, cycling through its
full 16-bit range roughly 15 times per second. The low byte alone cycles
through all 256 values every 256 microseconds. Because the exact moment of the
flush depends on the user's actions and the preceding code path, the value read
is effectively unpredictable -- pseudo-random from the user's perspective,
though entirely deterministic given the hardware state.

### FSM checksum recalculation

After updating the disc ID, the routine recalculates both FSM sector checksums
via `calc_fsm_checksums` (&905C) and writes the FSM to disc using the
`disc_op_tpl_write_fsm` template at &9071:

```
jsr calc_fsm_checksums       ; &8FC6 -- recalculate checksums
stx fsm_s0_checksum         ; &8FC9 -- store sector 0 checksum
sta fsm_s1_checksum         ; &8FCC -- store sector 1 checksum
ldx #&71                     ; &8FCF -- point to write-FSM template
ldy #&90
jsr exec_disc_command        ; &8FD3 -- write both FSM sectors
```

## Disc change detection

The disc ID serves as the primary mechanism for detecting floppy disc swaps.
The detection logic lives in `check_disc_changed` (&B47C) and its companion
entry point `read_clock_then_verify_disc_id` (&B48E).

### Two entry points

The disc-change check has two entry points depending on whether any file
channels are currently open on the drive:

**No channels open** -- entry via `check_disc_changed` (&B47C): the current
disc ID is read from the FSM and cached in per-drive workspace. This
establishes a baseline for comparison. Execution then falls through to read the
clock and verify.

**Channels open** -- entry via `read_clock_then_verify_disc_id` (&B48E): the
workspace already holds the disc ID from when the channel was opened or last
verified. The code skips the caching step and proceeds directly to timing and
comparison.

### Timing check

Both paths call `read_clock_for_timing` (&B4BF), which reads the system clock
via OSWORD 1 and computes elapsed time since the previous reading. If fewer
than 2 centiseconds have elapsed, the disc is assumed unchanged -- there has
not been enough time for the user to physically swap a floppy. This
short-circuit avoids unnecessary disc I/O on rapid successive checks.

### ID comparison

After the timing check, `verify_disc_id_unchanged` (&B491) re-reads both disc
ID bytes from the FSM and compares them against the cached workspace values:

```
lda fsm_s1_disc_id_lo       ; &B497 -- re-read low byte
cmp wksp_disc_id_lo,x       ; &B49A -- compare with cached
bne raise_disc_changed_error ; &B49D -- mismatch

lda fsm_s1_disc_id_hi       ; &B49F -- re-read high byte
cmp wksp_disc_id_hi,x       ; &B4A2 -- compare with cached
bne raise_disc_changed_error ; &B4A5 -- mismatch
```

If either byte differs, `raise_disc_changed_error` (&B4AE) reloads the FSM and
directory from the new disc, then raises error &C8 ("Disc changed").

## Design observations

The scheme is simple but effective for single-user floppy operation:

- **Low byte churn**: because the low byte changes on every flush, two
  different discs will almost certainly have different disc IDs even if they
  were formatted identically. The probability of a false negative (two discs
  having the same 16-bit ID) is roughly 1 in 65,536 per check.

- **High byte stability**: the high byte provides continuity across operations
  on the same disc. Two consecutive flushes to the same disc will differ only
  in the low byte, which is expected -- the comparison is between the cached
  workspace copy and a fresh FSM read, not between two consecutive flushes.

- **Sector 0 vs sector 1**: only the sector 1 copy is actively maintained.
  The sector 0 copy at &0EFB/&0EFC participates in the sector 0 checksum but
  is not updated by `write_dir_and_validate`. This asymmetry may reflect the
  fact that the disc-change logic only needs one authoritative copy, and sector
  1 was chosen.

- **No format-time initialisation**: the disc ID is not specially initialised
  during `*FORMAT`. The format path calls `write_dir_and_validate`, which
  applies the same timer-based update. A freshly formatted disc simply gets
  whatever timer value was current at the moment of the final FSM flush.
