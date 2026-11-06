# Changelog

All notable changes to this repository are tracked here.

## 0.1.1 - 2026-06-06

### Added

- Add behavior eval fixtures for planning, generation, editing, saving, QA handoff, and trigger-boundary cases.
- Add validator checks that bind behavior fixtures to the skill and reference source files.

### Changed

- Clarify that saved images go under the current workspace root, not the installed skill bundle.
- Add mode-specific reference loading guidance.
- Require a compact per-image QA manifest in final handoffs.
- Define direct generation without an explicit count as 3 images.
- Narrow implicit use boundaries for generic illustration, PPT, commercial brand art, children's cartoons, and non-Xiaohei image requests.

## 0.1.0 - 2026-06-06

### Added

- Add explicit skill operating modes: `plan_only`, `generate`, `edit`, and `save`.
- Add a pre-generation image spec contract before `image_gen` calls.
- Add deterministic save rules for slugged folders, sequential filenames, collision suffixes, and absolute-path handoffs.
- Add a zero-dependency repository validator exposed through `npm test`.
- Add copied-skill version tracking through `ian-xiaohei-illustrations/VERSION`.

### Changed

- Expand prompt and QA references so generation, editing, and saving rules are visible to future agents.
- Document the validation workflow in the README.
