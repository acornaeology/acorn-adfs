# Disassembly Guide

How to produce and maintain annotated, verified disassemblies of Acorn ADFS ROMs. Based on the successful disassembly of ADFS 1.30.

For project overview and build instructions, see [README.md](README.md). For architecture details, see [CLAUDE.md](CLAUDE.md). For ADFS-specific terminology, see [GLOSSARY.md](GLOSSARY.md).


## Prerequisites

- [uv](https://docs.astral.sh/uv/) for Python dependency management
- [beebasm](https://github.com/stardot/beebasm) (v1.10+) for assembly verification
- The ROM binary (16384 bytes for a 16 KB sideways ROM) for the version being disassembled
- MD5 and SHA-256 hashes of the ROM (`md5 <rom>`, `shasum -a 256 <rom>`)
- Reference materials: the Acorn ADFS User Guide, existing disassemblies (Hoglet, JGH, ADFS-multi-target)


## Quick reference: CLI tools

All tools are invoked via `uv run acorn-adfs-disasm-tool <command>`.

| Command | Description | Example |
|---------|-------------|---------|
| `disassemble` | Generate `.asm` and `.json` from ROM | `... disassemble 1.30` |
| `verify` | Reassemble and byte-compare against original ROM | `... verify 1.30` |
| `lint` | Validate annotation addresses and check for duplicates | `... lint 1.30` |
| `compare` | Compare two ROM versions (byte and opcode level) | `... compare 1.30 1.33` |
| `extract` | Extract assembly section by address range or label | `... extract 1.30 &8027 &8065` |
| `audit` | Audit subroutine annotations (summary, detail, flags) | `... audit 1.30 --summary` |
| `cfg` | Build inter-procedural call graph with depth ordering | `... cfg 1.30 --depth` |
| `context` | Generate per-subroutine context files for commenting | `... context 1.30 --sub 8027` |
| `labels` | Generate per-label context files for renaming | `... labels 1.30 --summary` |
| `rename-labels` | Batch rename auto-generated labels | `... rename-labels 1.30 --file renames.txt` |
| `insert-point` | Find insertion point for new subroutine declaration | `... insert-point 1.30 &8027` |
| `comment-check` | Check inline comments against instruction data | `... comment-check 1.30` |
| `backfill` | Propagate annotations between versions | `... backfill 1.30 1.33` |

The `extract` command accepts hex addresses in multiple formats (`&80EA`, `$80EA`, `0x80EA`) as well as label names.


## Quick reference: ad-hoc tools

Scripts in the `tools/` directory for cross-referencing and analysis:

| Tool | Description |
|------|-------------|
| `extract_multitarget_symbols.py` | Extract meaningful labels from the ADFS-multi-target ld65 debug file |
| `generate_labels_from_symbols.py` | Convert multi-target symbols to py8dis `label()` calls |
| `import_hoglet_labels.py` | Extract labels from Hoglet's BeebAsm disassembly |
| `import_multitarget_labels.py` | Parse workspace definitions from ADFS-multi-target source |
| `extract_jgh_comments.py` | Extract block comments from J.G. Harston's disassembly |
| `analyse_uncommented.py` | Analyse uncommented regions using cross-reference context |
| `basic_blocks.py` | Identify basic blocks and their annotation status per subroutine |
| `suggest_comments.py` | Generate comment suggestions from operand labels and patterns |


## Producing a new version disassembly

### Step 1: Directory structure

Create the version directory tree:

```
versions/adfs-<VER>/
  rom/
    adfs-<VER>.rom         # The ROM binary
    rom.json               # Metadata: title, size, md5, sha256, docs
  disassemble/
    __init__.py            # Empty
    disasm_adfs_<ver>.py   # Driver script (lowercase, dots removed)
  output/                  # Generated .asm and .json go here
```

Update `acornaeology.json` to add the new version to the versions array.

### Step 2: Bootstrap the driver script

Create a minimal driver script following the pattern in `disasm_adfs_130.py`:

```python
import os, sys, json
from pathlib import Path
from py8dis.commands import *
import py8dis.acorn as acorn

init(assembler_name="beebasm", lower_case=True)

# Load ROM
load(0x8000, rom_filepath, "6502")

# Standard definitions
acorn.bbc()
acorn.is_sideways_rom()

# Custom hooks for inline data patterns
def brk_error_hook(target, addr):
    inline_addr = addr + 3
    byte(inline_addr)
    stringz(inline_addr + 1)
    return None

# ... constants, labels, entry points, hooks, subroutines ...

# Generate output
output = go(print_output=False)
```

### Step 3: Import labels from reference disassemblies

If the ADFS-multi-target repository is available, build the matching configuration and extract symbols:

```sh
# Build the byte-identical ROM variant
cd /path/to/ADFS-multi-target
make -C src ROMNAME=bbcSCSI

# Verify MD5 matches
md5 build/bbcSCSI.rom

# Extract symbols (5853 symbols for ADFS 1.30)
python3 tools/extract_multitarget_symbols.py

# Generate py8dis label() calls
python3 tools/generate_labels_from_symbols.py
```

This provides meaningful names for ROM code labels, workspace locations, and hardware registers that map directly to the ADFS ROM addresses.

### Step 4: Declare dispatch tables

ADFS uses RTS-trick dispatch tables for service calls, FSCV, and OSFILE. Declare them with `rts_code_ptr()` so py8dis traces the dispatched code:

```python
# Service call dispatch: low bytes at &9A8F, high bytes at &9A99
for i in range(10):
    rts_code_ptr(0x9A8F + i, 0x9A99 + i)
```

### Step 5: Hook inline data patterns

ADFS has two common inline data patterns:

**Print-inline-string** (`print_inline_string` at &92A0): Prints a bit-7-terminated string following the JSR, then continues execution after the string.

```python
hook_subroutine(0x92A0, "print_inline_string", stringhi_hook)
```

**BRK error blocks** (`reload_fsm_and_dir_then_brk` at &8348 and similar): The called routine pops the return address to read inline error data (error number byte + zero-terminated message). Execution never continues.

```python
def brk_error_hook(target, addr):
    byte(addr + 3)
    stringz(addr + 3 + 1)
    return None

hook_subroutine(0x8348, "reload_fsm_and_dir_then_brk", brk_error_hook)
```

### Step 6: Verify the round-trip

After each change to the driver script, run the full pipeline:

```sh
uv run acorn-adfs-disasm-tool disassemble 1.30
uv run acorn-adfs-disasm-tool verify 1.30
uv run acorn-adfs-disasm-tool lint 1.30
```

Verification must always pass. Lint catches stale addresses and duplicate declarations.


## Annotation workflow

### Recommended approach: bottom-up call graph

The most effective approach is to annotate routines bottom-up through the call graph, starting with leaf routines (no outgoing calls) and working up to the complex handlers that call them.

1. **Get the call graph depth ordering**:
   ```sh
   uv run acorn-adfs-disasm-tool cfg 1.30 --depth
   ```
   This shows all declared subroutines ordered by depth, with leaves at depth 0.

2. **Create a progress tracking file** (e.g. `ANNOTATION_PROGRESS.md`) listing all routines grouped by depth, with checkboxes.

3. **Work through each routine**:
   - Use `audit --sub <addr>` to see the code, callers, callees, and flags
   - Read the ADFS User Guide entry for star commands
   - Add `comment(addr, "text", inline=True)` for every instruction
   - Add `subroutine()` with title, description, and calling convention
   - Run `disassemble`, `verify`, `lint` after each batch

4. **Mark completed routines** in the progress file.

### Why bottom-up works

Knowledge accumulates: by the time you reach a high-level routine like `my_osfile`, you already understand every subroutine it calls. The comments on leaf routines (`scsi_get_status`, `check_char_is_terminator`, `hex_digit`) provide context that makes the callers easier to understand.

### Using the basic block analysis tool

For routines that are partially annotated, the `basic_blocks.py` tool identifies which basic blocks (straight-line code sequences between branches) are uncommented and what commented blocks surround them:

```sh
python3 tools/basic_blocks.py 9109    # Detail for star_remove
python3 tools/basic_blocks.py         # Summary of all incomplete routines
```

Each uncommented block shows its predecessors and successors with their annotation status. This lets you infer the purpose of a gap from the annotated code around it — much faster than studying the code from scratch.

### Using the analyse_uncommented tool

For larger regions, the `analyse_uncommented.py` tool reports what named subroutines each uncommented region calls and what workspace locations it accesses:

```sh
python3 tools/analyse_uncommented.py
```

This reveals the purpose of unannotated code through its relationships with already-understood code.


## Annotation guidelines

### Comment style

All per-instruction comments use `inline=True`:

```python
comment(0x8027, "Y=4: copy 4 bytes", inline=True)
```

This places the comment at the end of the instruction line:

```asm
ldy #4          ; 8027: a0 04       ..             ; Y=4: copy 4 bytes
```

Without `inline=True`, comments appear on a separate line above the instruction — this is not the project style.

### Comment quality

**First pass**: Add mechanical comments that describe what each instruction does in context. Use operand labels to infer purpose:

```python
comment(0xA6C7, "Get current drive number", inline=True)   # lda wksp_current_drive
comment(0xA6CA, "Increment: &FF becomes 0", inline=True)    # inx
comment(0xA6CB, "Non-zero = drive is set, OK", inline=True) # bne return_31
```

**Second pass**: Replace mechanical comments with intention-revealing comments that explain *why*, not just *what*:

```python
comment(0xA6CB, "Drive is valid, return", inline=True)
```

**Subroutine descriptions** should explain purpose, entry/exit conditions, and side effects:

```python
subroutine(0xA6C7, "check_dir_loaded",
    title="Ensure current directory is loaded",
    description="""\
Check that the current directory buffer contains valid data.
If not, reload it from disc. Raises 'No directory' error if
no drive is selected (wksp_current_drive = &FF).
""")
```

### Comment length

Assembly comments are formatted to fit within 62 characters. This is a py8dis formatting constraint. For longer explanations, use the `subroutine()` description or add a Python comment above the `comment()` call in the driver script.

### Hex notation

- Use **Acorn notation** (`&XXXX`) in documentation, Markdown files, and human-readable output
- Use **Python notation** (`0xXXXX`) in Python scripts (driver scripts, tools)

### Naming conventions

- Labels: `snake_case` (e.g. `claim_tube`, `wksp_current_drive`, `fsm_sector_0`)
- Subroutine names: descriptive `snake_case` matching the label
- Star commands: `star_dir`, `star_cdir`, `star_rename`
- MOS handlers: `my_osfile`, `my_osfind`, `my_osgbpb`
- Service handlers: `service_handler_1`, `service_handler_2`


## Auditing annotations

### Summary mode

```sh
uv run acorn-adfs-disasm-tool audit 1.30 --summary
```

Shows all subroutines with computed flags. Key columns: address, name, terminator type (RTS/JMP/FALL→), item count, and flags.

### Detail mode

```sh
uv run acorn-adfs-disasm-tool audit 1.30 --sub claim_tube
uv run acorn-adfs-disasm-tool audit 1.30 --sub 0x8027
```

Full report including description, extent, callers, callees, escaping branches, and the assembly listing with comment templates.

### Undeclared targets

```sh
uv run acorn-adfs-disasm-tool audit 1.30 --undeclared
```

Lists all JSR/JMP targets that don't have `subroutine()` declarations. These should be declared to improve the call graph and subroutine boundary analysis.

### Audit flags

| Flag | Meaning | What to check |
|------|---------|---------------|
| `FALL_THROUGH` | Last item before next sub isn't RTS/JMP/BRK/RTI | Is the fall-through intentional and documented? |
| `FALL_THROUGH_ENTRY` | Predecessor falls through AND no JSR/JMP/branch refs | Is this genuinely only reachable via fall-through? |
| `NO_REFS` | Predecessor terminates but no refs found anywhere | Likely called indirectly (dispatch table, vector). |
| `BRANCH_ESCAPE` | A conditional branch targets outside the sub's extent | Is the branch target correct? Is it documented? |
| `DATA_ONLY` | All items are byte/string, zero code | Is this correctly marked as data, not mis-disassembly? |
| `AUTO_NAME` | Name matches `sub_c*` pattern | Needs a meaningful name. |


## Lint checks

The lint tool validates:

1. Every `comment()`, `subroutine()`, and `label()` address corresponds to a valid address in the py8dis JSON output
2. No duplicate `subroutine()` or `label()` declarations at the same address (prevents concatenated titles at call sites)
3. `address_links` in `rom.json` resolve correctly
4. `glossary_links` in `rom.json` reference valid GLOSSARY.md terms
5. No double-comment lines (`"; ;"`) in the assembly output (indicates subroutine description placed at a data address)


## Reference materials

### Acorn ADFS User Guide

The User Guide documents the behaviour of every star command, the OSFILE/OSFIND/OSGBPB/OSARGS calling conventions, the free space map format, and the directory entry structure. Read the relevant section before annotating each command handler.

Key chapters:
- Chapter 7: File handling using assembly language (OSFILE, OSFIND, OSGBPB, OSBGET, OSBPUT, OSARGS calling conventions)
- Chapter 10: Error messages (error codes and descriptions)
- Chapter 11: Technical information (free space map format, directory structure, sector layout)

### ADFS-multi-target reassembly

The [ADFS-multi-target](https://github.com/dominicbeesley/ADFS-multi-target) repository contains a ca65-based multi-target reassembly. Building the `bbcSCSI` configuration produces a byte-identical ROM to ADFS 1.30, and the ld65 debug file contains 5853 symbols with meaningful names.

The workspace definitions in `src/includes/workspace.inc` are particularly valuable — they document the layout of the &0E00-&1BFF workspace area with named fields for the free space map, disc operation control block, directory buffer, and per-channel tables.

### Hoglet's disassembly

[Hoglet's ADFS 1.30 disassembly](https://github.com/hoglet67/ADFS130) is a BeebAsm-syntax disassembly that reassembles to byte-identical ROMs. The labels are mostly address-based (`L8019` style) but the structural understanding and build variants are useful for verification.

### J.G. Harston's disassembly

J.G. Harston's disassembly (BBC BASIC source at `adfs130.src`) has selective but informative block comments at major section boundaries, including entry/exit condition documentation for key routines.


## Key technical details for ADFS 1.30

### Memory layout

| Range | Contents |
|-------|----------|
| &0E00-&0EFF | Free space map sector 0 (disc addresses) |
| &0F00-&0FFF | Free space map sector 1 (lengths) |
| &1000-&11FF | General workspace (disc op block, channel tables, flags) |
| &1200-&16FF | Directory buffer (5 sectors, max 47 entries of 26 bytes) |
| &1700-&1BFF | Random access file buffers (5 pages, one per open channel) |

### Free space map format

Sector 0 holds 3-byte disc addresses of free space regions. Sector 1 holds corresponding 3-byte lengths. Up to 82 entries. Byte 254 of sector 1 is the end-of-list pointer. Byte 255 of each sector is the checksum.

### Directory entry format

Each entry is 26 bytes:
- Bytes 0-9: Filename (bit 7 of bytes 0-3 stores R, W, L, D attributes)
- Byte 4 bit 7: E (execute only) attribute
- Bytes 10-13: Load address (4 bytes)
- Bytes 14-17: Execution address (4 bytes)
- Bytes 18-21: Length (4 bytes)
- Bytes 22-24: Start sector on disc (3 bytes)
- Byte 25: Sequence number

### SCSI command format

ADFS sends 6-byte SCSI commands: command byte, drive+LUN, sector address (3 bytes big-endian), sector count. The drive number is encoded as bits 5-7 of the second byte (LUN bits).

### Channel table layout

10 channels (handles &30-&39), each with 4-byte EXT, 4-byte PTR, allocation info, start sector, drive number, and flags. Channel tables are at fixed offsets in workspace page &1100.
