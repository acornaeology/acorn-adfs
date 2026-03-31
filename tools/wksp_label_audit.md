# Workspace Label Audit Tracker

Tracks progress on renaming hex-address workspace labels in the ADFS 1.30 disassembly.

## Status Key
- [ ] Not started
- [~] Analysed, needs discussion
- [x] Renamed and committed

## Page 1 (&1000-&10FF) — Hex-address labels

- [x] wksp_1001 (&1001) → wksp_buf_sec_lo — per-channel buffer sector addr low
- [x] wksp_1002 (&1002) → wksp_buf_sec_mid — per-channel buffer sector addr mid
- [x] wksp_1003 (&1003) → wksp_buf_sec_hi — per-channel buffer sector addr high + drive
- [x] wksp_1004 (&1004) → wksp_buf_flag — per-channel buffer state/dirty flags
- [x] wksp_1008 (&1008) → wksp_buf_flag_1 — buffer flag slot 1 (init alias)
- [x] wksp_100c (&100C) → wksp_buf_flag_2 — buffer flag slot 2 (init alias)
- [x] wksp_100d (&100D) → wksp_entry_field_base — Y-indexed base for entry fields
- [x] wksp_100e (&100E) → wksp_entry_len_base — Y-indexed base for entry lengths
- [x] wksp_1011 (&1011) → wksp_entry_calc_base — Y-indexed base for sequence calc
- [x] wksp_1014 (&1014) → wksp_disc_op_block — disc op block base / buffer flag 4
- [x] wksp_1024 (&1024) → wksp_entry_size_base — Y-indexed base for object size

## Page 2 (&1100-&11FF) — Hex-address labels

- [x] wksp_1121 (&1121) → wksp_disc_id_lo — per-drive disc ID low
- [x] wksp_1122 (&1122) → wksp_disc_id_hi — per-drive disc ID high
- [x] wksp_1131 (&1131) → wksp_scsi_status — SCSI combined status byte
- [x] wksp_1132 (&1132) → wksp_exec_handle — stored EXEC file handle

## Named labels to review

- [x] wksp_shadow_save (&10D7) → wksp_cmd_tail_hi — command tail pointer high byte
