# ADFS 1.30 Comment & Label Review Progress

Systematic review of every subroutine's inline comments and auto-generated
labels. Working bottom-up through the call graph so callees are reviewed
before their callers.

## Statistics

- Total subroutines: 115
- Reviewed: 57 / 115
- Auto-labels renamed: 82 / 940
- comment-check HIGH fixed: 7 / 7
- comment-check MEDIUM fixed: 7 / 50 (remaining 43 are chain_comment style)

## Phase 1: Mechanical Fixes

- [x] Fix 7 HIGH comment-check findings
- [x] Fix stale address and Tube register MEDIUM findings

## Phase 2: Bottom-Up Review

### Depth 0 (42 leaves)

| Addr | Name | Items | Auto Labels | Status |
|------|------|-------|-------------|--------|
| &8027 | claim_tube | 14 | 3 | REVIEWED |
| &8043 | release_tube | 11 | 1 | REVIEWED |
| &8056 | scsi_get_status | 8 | 1 | REVIEWED |
| &8080 | command_set_retries | 4 | 0 | REVIEWED |
| &81EF | tube_start_xfer_sei | 1 | 0 | REVIEWED |
| &8305 | wait_ensuring | 7 | 1 | REVIEWED |
| &8348 | reload_fsm_and_dir_then_brk | 4 | 0 | REVIEWED |
| &8351 | generate_error_no_suffix | 1 | 0 | REVIEWED |
| &843E | hex_digit | 6 | 1 | REVIEWED |
| &8449 | dec_number_error_100_y | 26 | 5 | REVIEWED |
| &84A7 | oscli_at_x | 2 | 0 | REVIEWED |
| &871A | check_char_is_terminator | 10 | 2 | REVIEWED |
| &8B1E | floppy_partial_sector | 14 | 2 | REVIEWED |
| &923E | my_osfile | 46 | 9 | REVIEWED |
| &944F | check_special_dir_char | 18 | 3 | REVIEWED |
| &9501 | print_entry_info | 32 | 7 | REVIEWED |
| &953F | star_dir | 20 | 2 | REVIEWED |
| &9A43 | jmp_indirect_fscv | 1 | 0 | REVIEWED |
| &9A63 | hd_init_detect | 9 | 2 | REVIEWED |
| &9AA3 | service_call_handler | 24 | 2 | REVIEWED |
| &9CDA | service_handler_4 | 40 | 6 | REVIEWED |
| &9E50 | my_fscv | 15 | 3 | REVIEWED |
| &A149 | copy_default_dir_name | 7 | 1 | REVIEWED |
| &A1AA | calc_total_free_space | 13 | 2 | REVIEWED |
| &A444 | star_lib | 12 | 2 | REVIEWED |
| &A460 | switch_to_library | 8 | 1 | REVIEWED |
| &A473 | restore_csd | 6 | 0 | REVIEWED |
| &A497 | star_back | 14 | 2 | REVIEWED |
| &A4CF | skip_spaces | 24 | 5 | REVIEWED |
| &A4F6 | check_drive_colon | 6 | 1 | REVIEWED |
| &A70E | get_wksp_addr_ba | 6 | 0 | REVIEWED |
| &A816 | load_fsm | 3 | 0 | REVIEWED |
| &ACFE | check_set_channel_y | 13 | 2 | REVIEWED |
| &B1B3 | star_close | 2 | 0 | REVIEWED |
| &BB09 | fdc_write_register_verify | 5 | 1 | REVIEWED |
| &BBB4 | floppy_get_step_rate | 19 | 4 | REVIEWED |
| &BBDA | claim_nmi | 6 | 0 | REVIEWED |
| &BBE7 | release_nmi | 4 | 0 | REVIEWED |
| &BBF1 | copy_code_to_nmi_space | 65 | 7 | REVIEWED |
| &BD22 | floppy_set_side_1 | 16 | 3 | REVIEWED |
| &BD4C | apply_head_load_flag | 6 | 1 | REVIEWED |
| &BF55 | floppy_calc_track_sector_from_block_check_range | 26 | 4 | REVIEWED |
| &BFA2 | xa_div_16_to_ya | 8 | 1 | REVIEWED |

### Depth 1 (24 subs)

| Addr | Name | Items | Auto Labels | Status |
|------|------|-------|-------------|--------|
| &8065 | scsi_start_command | 13 | 1 | REVIEWED |
| &830F | scsi_wait_for_req | 7 | 1 | REVIEWED |
| &842D | hex_number_error_100_y | 11 | 2 | REVIEWED |
| &8476 | invalidate_fsm_and_dir | 19 | 3 | REVIEWED |
| &84B5 | release_disc_space | 295 | 46 | |
| &872D | check_filename_length | 14 | 3 | REVIEWED |
| &9471 | parse_dir_argument | 42 | 9 | |
| &94E7 | star_info | 11 | 1 | REVIEWED |
| &993D | star_access | 79 | 14 | |
| &9E7F | star_cmd | 79 | 6 | |
| &A0F5 | parse_drive_argument | 13 | 2 | REVIEWED |
| &A252 | star_title | 16 | 2 | REVIEWED |
| &A47F | star_lcat | 4 | 0 | REVIEWED |
| &A48B | star_lex | 4 | 0 | REVIEWED |
| &A4B7 | skip_filename | 13 | 2 | REVIEWED |
| &A503 | star_rename | 218 | 32 | |
| &A6C7 | check_dir_loaded | 4 | 0 | REVIEWED |
| &A71A | calc_wksp_checksum | 13 | 2 | REVIEWED |
| &A81D | star_copy | 120 | 17 | |
| &A93C | fsc6_new_filing_system | 12 | 1 | REVIEWED |
| &AD16 | compare_ext_to_ptr | 31 | 5 | |
| &B08F | my_osbput | 117 | 16 | |
| &BF86 | floppy_calc_track_sector_from_b0_block | 15 | 2 | |
| &BFAE | floppy_error | 31 | 5 | |

### Depth 2 (12 subs)

| Addr | Name | Items | Auto Labels | Status |
|------|------|-------|-------------|--------|
| &81B8 | hd_data_transfer_256 | 26 | 5 | |
| &8353 | generate_error_suffix_x | 95 | 13 | |
| &9109 | star_remove | 113 | 15 | |
| &9433 | star_ex | 13 | 1 | |
| &A276 | star_compact | 125 | 17 | |
| &A6DE | verify_dir_integrity | 13 | 2 | |
| &A731 | check_wksp_checksum | 116 | 16 | |
| &A955 | my_osargs | 159 | 21 | |
| &AD63 | my_osbget | 330 | 42 | |
| &B57F | my_osgbpb | 524 | 62 | |
| &BB42 | floppy_init_transfer | 53 | 9 | |
| &BCC2 | floppy_wait_nmi_finish | 26 | 3 | |

### Depth 3+ (37 subs)

| Addr | Name | Depth | Items | Auto Labels | Status |
|------|------|-------|-------|-------------|--------|
| &829A | generate_error | 3 | 19 | 2 | |
| &8D21 | check_open | 3 | 451 | 64 | |
| &92A0 | print_inline_string | 3 | 142 | 19 | |
| &9570 | star_cdir | 3 | 416 | 59 | |
| &9AF1 | service_handler_2 | 3 | 42 | 5 | |
| &A0BB | star_delete | 3 | 3 | 0 | |
| &BD3F | floppy_restore_track_0 | 3 | 5 | 0 | |
| &99E6 | star_destroy | 4 | 42 | 6 | |
| &9B41 | service_handler_3 | 4 | 167 | 22 | |
| &9DA7 | help_print_header | 4 | 1 | 0 | |
| &A04A | star_map | 4 | 25 | 3 | |
| &A094 | check_compaction_recommended | 4 | 6 | 0 | |
| &A1C6 | print_space_value | 4 | 8 | 1 | |
| &B1B6 | my_osfind | 4 | 406 | 51 | |
| &BA11 | floppy_check_present | 4 | 115 | 17 | |
| &BD58 | floppy_format_track | 4 | 225 | 28 | |
| &9ACF | service_handler_1 | 5 | 17 | 2 | |
| &9DBE | service_handler_9 | 5 | 69 | 10 | |
| &A01B | star_free | 5 | 16 | 2 | |
| &A111 | star_dismount | 5 | 25 | 3 | |
| &A399 | star_run | 5 | 74 | 10 | |
| &BB14 | do_floppy_scsi_command | 5 | 19 | 2 | |
| &BA00 | do_floppy_scsi_command_ind | 6 | 6 | 1 | |
| &8089 | command_exec_xy | 7 | 49 | 6 | |
| &818A | command_done | 8 | 21 | 3 | |
| &823A | scsi_request_sense | 8 | 40 | 5 | |
| &831B | scsi_send_byte_a | 8 | 21 | 3 | |
| &8753 | compare_filename | 8 | 433 | 57 | |
| &9D19 | service_handler_8 | 8 | 71 | 10 | |
| &A0C3 | star_bye | 8 | 19 | 2 | |
| &A15E | star_mount | 8 | 26 | 3 | |
| &81F0 | tube_start_xfer | 9 | 37 | 6 | |
| &82FB | scsi_send_cmd_byte | 9 | 5 | 1 | |
| &8B41 | hd_command_partial_sector | 9 | 209 | 28 | |
| &80ED | hd_command | 10 | 75 | 11 | |
| &AAC6 | hd_command_bget_bput_sector | 10 | 246 | 33 | |
