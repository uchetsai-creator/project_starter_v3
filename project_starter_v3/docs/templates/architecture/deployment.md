# architecture/deployment.md

Purpose:
Describe runtime structure — how to run this system locally and how to deploy it.

Include:
- Services
- Environment variables
- Local startup flow
- Build/deploy flow
- Verification steps

Avoid:
- Business requirements
- Feature details

---

## Services

<!--
  List every service that needs to be running for the system to work.
  Port is optional — omit if not applicable (e.g. serverless, managed services).

  Examples:
    frontend    React / Vite          5173   serves the UI
    backend     Express / Node.js     4000   REST API
    database    PostgreSQL 16         5432   primary data store
    cache       Redis 7               6379   session and query cache
    queue       RabbitMQ              5672   async job queue
    worker      BullMQ worker         —      processes background jobs
    storage     MinIO (S3-compatible) 9000   file uploads (local only; S3 in prod)
-->

| Service | Technology | Port | Description |
|---|---|---|---|
| [service name] | [technology and version] | [port or —] | [description] |

---

## Environment Variables

<!--
  List every environment variable the system reads.
  Remove DATABASE_URL and JWT_SECRET if your project does not use them —
  these are examples, not requirements.
  Add all variables your project actually uses.
-->

| Variable | Required | Description | Example |
|---|---|---|---|
| `[VAR_NAME]` | ✅ | [what it controls] | `[example value]` |
| `[VAR_NAME]` | ❌ | [what it controls, and what the default is] | `[example value]` |

Copy `.env.example` to `.env` and fill in the values before starting.

---

## Local Startup Flow

<!--
  List the exact commands to get the system running locally.
  Adapt to whatever tools and package manager this project uses.
  Remove steps that don't apply (e.g. no migrations for a document DB).

  Common patterns:
    Docker Compose:   docker compose up -d
    Node.js:          npm install / pnpm install / yarn
    Python:           pip install -r requirements.txt / poetry install
    Go:               go mod download
    Ruby:             bundle install
    Migrations:       prisma migrate dev / rails db:migrate / alembic upgrade head / go run ./cmd/migrate
    Dev server:       npm run dev / python manage.py runserver / go run . / rails server
-->

Prerequisites:
- [required tools and versions, e.g., Docker Desktop, Node.js 22+, Python 3.12+]

```bash
# 1. [Step description]
[command]

# 2. [Step description]
[command]

# 3. [Step description]
[command]
```

Expected state when running:
- [service] available at [URL or description]
- [health check command and expected output]

---

## Build / Deploy Flow

<!--
  Describe how to build and deploy the system.
  Adapt to whatever CI/CD and hosting platform this project uses.

  Examples:
    docker compose build && docker push myapp:latest
    pnpm build → deploy to Vercel via git push
    go build -o bin/server → rsync to VPS
    railway up
    fly deploy
    kubectl apply -f k8s/
    serverless deploy
    eb deploy
-->

### Build

```bash
[build command(s)]
```

### Deploy

```bash
[deploy command(s)]
```

### Environments

| Environment | URL | Notes |
|---|---|---|
| Local | `http://localhost:[port]` | [local setup description] |
| Staging | `[URL]` | [hosting platform] |
| Production | `[URL]` | [hosting platform] |

---

## Verification

How to confirm the system is running correctly after startup.

- [ ] **[What to verify]**
  Run: `[exact command]`
  Expected: `[exact output]`

---

## Teardown

```bash
[command to stop all services]
```
