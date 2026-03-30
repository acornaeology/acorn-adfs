# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project overview

Annotated disassembly of Acorn ADFS (Advanced Disc Filing System) ROMs for the BBC Micro. Python scripts drive py8dis (a programmable 6502 disassembler) to produce readable, verified assembly output from the original ROM binaries. The first version covered is 1.30.

## Build commands

Requires [uv](https://docs.astral.sh/uv/) and [beebasm](https://github.com/stardot/beebasm) (v1.10+).

```sh
uv sync                                     # Install dependencies
uv run acorn-adfs-disasm-tool disassemble 1.30  # Generate .asm and .json from ROM
uv run acorn-adfs-disasm-tool lint 1.30         # Validate annotation addresses
uv run acorn-adfs-disasm-tool verify 1.30       # Reassemble and byte-compare against original ROM
```

Verification is the primary correctness check: the generated assembly must reassemble to a byte-identical copy of the original ROM. Lint validates that all annotation addresses (comments, subroutines, labels) reference valid item addresses in the py8dis output. CI runs `disassemble`, `lint`, then `verify` on every push.

## Architecture

### CLI entry point

`src/disasm_tools/cli.py` — subcommands: `disassemble`, `verify`, `lint`, `compare`, `extract`, `audit`, `cfg`, `context`, `labels`, `rename-labels`, `insert-point`, `comment-check`, `backfill`. Sets env vars `ACORN_ADFS_ROM` and `ACORN_ADFS_OUTPUT` before invoking version-specific scripts.

### Disassembly driver

`versions/adfs-1.30/disassemble/disasm_adfs_130.py` — the main annotation file. Configures py8dis with labels, constants, subroutine descriptions, comments, and relocated code blocks using py8dis's DSL (`label()`, `constant()`, `comment()`, `subroutine()`, `move()`, `hook_subroutine()`). This is where most development work happens.

### Lint

`src/disasm_tools/lint.py` — validates that every `comment()`, `subroutine()`, and `label()` address in a driver script corresponds to a valid address in the py8dis JSON output. Also validates `address_links` and `glossary_links` in each version's `rom.json`.

### Verification

`src/disasm_tools/verify.py` — assembles the generated `.asm` with beebasm and does a byte-for-byte comparison against the original ROM.

### Version layout

Each ROM version lives under `versions/adfs-<version>/`. Subdirectories:
- `rom/` — original ROM binary and metadata (`rom.json` with hashes)
- `disassemble/` — py8dis driver script
- `output/` — generated assembly (`.asm`) and structured data (`.json`)

Version IDs in `acornaeology.json` and CLI arguments are bare numbers (`1.30`). The `resolve_version_dirpath()` helper in `src/disasm_tools/paths.py` maps them to the directory using the `adfs` prefix.

### Glossary

`GLOSSARY.md` — project-level glossary of ADFS-specific and Acorn terms, registered in `acornaeology.json` as `"glossary": "GLOSSARY.md"`. Uses Markdown definition-list syntax with a brief/extended split:

```markdown
**TERM** (Expansion)
: Brief definition — one or two sentences. What the term IS.

  Extended detail — how ADFS uses it, implementation specifics,
  or additional context. Shown only on the glossary page.
```

First paragraph = brief (tooltip text). Subsequent indented paragraphs after a blank line = extended (glossary page only). Entries without extended detail keep a single paragraph.

### Documentation links in `rom.json`

Each version's `rom/rom.json` has a `docs` array. Each doc entry can have:

- `address_links` — maps hex address patterns in Markdown to disassembly addresses (validated by lint against the JSON output)
- `glossary_links` — maps term patterns in Markdown to glossary entries (validated by lint against `GLOSSARY.md`)

Both use the same shape: `{"pattern": "...", "occurrence": 0, "term"|"address": "..."}`. The `occurrence` field is a 0-based index among all substring matches of the pattern.

## Key technical context

- ADFS ROM base address: 0x8000, size: 16384 bytes (16 KB sideways ROM)
- NMOS 6502 processor (not 65C02)
- Free space map: sectors 0-1, stored in RAM at &0E00-&0FFF
- Directory buffer: 5 contiguous sectors, stored at &1200-&16FF (max 47 entries of 26 bytes)
- Workspace: &1000-&11FF
- SCSI registers: &FC40 (data), &FC42 (select)
- WD1770 floppy controller: &FE80-&FE87
- PAGE raised to &1D00 when ADFS selected
- py8dis dependency is a custom fork at `github.com/acornaeology/py8dis`
- Assembly output targets beebasm syntax
- Assembly comments are formatted to fit within 62 characters
