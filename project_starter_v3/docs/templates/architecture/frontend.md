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
  Describes the frontend module dependency structure.
  Fill in based on the actual stack and layer pattern described above.
  Use real layer names from your Stack and Component Strategy sections above.
  e.g. if your stack uses Page → Hook → API Client, use those names.
       if your stack uses View → Store → API, use those names instead.
  After writing, run: python3 docs/script/component_to_html.py docs/architecture/frontend.md
-->

```component
title: Frontend Module Structure

component "[e.g., Page / View / Screen]" as Layer1 {
  provides: [e.g., UI, user interaction]
  requires: Layer2
}

component "[e.g., Hook / Store / ViewModel]" as Layer2 {
  provides: [e.g., state, data fetching]
  requires: Layer3
}

component "[e.g., API Client / HTTP Layer]" as Layer3 {
  provides: [e.g., HTTP calls]
  requires: [e.g., Auth Token, Backend]
}

Layer1 --> Layer2 : uses
Layer2 --> Layer3 : calls
```
