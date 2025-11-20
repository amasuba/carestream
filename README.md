# CareStream

AI-Powered Quality of Experience Platform

This repository contains a small demo showing an end-to-end QoE incident scenario:
- Frontend: React (Vite) served by Nginx in Docker
- Backend: Django app with a monitoring demo that simulates Detection → Prediction → Ticket → Notification → Resolution → Follow-up
- ML predictor: small Flask service used by the demo

This README explains how to run the demo locally using Docker Compose and where to interact with it.

## Quick start (recommended)

Prerequisites:
- Docker and Docker Compose installed and running

Start the full stack (build images and run detached):

```bash
docker compose up --build -d --remove-orphans
```

Open the frontend in your browser:

- http://localhost:3005/  (frontend served by Nginx)

APIs available (backend Django):
- GET  /api/sessions/        — list recent sessions
- POST /api/scenario/start   — start the demo scenario (creates a session and runs the simulation)
- GET  /api/scenario/state   — current simulation state, session, tickets, notifications

Other services (optional):
- ML predictor: http://localhost:8002/predict (POST) — called by the backend; a local fallback is used if unreachable
- Demo server (lightweight): http://localhost:8003/

Check logs (helpful during development):

```bash
docker compose logs -f frontend    # frontend logs (nginx)
docker compose logs -f backend     # django backend logs
docker compose logs -f ml-predictor
```

Stop the stack:

```bash
docker compose down
```

## Notes & troubleshooting

- The frontend container serves files with Nginx on container port 80, which is mapped to host port `3005` by default (see `docker-compose.yml`). If `3005` is in use on your machine, change the mapping in `docker-compose.yml`.
- The Django backend uses SQLite by default (development). `docker-compose.yml` includes a Postgres service but Django is not wired to it — if you want Postgres, update `backend/carestream360/settings.py` and the environment accordingly.
- I enabled CORS (`django-cors-headers`) for convenience in the demo. Restrict `CORS_ALLOWED_ORIGINS` before deploying to production.
- If you press **Start Demo Scenario** on the frontend the UI will poll `/api/scenario/state` and display the session, tickets and notifications.

## Development notes

- The frontend source is in `frontend/src/` — built during Docker image creation into `/app/dist` and copied into Nginx's `/usr/share/nginx/html`.
- Backend app lives in `backend/apps/monitoring` and persists demo sessions/tickets/notifications in the configured DB.
- ML predictor service implementation is in `ml_models/predictor.py`.

## Repository

I committed and pushed the changes to `main` on the GitHub repository `https://github.com/amasuba/carestream`.

If you want, I can add healthchecks to `docker-compose.yml`, add a restart/reset button in the UI, or wire Django to Postgres next.

---
