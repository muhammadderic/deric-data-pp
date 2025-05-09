# Changelog

All notable changes to this project will be documented in this file.  
This format follows *Keep a Changelog* and *Semantic Versioning (SemVer)*.

---

## [0.1.0] - 2026-03-23-1614

### Added
- Core EDA Suite: Initial implementation of primary exploratory data analysis functions:
  - `analyze_numerical_statistics`
  - `analyze_categorical_statistics`
  - `classify_dataframe_columns`
  - `show_missing_values`
  - `show_unique_values_of_cat_columns`
- Custom Prompt System: Introduced the `custom_prompt` decorator for `analyze_numerical_statistics`, enabling modular, template-based expert instructions.
- Raw Code Introspection: Added support for viewing the underlying source code via `.raw()`.
- Template Support: Implemented a modular loading system for `.txt` template files.

### Fixed
- Packaging: Updated `pyproject.toml` to ensure `.txt` template files are properly included during installation.