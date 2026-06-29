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
    ("specifications", "specs/data-model.md"),
    ("specifications", "specs/api-contract.md"),
    ("specifications", "specs/permissions.md"),
    ("specifications", "specs/logging-spec.md"),
    ("specifications", "specs/research.md"),
    # 5. Flows — how it runs (individual *-module-data-flow.md added automatically)
    ("flows",          "modules/module-data-flow.md"),
    # 6. Project Status
    ("project",        "codebase-map.md"),
]
