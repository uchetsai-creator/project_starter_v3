# architecture/deployment.md

Purpose:
Describe runtime structure — how to run this system locally and how to deploy it.

Include:
- Services
- Environment variables
- Local startup flow
- Build/deploy flow

Avoid:
- Business requirements
- Feature details

---

## Services

| Service | Technology | Port | Description |
|---|---|---|---|
| [e.g., frontend] | [e.g., React / Vite] | [e.g., 5173] | [description] |
| [e.g., backend] | [e.g., Express / Node.js] | [e.g., 4000] | [description] |
| [e.g., database] | [e.g., PostgreSQL 16] | [e.g., 5432] | [description] |
| [e.g., cache] | [e.g., Redis] | [e.g., 6379] | [description] |

---

## Environment Variables

| Variable | Required | Description | Example |
|---|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/db` |
| `JWT_SECRET` | ✅ | Secret for signing JWT tokens | `[random 32-char string]` |
| `[VAR_NAME]` | ✅ / ❌ | [description] | [example value] |

Copy `.env.example` to `.env` and fill in the values before starting.

---

## Local Startup Flow

Prerequisites:
- [e.g., Docker Desktop, Node.js 22+, pnpm]

```bash
# 1. Start infrastructure services
[e.g., docker compose up -d]

# 2. Install dependencies
[e.g., pnpm install]

# 3. Run database migrations
[e.g., pnpm prisma migrate dev]

# 4. Start development servers
[e.g., pnpm dev]
```

Expected state when running:
- [e.g., Frontend available at http://localhost:5173]
- [e.g., Backend API available at http://localhost:4000]
- [e.g., Health check: curl http://localhost:4000/health → {"status":"ok"}]

---

## Build / Deploy Flow

### Build

```bash
[e.g., docker compose build]
[e.g., pnpm build]
```

### Deploy

```bash
[e.g., docker push myapp:latest]
[e.g., kubectl apply -f k8s/]
[e.g., railway up]
```

### Environment

| Environment | URL | Notes |
|---|---|---|
| Local | `http://localhost:[port]` | Docker Compose |
| Staging | `[URL]` | [hosting platform] |
| Production | `[URL]` | [hosting platform] |
