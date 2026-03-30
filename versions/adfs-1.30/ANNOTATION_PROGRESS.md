# ADFS 1.30 Annotation Progress

Systematic inline commenting of every subroutine, working bottom-up
through the call graph. Each routine gets inline comments on every
instruction, then a review pass for intention-revealing comments.

## Depth 0 (leaves - no outgoing calls)

- [x] &8027 claim_tube
- [x] &8043 release_tube
- [x] &8056 scsi_get_status
- [x] &8080 command_set_retries
- [x] &81EF tube_start_xfer_sei
- [x] &8305 wait_ensuring
- [x] &8348 reload_fsm_and_dir_then_brk
- [x] &8351 generate_error_no_suffix
- [x] &843E hex_digit
- [x] &8449 dec_number_error_100_y
- [x] &8476 invalidate_fsm_and_dir
- [x] &84A7 oscli_at_x
- [x] &84B5 release_disc_space (partial)
- [x] &871A check_char_is_terminator
- [x] &8B1E floppy_partial_sector
- [x] &923E my_osfile (dispatch commented)
- [x] &9433 star_ex
- [x] &94E7 star_info
- [x] &953F star_dir
- [x] &9A43 jmp_indirect_fscv
- [x] &9A63 hd_init_detect
- [x] &9AA3 service_call_handler
- [x] &9CDA service_handler_4
- [x] &9E50 my_fscv (dispatch only)
- [x] &A252 star_title
- [x] &A444 star_lib
- [x] &A47F star_lcat
- [x] &A48B star_lex
- [x] &A70E get_wksp_addr_ba
- [x] &A816 load_fsm
- [x] &ACFE check_set_channel_y
- [x] &B1B3 star_close
- [x] &BBB4 floppy_get_step_rate
- [x] &BBF1 copy_code_to_nmi_space
- [x] &BD22 floppy_set_side_1
- [x] &BF55 floppy_calc_track_sector_from_block_check_range
- [x] &BFA2 xa_div_16_to_ya

## Depth 1

- [x] &8065 scsi_start_command
- [x] &830F scsi_wait_for_req
- [x] &842D hex_number_error_100_y
- [x] &872D check_filename_length
- [x] &8D21 check_open (entry only)
- [x] &9109 star_remove
- [x] &92A0 print_inline_string
- [x] &993D star_access
- [x] &9E7F star_cmd
- [x] &A276 star_compact
- [x] &A497 star_back
- [x] &A503 star_rename
- [x] &A6C7 check_dir_loaded
- [x] &A71A calc_wksp_checksum
- [x] &A81D star_copy
- [x] &A93C fsc6_new_filing_system
- [x] &AD16 compare_ext_to_ptr
- [x] &B08F my_osbput (entry only)
- [x] &BF86 floppy_calc_track_sector_from_b0_block
- [x] &BFAE floppy_error

## Depth 2

- [x] &81B8 hd_data_transfer_256
- [x] &8353 generate_error_suffix_x
- [x] &99E6 star_destroy
- [x] &9DBE service_handler_9
- [x] &A01B star_free
- [x] &A04A star_map
- [x] &A0BB star_delete
- [x] &A731 check_wksp_checksum
- [x] &A955 my_osargs (entry only)
- [x] &AD63 my_osbget (entry only)
- [x] &B1B6 my_osfind (entry only)
- [x] &B57F my_osgbpb (entry only)
- [x] &BB14 do_floppy_scsi_command (entry only)
- [x] &BCC2 floppy_wait_nmi_finish

## Depth 3+

- [x] &829A generate_error
- [x] &80ED hd_command
- [x] &8089 command_exec_xy
- [x] &818A command_done
- [x] &823A scsi_request_sense
- [x] &831B scsi_send_byte_a
- [x] &8753 compare_filename
- [x] &9570 star_cdir (entry only)
- [x] &9ACF service_handler_1
- [x] &9AF1 service_handler_2
- [x] &9B41 service_handler_3 (partial)
- [x] &9D19 service_handler_8
- [x] &A0C3 star_bye
- [x] &A15E star_mount
- [x] &A399 star_run
- [x] &A111 star_dismount
- [x] &82FB scsi_send_cmd_byte
- [x] &81F0 tube_start_xfer
- [x] &8B41 hd_command_partial_sector
- [x] &AAC6 hd_command_bget_bput_sector
- [x] &BA00 do_floppy_scsi_command_ind
- [x] &BA11 floppy_check_present
- [x] &BD3F floppy_restore_track_0
- [x] &BF86 floppy_calc_track_sector_from_b0_block
