"""pdf_allowlist.py — Single source of truth for the PDF file list.

Imported by both build_pdf.py and translate_docs.py.
Edit only this file when adding or removing documents from the PDF.

Rules:
  - Each entry is (section_key, relative_path_from_docs_dir).
  - section_key must match a key in STRINGS["en"]["sections"] in build_pdf.py.
  - Order determines the order documents appear in the PDF.
  - Files under business/*-process.md, business/*-object.md, and
    modules/*/*-module-data-flow.md are auto-scanned and do NOT need to be listed here.
  - log-*.md files are intentionally excluded — they are implementation-level detail,
    not suitable for the PDF audience.
"""

PDF_ALLOWLIST = [
    # 1. Business — understand why before what
    ("business",       "business/business-process.md"),   # index
    ("business",       "business/business-objects.md"),   # index
    ("business",       "business/business-rules.md"),
    # 2. Requirements — what to build
    ("requirements",   "project-requirements.md"),
    # 3. Architecture — how it is structured
    ("architecture",   "architecture/architecture.md"),
    ("architecture",   "architecture/backend.md"),
    ("architecture",   "architecture/frontend.md"),
    ("architecture",   "architecture/database.md"),
    ("architecture",   "architecture/deployment.md"),
    # 4. Specifications — how it is implemented
    ("specifications", "specs/quickstart.md"),
    ("specifications", "specs/data-model.md"),
    ("specifications", "specs/api-contract.md"),
    ("specifications", "specs/permissions.md"),
    ("specifications", "specs/logging-spec.md"),
    # specs/research.md — excluded until filled with actual technology decisions
    # 5. Flows — individual *-module-data-flow.md and *-flow.md are added automatically
    # by build_pdf.py (find_allowed_files). The index files are included but filtered
    # to show only their index tables (see PDF_SECTION_FILTER below).
    ("flows",          "modules/module-data-flow.md"),
    ("flows",          "modules/module-flow.md"),
    # 6. Project Status
    ("project",        "codebase-map.md"),
]


# Per-file section filter: only the listed ## headings (and their content) are kept.
# Everything else in the file is stripped before rendering.
# Key: relative path from docs_dir (same as PDF_ALLOWLIST).
# Value: list of exact ## heading strings to keep.
PDF_SECTION_FILTER = {
    "modules/module-data-flow.md":    ["## Module Flow Files"],
    "modules/module-flow.md":         ["## Flow Files"],
    "business/business-objects.md":   ["## Object Files", "## Relationships"],
    "business/business-process.md":   ["## Process Files"],
    # business-rules.md: keep real rule sections, strip BR-001/BR-002 placeholder blocks
    # (placeholder ### headings are removed by clean_for_pdf, but keeping explicit here
    #  in case the file has content mixed with placeholders)
    "business/business-rules.md":     ["## Approval Rules", "## Validation Rules",
                                       "## Notification Rules", "## Audit Rules"],
}
