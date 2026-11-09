# Accounts Microservice DevOps Capstone

![CI](https://github.com/RONAK4YOU/devops-capstone-accounts/actions/workflows/ci-build.yaml/badge.svg)

A small Flask REST API for managing accounts, built with tests, security headers, GitHub Actions, Docker, Kubernetes, and Tekton deployment examples.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate  |  macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
flask --app service run --port 8080
```

`GET /` returns service status. Account endpoints are under `/accounts`.

## Test and quality

```bash
nosetests --with-coverage --cover-package=service
flake8 service tests
pylint service
```

## Docker

```bash
docker build -t accounts:1.0 .
docker run --rm -p 8080:8080 accounts:1.0
```

## Kubernetes and Tekton

Manifests are in `k8s/` and `tekton/`. Apply to a configured cluster with `kubectl apply -f k8s/` and install/run the Tekton resources using the commands in `tekton/README.md`.

## User stories

See [user-story.md](user-story.md) for the story template and [docs/project-board.md](docs/project-board.md) for the backlog and sprint plan.

