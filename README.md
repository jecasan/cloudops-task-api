# TaskFlow

> A production-grade task management API demonstrating end-to-end DevOps practices.

[![CI](https://github.com/YOUR_USERNAME/taskflow/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/taskflow/actions/workflows/ci.yml)
[![Security](https://img.shields.io/badge/security-trivy%20%7C%20checkov%20%7C%20gitleaks-blue)](docs/adr/)

## Stack

| Layer | Tool |
|---|---|
| API | FastAPI + Python 3.12 |
| Database | PostgreSQL 15 |
| Containers | Docker (multi-stage) |
| IaC | Terraform + AWS Free Tier |
| Orchestration | Kubernetes (Minikube) + ArgoCD |
| CI/CD | GitHub Actions |
| Observability | Prometheus + Grafana + Loki |

## Quick start

```bash
cp .env.example .env          # fill in your values
docker compose up --build
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Documentation

Full docs at [YOUR_USERNAME.github.io/taskflow](https://YOUR_USERNAME.github.io/taskflow)

- [Architecture](docs/adr/)
- [Runbooks](docs/runbooks/)
- [Contributing](CONTRIBUTING.md)
