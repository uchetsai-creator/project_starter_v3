# architecture/frontend.md

Purpose:
Describe frontend structure.

Include:
- Stack
- Page structure
- Component strategy
- API hook strategy
- Shared UI standards

Avoid:
- Page-by-page requirements
- UI text
- Business workflow details

---

## Stack

[e.g., React 18 / TypeScript / React Query / Tailwind CSS]

## Page Structure

```
src/
├── pages/
│   └── [feature]/
│       └── [Feature]Page.tsx
├── components/
│   └── [feature]/
│       └── [Feature]Form.tsx
└── hooks/
    └── use[Feature].ts
```

## Component Strategy

[Describe component split principles, e.g., Page → Section → Component]

## API Hook Strategy

[Describe how React Query / SWR / other hooks are used]

## Shared UI Standards

[Describe shared components, design system, etc.]

## Component Structure

<!--
  After writing, run: python3 docs/script/component_to_html.py docs/architecture/frontend.md
-->

```component
title: Frontend Module Structure

component "[Feature] Page" as Page {
  provides: [FeaturePage]
  requires: [Feature] Hook, [Feature] Form
}

component "[Feature] Hook" as Hook {
  provides: use[Feature]
  requires: API Client
}

component "API Client" as API {
  provides: apiGet, apiPost
  requires: Browser Fetch API
}

Page --> Hook : uses
Hook --> API : calls
```
