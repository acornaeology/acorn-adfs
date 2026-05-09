# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project overview

Annotated disassembly of Acorn ADFS (Advanced Disc Filing System) ROMs for the BBC Micro. Python scripts drive [dasmos](https://github.com/acornaeology/dasmos) (a programmable 6502 disassembler) to produce readable, verified assembly output from the original ROM binaries. The first version covered is 1.30.

## Build commands

Requires [uv](https://docs.astral.sh/uv/) and [beebasm](https://github.com/stardot/beebasm) (v1.10+).

```sh
uv sync                                                                                # Install dependencies (fantasm, dasmos)
uv run fantasm disassemble 1.30                                                         # Run the dasmos driver via fantasm (sets FANTASM_ROM / FANTASM_OUTPUT_DIR)
uv run fantasm lint 1.30 versions/adfs-1.30/disassemble/disasm_adfs_130.py             # Validate annotation addresses
uv run fantasm verify 1.30                                                              # Reassemble and byte-compare against original ROM
```

Verification is the primary correctness check: the generated assembly must reassemble to a byte-identical copy of the original ROM. Lint validates that all annotation addresses (comments, subroutines, labels) reference valid item addresses in the dasmos output. CI runs disassemble, lint, then verify on every push.

## Architecture

### Tooling: fantasm + dasmos

The orchestration layer is provided by [fantasm](https://github.com/acornaeology/fantasm) — installed as a regular project dependency. fantasm exposes a `fantasm` CLI (subcommands: `verify`, `lint`, `compare`, `audit`, `cfg`, `comments`, `labels`, `context`, `asm`, `sub`, `addresses`, `annotations`, `backfill`, `promote`, `fingerprint`, `shared`, `info`, `project`, `disassemble`) and a `fantasm.api` package for programmatic use. Project layout, prefixes, memory regions, and per-version metadata live in `fantasm.toml`. fantasm is library-agnostic: it runs the per-version driver as a subprocess and consumes the JSON / `.asm` artefacts the driver emits.

**Full fantasm reference: <https://acornaeology.github.io/fantasm/>** — the user guide covers every subcommand, the `fantasm.toml` schema, the version-graph workflows, and the importable `fantasm.api`. Reach for it before guessing.

[dasmos](https://github.com/acornaeology/dasmos) (a programmable 6502 disassembler with a stable 1.0 API, byte-faithful round-trip oracle, and Stevedore-managed CPU / renderer / environment plug-ins) is invoked directly via the per-version driver script under `versions/adfs-<VER>/disassemble/`. dasmos replaced the earlier py8dis tooling; the per-version drivers were ported in commit 3c3a653. The driver builds a `dasmos.Disassembler` with `Disassembler.create(cpu="6502", environments=[...])`, calls `d.load()`, registers labels/comments/subroutines/hooks, then renders both `beebasm` and `json` outputs from a single `ir = d.disassemble()` step. Reference: <https://acornaeology.github.io/dasmos/driver_api.html>. Local source of truth: `/Users/rjs/Code/acornaeology/dasmos/` (sibling checkout — read `src/dasmos/` directly when investigating behaviour).

### Disassembly driver

`versions/adfs-1.30/disassemble/disasm_adfs_130.py` — the main annotation file. Configures dasmos with labels, constants, subroutine descriptions, comments, and relocated code blocks using the dasmos driver API (`d.label()`, `d.constant()`, `d.comment()`, `d.subroutine()`, `d.add_move()`, `d.hook_subroutine()`, `d.format_hint()`). This is where most development work happens.

### Lint

`fantasm lint <VER> <DRIVER_PATH>` validates that every `comment()`, `subroutine()`, and `label()` address in a driver script corresponds to a valid address in the dasmos JSON output (or the workspace / external regions declared in `fantasm.toml`). Doc-link checks against `rom.json`'s `address_links` / `glossary_links` aren't covered by fantasm yet; they remain TODO.

### Verification

`fantasm verify <VER>` assembles the generated `.asm` with beebasm and does a byte-for-byte comparison against the original ROM.

### Version layout

Each ROM version lives under `versions/adfs-<version>/`. Subdirectories:
- `rom/` — original ROM binary and metadata (`rom.json` with hashes)
- `disassemble/` — dasmos driver script
- `output/` — generated assembly (`.asm`) and structured data (`.json`)

Version IDs in `acornaeology.json` and CLI arguments are bare numbers (`1.30`). The directory layout is governed by `[versions] prefixes` in `fantasm.toml`; fantasm's `resolve_version_files()` maps a version ID to the matching `versions/adfs-{version_id}/` directory.

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
- Disassembler dependency is `dasmos>=1.0` (resolved from PyPI). Source of truth: <https://github.com/acornaeology/dasmos>; docs at <https://acornaeology.github.io/dasmos/>
- Assembly output targets beebasm syntax (`ir.render("beebasm", ...)`); structured output is `ir.render("json")`
- Assembly comments are formatted to fit within 62 characters
