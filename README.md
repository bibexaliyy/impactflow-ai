# ImpactFlow AI

AI-powered report generator for NGOs, CSOs, and CBOs which turns structured
project inputs into donor-ready reports, exportable as Word or PDF.

## Stack

Django (monolith) · Postgres · Tailwind + htmx · Claude API · python-docx · weasyprint

One language, one codebase, one deploy  built for a solo builder + AI
co-builder to maintain long-term without splitting focus across a
separate frontend/backend stack. See project notes for the reasoning.

## App structure

- **accounts** — `Organization` (the multi-tenancy boundary) + custom `User` model, signup/login
- **projects** — the structured intake form (objectives, activities, participants, outcomes, challenges, lessons, success story)
- **ai_engine** — the Claude API call and prompt template; the only place in the codebase that talks to the AI
- **reports** — the generated `Report` model (9 sections) + download endpoints
- **exports** — DOCX (python-docx) and PDF (weasyprint, from a shared HTML template) generation

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then fill in ANTHROPIC_API_KEY at minimum

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/accounts/signup/` to create your first
organization + user, then `/` to create a project and generate a report.

No `DATABASE_URL` set → falls back to SQLite automatically, so you can
develop without standing up Postgres. Set `DATABASE_URL` once you're
ready to test against Postgres or deploy.

## What's already wired up

- Multi-tenant data model (every Project/Report scoped to an Organization) from day one
- Custom User model (painful to add later, free now)
- AI call with retry + backoff, and a defined error path if generation fails (never fails silently on a donor-facing doc)
- One HTML template shared between the web preview and the PDF export, so both stay visually consistent
- htmx-powered "Generate Report" button — no separate frontend build, still feels interactive

## Not built yet — next priorities

- Report editing (currently generate → export only, no in-app editing of AI output)
- Team invites (multiple users per Organization — the model supports it, the UI doesn't yet)
- Billing/plans (Organization has a `plan` field, no Stripe integration yet)
- Tests
- Production deploy config (Render/Railway) — `gunicorn` and `whitenoise` are in requirements.txt, not yet configured

## Deployment notes

- `weasyprint` needs system-level dependencies (Pango, Cairo) — most PaaS
  buildpacks (Render, Railway) handle this, but confirm before relying on it in production.
- Set `DEBUG=False` and a real `SECRET_KEY` before deploying anywhere public.
