# Subroutine Calling Convention Audit

Track progress adding on_entry/on_exit to subroutine() calls.

## Status key
- [ ] Not started
- [x] Done
- [~] Skipped (N/A: error handler, data table, etc.)

## Batch &8000-&83FF: SCSI driver, Tube, command infrastructure (23 subs)

- [ ] &8027 claim_tube
- [ ] &8043 release_tube
- [ ] &8056 scsi_get_status
- [ ] &8065 scsi_start_command
- [ ] &8080 command_set_retries
- [ ] &8089 command_exec_xy
- [ ] &80ED hd_command
- [ ] &818A command_done
- [ ] &81B8 hd_data_transfer_256
- [ ] &81EF tube_start_xfer_sei
- [ ] &81F0 tube_start_xfer
- [ ] &823A scsi_request_sense
- [ ] &8287 exec_disc_op_from_wksp
- [ ] &828B exec_disc_command
- [ ] &829A generate_error
- [ ] &82FB scsi_send_cmd_byte
- [ ] &8305 wait_ensuring
- [ ] &830F scsi_wait_for_req
- [ ] &831B scsi_send_byte_a
- [ ] &832B generate_disc_error
- [ ] &8348 reload_fsm_and_dir_then_brk
- [ ] &8351 generate_error_no_suffix
- [ ] &8353 generate_error_suffix_x

## Batch &8400-&87FF: FSM management, disc space, filename parsing (22 subs)

- [ ] &841C str_at
- [ ] &842D hex_number_error_100_y
- [ ] &843E hex_digit
- [ ] &8449 dec_number_error_100_y
- [ ] &8476 invalidate_fsm_and_dir
- [ ] &8499 str_exec_abbrev
- [ ] &84A0 osbyte_y_ff_x_00
- [ ] &84A7 oscli_at_x
- [ ] &84B5 release_disc_space
- [ ] &856B add_size_to_existing_entry
- [ ] &85C1 insert_new_entry
- [ ] &8609 sum_free_space
- [ ] &8632 allocate_disc_space
- [ ] &8708 advance_text_ptr
- [ ] &870F parse_and_setup_search
- [ ] &871A check_char_is_terminator
- [ ] &872D check_filename_length
- [ ] &8753 compare_filename
- [ ] &8798 check_both_exhausted
- [ ] &87A8 begin_star_match
- [ ] &87CB star_match_succeeded
- [ ] &87CF check_name_ended

## Batch &8800-&8FFF: Directory operations, entry manipulation (34 subs)

- [ ] &880C disc_op_tpl_read_fsm
- [ ] &8822 parse_drive_from_ascii
- [ ] &8849 bad_drive_name
- [ ] &884C parse_filename_from_cmdline
- [ ] &8905 save_text_ptr_after_match
- [ ] &895E advance_dir_entry_ptr
- [ ] &89D0 get_object_type_result
- [ ] &89D3 save_wksp_and_return
- [ ] &8A3D multi_sector_disc_command
- [ ] &8A45 check_disc_command_type
- [ ] &8A63 adjust_for_partial_xfer
- [ ] &8B1E floppy_partial_sector
- [ ] &8B41 hd_command_partial_sector
- [ ] &8BB3 exec_disc_and_check_error
- [ ] &8BC8 not_found_error
- [ ] &8C05 osfile_save_check_existing
- [ ] &8C62 search_dir_for_file
- [ ] &8CC3 check_existing_for_save
- [ ] &8CC9 setup_disc_write
- [ ] &8D10 check_file_not_open
- [ ] &8D21 check_open
- [ ] &8D69 no_open_files_on_drive
- [ ] &8D6E set_up_directory_search
- [ ] &8DD6 parse_and_search_dir
- [ ] &8DDE mark_saved_drive_unset
- [ ] &8DED tbl_forbidden_chars
- [ ] &8DF3 check_file_not_open2
- [ ] &8E6F allocate_disc_space_for_file
- [ ] &8E8B copy_entry_from_template
- [ ] &8F4C validate_not_locked
- [ ] &8F86 write_dir_and_validate
- [ ] &8FDF find_first_matching_entry
- [ ] &8FEA mark_directory_dirty
- [ ] &8FFA check_first_char_wildcard

## Batch &9000-&95FF: Catalogue, path resolution, star commands (23 subs)

- [ ] &905C setup_print_hex_field
- [ ] &9071 disc_op_tpl_write_fsm_unused
- [ ] &9109 star_remove
- [ ] &9128 check_and_delete_found
- [ ] &923E my_osfile
- [ ] &9269 osfile_dispatch_lo
- [ ] &927B setup_entry_name_ptr
- [ ] &92A0 print_inline_string
- [ ] &92C4 print_via_osasci
- [ ] &92DE print_entry_name_and_access
- [ ] &9316 l9316
- [ ] &931B print_hex_byte
- [ ] &932A verify_dir_and_list
- [ ] &9433 star_ex
- [ ] &944F check_special_dir_char
- [ ] &9471 parse_dir_argument
- [ ] &947F parse_path_and_load
- [ ] &94CC dummy_root_dir_entry
- [ ] &94E7 star_info
- [ ] &94FA conditional_info_display
- [ ] &9501 print_entry_info
- [ ] &953F star_dir
- [ ] &9570 star_cdir

## Batch &9600-&9BFF: Star commands, service calls, init (16 subs)

- [ ] &9632 osfile_tpl_cdir
- [ ] &97A8 format_init_dir
- [ ] &993D star_access
- [ ] &9945 clear_rwl_attributes
- [ ] &9951 set_file_attributes
- [ ] &99E6 star_destroy
- [ ] &9A43 jmp_indirect_fscv
- [ ] &9A46 default_workspace_data
- [ ] &9A63 hd_init_detect
- [ ] &9A78 boot_option_addr_table
- [ ] &9A8F service_dispatch_lo
- [ ] &9AA3 service_call_handler
- [ ] &9ACF service_handler_1
- [ ] &9AE6 adfs_hardware_found
- [ ] &9AF1 service_handler_2
- [ ] &9B41 service_handler_3

## Batch &9C00-&9FFF: MOS interface, command dispatch (17 subs)

- [ ] &9CB3 tbl_fs_vectors
- [ ] &9CC1 tbl_extended_vectors
- [ ] &9CD6 str_filing_system_name
- [ ] &9CDA service_handler_4
- [ ] &9D11 service4_claim_and_dispatch
- [ ] &9D19 service_handler_8
- [ ] &9DA7 help_print_header
- [ ] &9DBE service_handler_9
- [ ] &9DDA print_help_command_list
- [ ] &9E48 tbl_help_param_ptrs
- [ ] &9E50 my_fscv
- [ ] &9E6D fscv_dispatch_lo
- [ ] &9E7F star_cmd
- [ ] &9EE3 tbl_commands
- [ ] &9F8D tbl_help_param_strings
- [ ] &9FD8 fsc7_read_handle_range
- [ ] &9FDD fsc0_star_opt

## Batch &A000-&A4FF: *FREE, *COMPACT, utilities, string handling (29 subs)

- [ ] &A016 ca016
- [ ] &A01B star_free
- [ ] &A04A star_map
- [ ] &A094 check_compaction_recommended
- [ ] &A0BB star_delete
- [ ] &A0C3 star_bye
- [ ] &A0EA scsi_cmd_park
- [ ] &A0F5 parse_drive_argument
- [ ] &A111 star_dismount
- [ ] &A149 copy_default_dir_name
- [ ] &A15E star_mount
- [ ] &A19F scsi_cmd_unpark
- [ ] &A1AA calc_total_free_space
- [ ] &A1C6 print_space_value
- [ ] &A252 star_title
- [ ] &A276 star_compact
- [ ] &A29B bad_compact_error
- [ ] &A35A combine_hex_digit_pair
- [ ] &A365 parse_second_filename
- [ ] &A399 star_run
- [ ] &A444 star_lib
- [ ] &A460 switch_to_library
- [ ] &A473 restore_csd
- [ ] &A47F star_lcat
- [ ] &A48B star_lex
- [ ] &A497 star_back
- [ ] &A4B7 skip_filename
- [ ] &A4CF skip_spaces
- [ ] &A4F6 check_drive_colon

## Batch &A500-&A9FF: Workspace management, OSARGS, channel mgmt (16 subs)

- [ ] &A503 star_rename
- [ ] &A6C7 check_dir_loaded
- [ ] &A6DE verify_dir_integrity
- [ ] &A6F9 broken_directory_error
- [ ] &A70E get_wksp_addr_ba
- [ ] &A71A calc_wksp_checksum
- [ ] &A72B store_wksp_checksum_ba_y
- [ ] &A731 check_wksp_checksum
- [ ] &A749 save_workspace_state
- [ ] &A7A2 load_dir_for_drive
- [ ] &A7C0 setup_disc_read_for_dir
- [ ] &A816 load_fsm
- [ ] &A81D star_copy
- [ ] &A93C fsc6_new_filing_system
- [ ] &A955 my_osargs
- [ ] &A97C flush_all_channels

## Batch &AA00-&AFFF: Buffer management, BGET, sector I/O (15 subs)

- [ ] &AAA6 validate_and_set_ptr
- [ ] &AAC6 hd_command_bget_bput_sector
- [ ] &AB63 wait_write_data_phase
- [ ] &ABD8 find_buffer_for_sector
- [ ] &AC62 read_single_hd_sector
- [ ] &ACD7 calc_buffer_page_from_offset
- [ ] &ACE9 step_ensure_offset_loop
- [ ] &ACFE check_set_channel_y
- [ ] &AD16 compare_ext_to_ptr
- [ ] &AD53 eof_error
- [ ] &AD63 my_osbget
- [ ] &AD8D calc_bget_sector_addr
- [ ] &ADC5 switch_to_channel_drive
- [ ] &AE4C advance_to_next_dir_entry
- [ ] &AEBC update_ext_to_ptr

## Batch &B000-&B5FF: BPUT, OSGBPB, OSFIND, drive selection (13 subs)

- [ ] &B060 update_ext_from_new_ptr
- [ ] &B08F my_osbput
- [ ] &B123 increment_ptr_after_write
- [ ] &B18C sync_ext_to_ptr
- [ ] &B1B3 star_close
- [ ] &B1B6 my_osfind
- [ ] &B24D next_conflict_check
- [ ] &B3F1 update_dir_entry_on_close
- [ ] &B4F5 check_drive_and_reload_fsm
- [ ] &B510 get_drive_bit_mask
- [ ] &B51C set_drive_from_channel
- [ ] &B579 convert_drive_to_slot
- [ ] &B57F my_osgbpb

## Batch &B600-&BFFF: Floppy driver, NMI handler, format, utilities (34 subs)

- [ ] &B825 setup_osgbpb_output_buffer
- [ ] &B85B output_byte_to_buffer
- [ ] &B872 output_dir_entry_name
- [ ] &B980 transfer_sector_bytes
- [ ] &BA00 do_floppy_scsi_command_ind
- [ ] &BA11 floppy_check_present
- [ ] &BAC6 process_floppy_result
- [ ] &BAF4 retry_after_error
- [ ] &BB09 fdc_write_register_verify
- [ ] &BB14 do_floppy_scsi_command
- [ ] &BB42 floppy_init_transfer
- [ ] &BB82 set_read_transfer_mode
- [ ] &BB92 claim_nmi_and_init
- [ ] &BBB4 floppy_get_step_rate
- [ ] &BBDA claim_nmi
- [ ] &BBE7 release_nmi
- [ ] &BBF1 copy_code_to_nmi_space
- [ ] &BC79 nmi_code_start
- [ ] &BC93 nmi_check_status_error
- [ ] &BCA5 nmi_check_end_of_operation
- [ ] &BCC2 floppy_wait_nmi_finish
- [ ] &BCFD select_fdc_rw_command
- [ ] &BD19 floppy_set_side_0_unused
- [ ] &BD22 floppy_set_side_1
- [ ] &BD2B clear_transfer_complete
- [ ] &BD38 clear_seek_flag
- [ ] &BD3F floppy_restore_track_0
- [ ] &BD4C apply_head_load_flag
- [ ] &BD58 floppy_format_track
- [ ] &BF55 floppy_calc_track_sector_from_block_check_range
- [ ] &BF86 floppy_calc_track_sector_from_b0_block
- [ ] &BFA2 xa_div_16_to_ya
- [ ] &BFAE floppy_error
- [ ] &BFF6 str_rom_footer

