# Label Consistency Audit

Check that each subroutine entry label (and internal labels) are
consistent with the subroutine's title and description.

## Status key
- [ ] Not yet reviewed
- [x] Reviewed, name is consistent
- [!] Reviewed, needs renaming (proposed name noted)

## Batch &8000-&83FF: SCSI driver, Tube, command infrastructure (23 subs)

- [x] &8027 `claim_tube` — "Claim Tube if present"
- [x] &8043 `release_tube` — "Release Tube if in use"
- [x] &8056 `scsi_get_status` — "Read SCSI status with settling"
- [x] &8065 `scsi_start_command` — "SCSI bus selection and command phase"
- [x] &8080 `command_set_retries` — "Set retry count for disc operation"
- [x] &8089 `command_exec_xy` — "Execute disc command with control block at (X,Y)"
- [x] &80ED `hd_command` — "Execute hard drive SCSI command"
- [x] &818A `command_done` — "Complete SCSI command and read status"
- [x] &81B8 `hd_data_transfer_256` — "SCSI 256-byte sector data transfer"
- [x] &81EF `tube_start_xfer_sei` — "Start Tube transfer with interrupts disabled"
- [x] &81F0 `tube_start_xfer` — "Start Tube transfer"
- [x] &823A `scsi_request_sense` — "SCSI Request Sense command"
- [x] &8287 `exec_disc_op_from_wksp` — "Execute disc command from workspace control block"
- [x] &828B `exec_disc_command` — "Execute disc command and check for error"
- [x] &829A `generate_error` — "Generate a BRK error"
- [x] &82FB `scsi_send_cmd_byte` — "Send one byte during SCSI command phase"
- [x] &8305 `wait_ensuring` — "Wait while files are being ensured"
- [x] &830F `scsi_wait_for_req` — "Wait for SCSI REQ signal"
- [x] &831B `scsi_send_byte_a` — "Send byte A on SCSI bus after REQ"
- [x] &832B `generate_disc_error` — "Generate disc error with state recovery"
- [x] &8348 `reload_fsm_and_dir_then_brk` — "Reload FSM and directory then raise error"
- [x] &8351 `generate_error_no_suffix` — "Generate error without drive/sector suffix"
- [x] &8353 `generate_error_suffix_x` — "Generate error with suffix control in X"

## Batch &8400-&87FF: FSM management, disc space, filename parsing (22 subs)

- [x] &841C `str_at` — "Error suffix string constants"
- [!] &842D `hex_number_error_100_y` — "Parse hex number or raise error" → `error_append_hex`
- [x] &843E `hex_digit` — "Convert 4-bit value to ASCII hex digit"
- [!] &8449 `dec_number_error_100_y` — "Parse decimal number or raise error" → `error_append_dec`
- [x] &8476 `invalidate_fsm_and_dir` — "Mark FSM and directory as invalid"
- [x] &8499 `str_exec_abbrev` — "OSCLI abbreviation strings"
- [x] &84A0 `osbyte_y_ff_x_00` — "Call OSBYTE to read current value"
- [x] &84A7 `oscli_at_x` — "Execute OSCLI with string at X"
- [x] &84B5 `release_disc_space` — "Release disc space back to free space map"
- [x] &856B `add_size_to_existing_entry` — "Add released size to FSM entry"
- [x] &85C1 `insert_new_entry` — "Insert new entry into FSM"
- [x] &8609 `sum_free_space` — "Sum all free space in FSM"
- [x] &8632 `allocate_disc_space` — "Allocate disc space from free space map"
- [x] &8708 `advance_text_ptr` — "Advance text pointer by one character"
- [x] &870F `parse_and_setup_search` — "Parse argument and set up directory search"
- [x] &871A `check_char_is_terminator` — "Check if character is a filename terminator"
- [x] &872D `check_filename_length` — "Check filename is within 10-character limit"
- [x] &8753 `compare_filename` — "Compare filename against pattern with wildcards"
- [x] &8798 `check_both_exhausted` — "Check pattern and name both exhausted"
- [x] &87A8 `begin_star_match` — "Begin wildcard '*' matching"
- [x] &87CB `star_match_succeeded` — "Return successful wildcard match"
- [x] &87CF `check_name_ended` — "Check name ended during '*' match"

## Batch &8800-&8FFF: Directory operations, entry manipulation (34 subs)

- [x] &880C `disc_op_tpl_read_fsm` — "Disc operation templates for FSM and directory reads"
- [x] &8822 `parse_drive_from_ascii` — "Parse drive number from ASCII character"
- [x] &8849 `bad_drive_name` — "Raise Bad name error for invalid drive"
- [x] &884C `parse_filename_from_cmdline` — "Parse filename from command line"
- [x] &8905 `save_text_ptr_after_match` — "Save text pointer and determine object type"
- [x] &895E `advance_dir_entry_ptr` — "Advance to next matching directory entry"
- [x] &89D0 `get_object_type_result` — "Load object type and save workspace"
- [x] &89D3 `save_wksp_and_return` — "Save workspace state and return result"
- [x] &8A3D `multi_sector_disc_command` — "Execute multi-sector disc command"
- [x] &8A45 `check_disc_command_type` — "Check command type and adjust sector count"
- [!] &8A63 `adjust_for_partial_xfer` — "Execute disc transfer in batches" → `exec_disc_transfer_batched`
- [x] &8B1E `floppy_partial_sector` — "Floppy disc partial sector transfer"
- [x] &8B41 `hd_command_partial_sector` — "Hard drive partial sector transfer"
- [!] &8BB3 `exec_disc_and_check_error` — "Search for non-directory file" → `search_for_file`
- [x] &8BC8 `not_found_error` — "Generate Not found error"
- [x] &8C05 `osfile_save_check_existing` — "OSFILE A=0: check for existing file before save"
- [x] &8C62 `search_dir_for_file` — "Search directory for matching file"
- [x] &8CC3 `check_existing_for_save` — "Check for existing file before save"
- [!] &8CC9 `setup_disc_write` — "Parse filename from OSFILE block and search" → `parse_osfile_and_search`
- [x] &8D10 `check_file_not_open` — "Check file is not locked or open"
- [x] &8D21 `check_open` — "Check if file is open"
- [x] &8D69 `no_open_files_on_drive` — "No open file conflict found"
- [x] &8D6E `set_up_directory_search` — "Validate path and check for wildcards"
- [!] &8DD6 `parse_and_search_dir` — "Check next path character is terminator" → `check_path_terminator`
- [!] &8DDE `mark_saved_drive_unset` — "Raise Wild cards error" → `wild_cards_error`
- [x] &8DED `tbl_forbidden_chars` — "Forbidden filename characters"
- [!] &8DF3 `check_file_not_open2` — "Copy OSFILE addresses and search for empty entry" → `copy_addrs_and_find_empty_entry`
- [x] &8E6F `allocate_disc_space_for_file` — "Allocate disc space and store in entry"
- [x] &8E8B `copy_entry_from_template` — "Copy OSFILE template into directory entry"
- [x] &8F4C `validate_not_locked` — "Validate file is not locked then create entry"
- [x] &8F86 `write_dir_and_validate` — "Write directory and FSM back to disc"
- [x] &8FDF `find_first_matching_entry` — "Find first matching directory entry"
- [!] &8FEA `mark_directory_dirty` — "Validate FSM checksums and mark directory dirty" → `validate_fsm_and_mark_dirty`
- [!] &8FFA `check_first_char_wildcard` — "Raise Bad FS map error" → `bad_fs_map_error`

## Batch &9000-&95FF: Catalogue, path resolution, star commands (24 subs)

- [x] &905C `calc_fsm_checksums` — "Calculate FSM sector checksums"
- [x] &9071 `disc_op_tpl_write_fsm_unused` — "Unused write-FSM disc operation template"
- [x] &907C `osfile_write_load_addr` — "OSFILE write catalogue info handler"
- [x] &9109 `star_remove` — "*REMOVE command handler"
- [x] &9128 `check_and_delete_found` — "Validate and delete a directory entry"
- [!] &923E `my_osfile` — "OSFILE handler" → `osfile_handler`
- [x] &9269 `osfile_dispatch_lo` — "OSFILE dispatch table"
- [!] &927B `setup_entry_name_ptr` — "Set up entry name pointer for star commands" → `setup_help_param_ptr`
- [x] &92A0 `print_inline_string` — "Print bit-7-terminated inline string"
- [x] &92C4 `print_via_osasci` — "Print character preserving registers"
- [x] &92DE `print_entry_name_and_access` — "Print entry name and access string"
- [!] &9316 `l9316` — "Access attribute character table" → `tbl_access_chars`
- [x] &931B `print_hex_byte` — "Print a byte as two hex digits"
- [x] &932A `verify_dir_and_list` — "Verify directory and print catalogue header"
- [x] &9433 `star_ex` — "*EX command handler"
- [x] &944F `check_special_dir_char` — "Check for ^ (parent) or @ (current) directory"
- [x] &9471 `parse_dir_argument` — "Parse optional directory path argument"
- [x] &947F `parse_path_and_load` — "Parse path and load target directory"
- [x] &94CC `dummy_root_dir_entry` — "Dummy directory entry for root directory '$'"
- [x] &94E7 `star_info` — "*INFO command handler"
- [x] &94FA `conditional_info_display` — "Display file info if *OPT1 verbose"
- [x] &9501 `print_entry_info` — "Print full catalogue info for one directory entry"
- [x] &953F `star_dir` — "*DIR command handler"
- [x] &9570 `star_cdir` — "*CDIR command handler"

## Batch &9600-&9BFF: Star commands, service calls, init (16 subs)

- [x] &9632 `osfile_tpl_cdir` — "OSFILE control block template for *CDIR"
- [x] &97A8 `format_init_dir` — "Initialise directory structure for format"
- [x] &993D `star_access` — "*ACCESS command handler"
- [x] &9945 `clear_rwl_attributes` — "Clear R, W, L attribute bits in entry"
- [x] &9951 `set_file_attributes` — "Set file attributes from access string"
- [x] &99E6 `star_destroy` — "*DESTROY command handler"
- [x] &9A43 `jmp_indirect_fscv` — "Jump through FSCV indirect vector"
- [x] &9A46 `default_workspace_data` — "Default workspace initialisation template"
- [x] &9A63 `hd_init_detect` — "Detect hard drive hardware"
- [x] &9A78 `boot_option_addr_table` — "Boot option OSCLI address table and command strings"
- [x] &9A8F `service_dispatch_lo` — "Service call dispatch table"
- [x] &9AA3 `service_call_handler` — "ROM service call handler"
- [x] &9ACF `service_handler_1` — "Service 1: absolute workspace claim"
- [x] &9AE6 `adfs_hardware_found` — "Claim workspace for ADFS"
- [x] &9AF1 `service_handler_2` — "Service 2: private workspace claim"
- [x] &9B41 `service_handler_3` — "Service 3: auto-boot"

## Batch &9C00-&9FFF: MOS interface, command dispatch (17 subs)

- [x] &9CB3 `tbl_fs_vectors` — "Filing system vector addresses"
- [x] &9CC1 `tbl_extended_vectors` — "Extended vector table"
- [x] &9CD6 `str_filing_system_name` — "Filing system name string"
- [x] &9CDA `service_handler_4` — "Service 4: unrecognised star command"
- [!] &9D11 `service4_claim_and_dispatch` — "Decline service 4 and pass on" → `service4_decline`
- [x] &9D19 `service_handler_8` — "Service 8: unrecognised OSWORD"
- [x] &9DA7 `help_print_header` — "Print *HELP version header line"
- [x] &9DBE `service_handler_9` — "Service 9: *HELP"
- [x] &9DDA `print_help_command_list` — "Print *HELP ADFS command list"
- [x] &9E48 `tbl_help_param_ptrs` — "*HELP parameter format string pointer table"
- [!] &9E50 `my_fscv` — "Filing system control vector handler" → `fscv_handler`
- [x] &9E6D `fscv_dispatch_lo` — "FSCV dispatch table"
- [x] &9E7F `star_cmd` — "Parse and dispatch star command"
- [x] &9EE3 `tbl_commands` — "Star command name and dispatch table"
- [x] &9F8D `help_param_list_spec` — "*HELP parameter format strings"
- [x] &9FD8 `fsc7_read_handle_range` — "FSC 7: return ADFS file handle range"
- [x] &9FDD `fsc0_star_opt` — "FSC 0: *OPT command handler"

## Batch &A000-&A4FF: *FREE, *COMPACT, utilities, string handling (29 subs)

- [!] &A016 `ca016` — "Print a space character" → `print_space`
- [x] &A01B `star_free` — "*FREE command handler"
- [x] &A04A `star_map` — "*MAP command handler"
- [x] &A094 `check_compaction_recommended` — "Check if disc compaction is recommended"
- [x] &A0BB `star_delete` — "*DELETE command handler"
- [x] &A0C3 `star_bye` — "*BYE command handler"
- [x] &A0EA `scsi_cmd_park` — "SCSI park heads disc operation control block"
- [x] &A0F5 `parse_drive_argument` — "Parse optional drive number argument"
- [x] &A111 `star_dismount` — "*DISMOUNT command handler"
- [x] &A149 `copy_default_dir_name` — "Copy default directory name to workspace"
- [x] &A15E `star_mount` — "*MOUNT command handler"
- [x] &A19F `scsi_cmd_unpark` — "SCSI unpark heads disc operation control block"
- [x] &A1AA `calc_total_free_space` — "Calculate total free space on disc"
- [x] &A1C6 `print_space_value` — "Print space value in hex and decimal"
- [x] &A252 `star_title` — "*TITLE command handler"
- [x] &A276 `star_compact` — "*COMPACT command handler"
- [x] &A29B `bad_compact_error` — "Raise Bad compact error"
- [x] &A35A `combine_hex_digit_pair` — "Combine two hex nibbles into a byte"
- [x] &A365 `parse_second_filename` — "Parse second filename from command line"
- [x] &A399 `star_run` — "*RUN command handler"
- [x] &A444 `star_lib` — "*LIB command handler"
- [x] &A460 `switch_to_library` — "Switch CSD to library directory"
- [x] &A473 `restore_csd` — "Restore CSD sector from saved copy"
- [x] &A47F `star_lcat` — "*LCAT command handler"
- [x] &A48B `star_lex` — "*LEX command handler"
- [x] &A497 `star_back` — "*BACK command handler"
- [x] &A4B7 `skip_filename` — "Skip past filename in command string"
- [x] &A4CF `skip_spaces` — "Skip leading spaces in command argument"
- [x] &A4F6 `check_drive_colon` — "Check for drive specifier colon"

## Batch &A500-&A9FF: Workspace management, OSARGS, channel mgmt (16 subs)

- [x] &A503 `star_rename` — "*RENAME command handler"
- [x] &A6C7 `check_dir_loaded` — "Ensure current directory is loaded"
- [x] &A6DE `verify_dir_integrity` — "Verify directory buffer integrity"
- [x] &A6F9 `broken_directory_error` — "Raise Broken directory error"
- [x] &A70E `get_wksp_addr_ba` — "Get workspace address into &BA"
- [x] &A71A `calc_wksp_checksum` — "Calculate workspace checksum"
- [x] &A72B `store_wksp_checksum_ba_y` — "Calculate and store workspace checksum"
- [x] &A731 `check_wksp_checksum` — "Verify workspace checksum"
- [x] &A749 `save_workspace_state` — "Save all registers and workspace"
- [x] &A7A2 `load_dir_for_drive` — "Restore workspace and load directory"
- [x] &A7C0 `setup_disc_read_for_dir` — "Set up disc read for directory load"
- [x] &A816 `load_fsm` — "Load free space map from disc"
- [x] &A81D `star_copy` — "*COPY command handler"
- [x] &A93C `fsc6_new_filing_system` — "FSC 6: new filing system selected"
- [!] &A955 `my_osargs` — "OSARGS handler" → `osargs_handler`
- [x] &A97C `flush_all_channels` — "Flush all open channel buffers"

## Batch &AA00-&AFFF: Buffer management, BGET, sector I/O (15 subs)

- [x] &AAA6 `validate_and_set_ptr` — "Flush buffers and set file pointer"
- [x] &AAC6 `hd_command_bget_bput_sector` — "Hard drive single sector for BGET/BPUT"
- [!] &AB63 `wait_write_data_phase` — "Write 256 bytes to SCSI bus" → `scsi_write_page`
- [x] &ABD8 `find_buffer_for_sector` — "Find or allocate a buffer for a sector"
- [x] &AC62 `read_single_hd_sector` — "Read a single sector via SCSI"
- [x] &ACD7 `calc_buffer_page_from_offset` — "Calculate buffer page from channel offset"
- [x] &ACE9 `step_ensure_offset_loop` — "Step through ensure table entries"
- [x] &ACFE `check_set_channel_y` — "Validate and set channel number from Y"
- [x] &AD16 `compare_ext_to_ptr` — "Compare file EXT to PTR"
- [x] &AD53 `eof_error` — "Raise EOF error"
- [!] &AD63 `my_osbget` — "OSBGET handler" → `osbget_handler`
- [x] &AD8D `calc_bget_sector_addr` — "Calculate sector address for BGET"
- [x] &ADC5 `switch_to_channel_drive` — "Switch to channel's drive for I/O"
- [x] &AE4C `advance_to_next_dir_entry` — "Advance directory scan pointer"
- [x] &AEBC `update_ext_to_ptr` — "Handle PTR exceeding EXT"

## Batch &B000-&B5FF: BPUT, OSGBPB, OSFIND, drive selection (13 subs)

- [x] &B060 `update_ext_from_new_ptr` — "Update EXT from new PTR value"
- [!] &B08F `my_osbput` — "OSBPUT handler" → `osbput_handler`
- [x] &B123 `increment_ptr_after_write` — "Increment PTR after byte write"
- [x] &B18C `sync_ext_to_ptr` — "Synchronise EXT to PTR if at EOF"
- [x] &B1B3 `star_close` — "*CLOSE command handler"
- [!] &B1B6 `my_osfind` — "OSFIND handler" → `osfind_handler`
- [x] &B24D `next_conflict_check` — "Continue open-channel conflict scan"
- [x] &B3F1 `update_dir_entry_on_close` — "Update directory entry on file close"
- [x] &B4F5 `check_drive_and_reload_fsm` — "Check disc changed and reload FSM if needed"
- [x] &B510 `get_drive_bit_mask` — "Get bit mask for drive slot"
- [x] &B51C `set_drive_from_channel` — "Set current drive from channel's drive"
- [x] &B579 `convert_drive_to_slot` — "Convert drive number to slot index"
- [!] &B57F `my_osgbpb` — "OSGBPB handler" → `osgbpb_handler`

## Batch &B600-&BFFF: Floppy driver, NMI handler, format, utilities (34 subs)

- [x] &B825 `setup_osgbpb_output_buffer` — "Set up OSGBPB output buffer"
- [x] &B85B `output_byte_to_buffer` — "Output byte to Tube or host buffer"
- [x] &B872 `output_dir_entry_name` — "Output 10-byte directory entry name"
- [x] &B980 `transfer_sector_bytes` — "Transfer sector bytes between buffer and memory"
- [x] &BA00 `do_floppy_scsi_command_ind` — "Floppy disc command (indirect entry)"
- [x] &BA11 `floppy_check_present` — "Check floppy disc hardware present"
- [!] &BAC6 `process_floppy_result` — "Set up FDC registers and seek to track" → `setup_fdc_and_seek`
- [x] &BAF4 `retry_after_error` — "Set up track for floppy retry"
- [x] &BB09 `fdc_write_register_verify` — "Write to WD1770 register with readback verify"
- [x] &BB14 `do_floppy_scsi_command` — "Execute floppy disc command"
- [x] &BB42 `floppy_init_transfer` — "Initialise floppy disc transfer"
- [x] &BB82 `set_read_transfer_mode` — "Set read mode and initialise floppy"
- [x] &BB92 `claim_nmi_and_init` — "Claim NMI and initialise floppy transfer"
- [x] &BBB4 `floppy_get_step_rate` — "Get floppy step rate"
- [x] &BBDA `claim_nmi` — "Claim NMI via service call 12"
- [x] &BBE7 `release_nmi` — "Release NMI via service call 11"
- [x] &BBF1 `copy_code_to_nmi_space` — "Copy NMI handler code to NMI workspace"
- [x] &BC79 `nmi_code_start` — "NMI handler code (copied to &0D00)"
- [x] &BC93 `nmi_check_status_error` — "NMI status/error handler"
- [x] &BCA5 `nmi_check_end_of_operation` — "NMI end-of-operation handler"
- [x] &BCC2 `floppy_wait_nmi_finish` — "Wait for floppy NMI transfer to complete"
- [x] &BCFD `select_fdc_rw_command` — "Select and issue FDC read/write command"
- [x] &BD19 `floppy_set_side_0_unused` — "Unused: select floppy disc side 0"
- [x] &BD22 `floppy_set_side_1` — "Select floppy disc side 1"
- [x] &BD2B `clear_transfer_complete` — "Clear floppy transfer complete flag"
- [x] &BD38 `clear_seek_flag` — "Clear floppy seek-in-progress flag"
- [x] &BD3F `floppy_restore_track_0` — "Seek floppy head to track 0"
- [x] &BD4C `apply_head_load_flag` — "Apply head load delay to FDC command"
- [x] &BD58 `floppy_format_track` — "Format a floppy disc track"
- [x] &BF55 `floppy_calc_track_sector_from_block_check_range` — "Calculate track/sector from block with range check"
- [x] &BF86 `floppy_calc_track_sector_from_b0_block` — "Calculate track/sector from block at &B0"
- [x] &BFA2 `xa_div_16_to_ya` — "Divide X:A by 16, result in Y:A"
- [x] &BFAE `floppy_error` — "Handle floppy disc error"
- [x] &BFF6 `str_rom_footer` — "ROM footer text"
