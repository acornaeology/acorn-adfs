# Glossary

**ADFS** (Advanced Disc Filing System)
: A filing system ROM for the BBC Micro supporting hierarchical directories, random access files, and both floppy disc and SCSI hard disc storage.

  ADFS was Acorn's replacement for the simpler DFS (Disc Filing System), adding
  subdirectories, longer filenames, and hard disc support. It uses a free space
  map rather than a fixed catalogue, allowing more flexible disc allocation.

**Boot option**
: A per-disc setting (0-3) stored in the free space map that controls what happens when the disc is booted. Option 0 does nothing, 1 runs `*LOAD $.!BOOT`, 2 runs `*RUN $.!BOOT`, and 3 runs `*EXEC $.!BOOT`. Set with `*OPT 4,n`.

**BRK**
: A 6502 software interrupt instruction used by the MOS for error reporting. A BRK is followed by an error number byte and a zero-terminated error message string. The MOS routes BRK through BRKV (&0202).

**Channel**
: An internal slot representing an open file. ADFS supports up to 10 simultaneous open files, numbered 0-9 internally and presented as file handles &30-&39. Each channel tracks the file's PTR, EXT, allocation, buffer state, start sector, and parent directory.

  The per-channel tables occupy workspace page 2 (&1100-&11FF), with separate
  tables for EXT, PTR, allocation, flags, start sector, and directory sector.
  Each table has 10-byte spacing (one byte per channel). The channel buffer
  table at &1000-&1014 has 5 slots with 4-byte spacing, mapping buffer sectors
  and dirty flags for the most recently accessed channels.

**CSD** (Currently Selected Directory)
: The directory that ADFS uses as the default context for file operations. Changed with `*DIR`. Stored in the directory buffer at &1200-&16FF.

**DFS** (Disc Filing System)
: Acorn's original floppy disc filing system for the BBC Micro. DFS uses a fixed catalogue of up to 31 files in a flat structure with no subdirectories. ADFS replaced DFS for users needing hierarchical directories and hard disc support.

**Directory**
: An ADFS on-disc structure occupying five contiguous sectors, containing up to 47 file entries of 26 bytes each plus metadata (title, parent pointer, sequence number). Identified by a four-character marker string "Hugo" or "Nick".

**Directory entry**
: A 26-byte record within a directory: 10 bytes for name and access string, 4 bytes load address, 4 bytes execution address, 4 bytes length, 3 bytes start sector, 1 byte sequence number.

**Disc ID** (Disc Identifier)
: A two-byte value stored in the free space map (bytes &FB-&FC of sector 1) that identifies the currently inserted disc. ADFS saves the disc ID per drive slot and compares it on each access to detect disc changes, triggering an FSM and directory reload when a different disc is found.

**DRQ** (Data Request)
: A hardware signal from the WD1770 floppy disc controller indicating that a byte of data is ready to be transferred. Each DRQ assertion triggers an NMI, which the ADFS NMI handler services by reading or writing one byte between the FDC data register and the transfer buffer.

**EXT** (File Extent)
: The logical size of an open file in bytes. Tracked as a 4-byte value per channel. BPUT operations beyond EXT automatically extend the file. OSARGS A=3 reads EXT; OSARGS A=4 writes it.

**FDC** (Floppy Disc Controller)
: The hardware controller chip for floppy disc drives. In ADFS 1.30 this is the WD1770, accessed via memory-mapped registers at &FE80-&FE87. The FDC handles low-level disc operations including read, write, seek, and format.

**Free space map** (FSM)
: A pair of 256-byte sectors (sectors 0 and 1) on each drive describing the free space as a list of (address, length) pairs. Sector 0 holds disc addresses; sector 1 holds corresponding lengths. Stored in RAM at &0E00-&0FFF.

  The free space map also contains the disc identifier, boot option number,
  total disc size, and a checksum byte. The pointer at byte 254 of sector 1
  indicates the end of the free space list.

**FSC** (Filing System Control)
: A set of sub-function codes dispatched through the FSCV vector (&021E). FSC calls handle operations like `*RUN`, `*CAT`, boot, and filing system selection. ADFS implements FSC codes 0-8 via a dispatch table.

**GSINIT/GSREAD**
: MOS string-handling routines. GSINIT (&C2B2) initialises parsing of a string argument; GSREAD (&C2A2) reads the next character, handling quoted strings and escape sequences.

**LUN** (Logical Unit Number)
: A secondary address within a SCSI device, allowing a single physical device to present multiple logical discs. ADFS encodes the LUN in the top 3 bits of the sector address high byte in the SCSI command descriptor block, supporting up to 8 logical units per SCSI target.

**MOS** (Machine Operating System)
: The BBC Micro's built-in operating system ROM, providing the filing system API (OSFILE, OSFIND, OSGBPB, etc.), service call dispatch, and hardware abstraction.

**NMI** (Non-Maskable Interrupt)
: A hardware interrupt used by the WD1770 floppy disc controller for data transfer. ADFS installs its own NMI handler to manage byte-by-byte disc I/O.

  The NMI handler is self-modifying code copied to RAM at &0D00-&0D5F.
  The read/write opcode, transfer address, and completion flag are patched
  at runtime. Separate handler variants exist for direct memory transfer
  and Tube transfer. For multi-sector operations, the handler calls back
  into the ROM to step between tracks.

**OSARGS**
: MOS routine at &FFDA for reading and writing open file attributes. Dispatched through ARGSV (&0214). With A=0 reads PTR, A=1 writes PTR, A=2 reads EXT, A=3 writes EXT, A=&FF ensures (flushes) all files to disc.

**OSBGET** (OS Byte Get)
: MOS routine at &FFD7 for reading a single byte from an open file. Dispatched through BGETV (&0216). Returns the byte in A and advances the file's PTR by one.

**OSBPUT** (OS Byte Put)
: MOS routine at &FFD4 for writing a single byte to an open file. Dispatched through BPUTV (&0218). Writes the byte in A at the current PTR position and advances PTR. If PTR reaches EXT, the file is extended.

**OSBYTE**
: MOS routine at &FFF4 for miscellaneous OS functions, selected by the value in A. ADFS uses OSBYTE for operations like reading the ROM number, claiming workspace, and setting PAGE.

**OSCLI**
: MOS routine at &FFF7 for executing star commands. ADFS registers its commands through the service call mechanism and dispatches them via a command table.

**OSFILE**
: MOS routine at &FFDD for whole-file operations (load, save, read/write catalogue info, delete, create). Indirected through FILEV (&0212).

**OSFIND**
: MOS routine at &FFCE for opening and closing files for byte access. Indirected through FINDV (&021C).

**OSGBPB**
: MOS routine at &FFD1 for reading or writing groups of bytes. Indirected through GBPBV (&021A).

**OSWORD**
: MOS routine at &FFF1 for word-sized operations, selected by the value in A. ADFS uses OSWORD &72 for direct disc access (read/write sectors).

**PAGE**
: The address of the start of user memory, set by the current filing system. ADFS sets PAGE to &1D00, above its workspace and directory buffer.

**PTR** (File Pointer)
: The current read/write position within an open file, tracked as a 4-byte value per channel. Automatically advanced by BGET/BPUT and OSGBPB. OSARGS A=0 reads PTR; OSARGS A=1 writes PTR (allowing random access).

**SCSI** (Small Computer System Interface)
: The bus protocol used by ADFS for Winchester (hard disc) access. The BBC Micro's SCSI interface uses memory-mapped registers at &FC40-&FC43.

  ADFS implements the full SCSI selection, command, data transfer, and status
  phases. Drive selection encodes the SCSI ID as a bit pattern (drive 0 = &01,
  drive 1 = &02, etc.). The LUN is encoded in the top 3 bits of the command
  block's MSB sector address byte.

**Sector**
: The basic unit of disc storage, 256 bytes in ADFS. Sectors are addressed by a 3-byte sector number (up to 16 million sectors). On floppy discs, 16 sectors per track. On hard discs, sectors are addressed linearly through SCSI commands.

**Service call**
: The MOS mechanism for broadcasting events to sideways ROMs. ADFS responds to service calls for ROM initialisation, command dispatch, filing system selection, and break handling.

**Sideways ROM**
: One of up to 16 ROM images mapped into the &8000-&BFFF address space on the BBC Micro. Only one is paged in at a time, selected via the ROM latch at &FE30. ADFS is a 16 KB sideways ROM.

**Track**
: A concentric circular path on a floppy disc surface. ADFS uses 80 tracks per side (0-79), with 16 sectors per track, giving 1280 sectors (320 KB) per side. Double-sided discs use tracks 0-79 for side 0 and 80-159 for side 1, giving 640 KB total.

**Tube**
: The interface between the BBC Micro (host) and a second processor (parasite). ADFS includes Tube support for transferring data between the host's disc system and the parasite's memory.

  When a second processor is present, file data is transferred via the Tube
  ULA registers (&FEE0-&FEE7) rather than being stored directly in host
  memory. The NMI handler has separate code paths for Tube read and Tube
  write operations.

**VIA** (Versatile Interface Adapter)
: The MOS Technology 6522 peripheral interface chip. The BBC Micro has two VIAs: the system VIA at &FE40-&FE4F (keyboard, sound, timers) and the user VIA at &FE60-&FE6F. ADFS reads the system VIA timer T1 counter (&FE44) to seed disc ID values.

**WD1770**
: The Western Digital floppy disc controller IC used in the BBC Micro Model B+ and later machines. Accessed via memory-mapped registers at &FE80-&FE87. ADFS uses the 1770 for floppy disc read, write, seek, and format operations.

  The 1770 replaced the earlier Intel 8271 controller. ADFS 1.30 supports only
  the 1770, not the 8271.

**Winchester**
: Industry term for a sealed hard disc drive, used by Acorn documentation to refer to SCSI hard discs attached to the BBC Micro. ADFS supports Winchester drives as drives 0-3 (SCSI ID 0, LUN 0-3), with floppy drives mapped to drives 4-7.

**Workspace**
: ADFS claims private RAM at &0E00-&11FF for the free space map (&0E00-&0FFF), general workspace (&1000-&11FF), and the directory buffer (&1200-&16FF). This memory is above the default DFS/tape PAGE but below ADFS's own PAGE of &1D00.

**Zero page**
: The first 256 bytes of 6502 memory (&00-&FF), used for fast access via zero-page addressing modes. ADFS uses a small number of zero-page locations (around &A0-&BF) for temporary pointers and workspace during filing system operations.
