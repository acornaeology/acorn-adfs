# Glossary

**ADFS** (Advanced Disc Filing System)
: A filing system ROM for the BBC Micro supporting hierarchical directories, random access files, and both floppy disc and SCSI hard disc storage.

  ADFS was Acorn's replacement for the simpler DFS (Disc Filing System), adding
  subdirectories, longer filenames, and hard disc support. It uses a free space
  map rather than a fixed catalogue, allowing more flexible disc allocation.

**BRK**
: A 6502 software interrupt instruction used by the MOS for error reporting. A BRK is followed by an error number byte and a zero-terminated error message string. The MOS routes BRK through BRKV (&0202).

**CSD** (Currently Selected Directory)
: The directory that ADFS uses as the default context for file operations. Changed with `*DIR`. Stored in the directory buffer at &1200-&16FF.

**Directory**
: An ADFS on-disc structure occupying five contiguous sectors, containing up to 47 file entries of 26 bytes each plus metadata (title, parent pointer, sequence number). Identified by a four-character marker string "Hugo" or "Nick".

**Directory entry**
: A 26-byte record within a directory: 10 bytes for name and access string, 4 bytes load address, 4 bytes execution address, 4 bytes length, 3 bytes start sector, 1 byte sequence number.

**Free space map** (FSM)
: A pair of 256-byte sectors (sectors 0 and 1) on each drive describing the free space as a list of (address, length) pairs. Sector 0 holds disc addresses; sector 1 holds corresponding lengths. Stored in RAM at &0E00-&0FFF.

  The free space map also contains the disc identifier, boot option number,
  total disc size, and a checksum byte. The pointer at byte 254 of sector 1
  indicates the end of the free space list.

**GSINIT/GSREAD**
: MOS string-handling routines. GSINIT (&C2B2) initialises parsing of a string argument; GSREAD (&C2A2) reads the next character, handling quoted strings and escape sequences.

**MOS** (Machine Operating System)
: The BBC Micro's built-in operating system ROM, providing the filing system API (OSFILE, OSFIND, OSGBPB, etc.), service call dispatch, and hardware abstraction.

**NMI** (Non-Maskable Interrupt)
: A hardware interrupt used by the WD1770 floppy disc controller for data transfer. ADFS installs its own NMI handler to manage byte-by-byte disc I/O.

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

**SCSI** (Small Computer System Interface)
: The bus protocol used by ADFS for Winchester (hard disc) access. The BBC Micro's SCSI interface uses memory-mapped registers at &FC40-&FC43.

  ADFS implements the full SCSI selection, command, data transfer, and status
  phases. Drive selection encodes the SCSI ID as a bit pattern (drive 0 = &01,
  drive 1 = &02, etc.). The LUN is encoded in the top 3 bits of the command
  block's MSB sector address byte.

**Service call**
: The MOS mechanism for broadcasting events to sideways ROMs. ADFS responds to service calls for ROM initialisation, command dispatch, filing system selection, and break handling.

**Sideways ROM**
: One of up to 16 ROM images mapped into the &8000-&BFFF address space on the BBC Micro. Only one is paged in at a time, selected via the ROM latch at &FE30. ADFS is a 16 KB sideways ROM.

**Tube**
: The interface between the BBC Micro (host) and a second processor (parasite). ADFS includes Tube support for transferring data between the host's disc system and the parasite's memory.

**WD1770**
: The Western Digital floppy disc controller IC used in the BBC Micro Model B+ and later machines. Accessed via memory-mapped registers at &FE80-&FE87. ADFS uses the 1770 for floppy disc read, write, seek, and format operations.

  The 1770 replaced the earlier Intel 8271 controller. ADFS 1.30 supports only
  the 1770, not the 8271.

**Workspace**
: ADFS claims private RAM at &0E00-&11FF for the free space map (&0E00-&0FFF), general workspace (&1000-&11FF), and the directory buffer (&1200-&16FF). This memory is above the default DFS/tape PAGE but below ADFS's own PAGE of &1D00.

**Zero page**
: The first 256 bytes of 6502 memory (&00-&FF), used for fast access via zero-page addressing modes. ADFS uses a small number of zero-page locations (around &A0-&BF) for temporary pointers and workspace during filing system operations.
