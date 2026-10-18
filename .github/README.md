# GitHub Project Configuration

- `workflows/ci-cd.yml`: backend lint/tests, MySQL migration validation, Compose gateway smoke test, GHCR publishing, and optional SSH deployment.
- `dependabot.yml`: weekly updates for GitHub Actions, Python dependencies, and backend/gateway Docker images.

Deployment remains disabled unless the repository variable `DEPLOY_ENABLED=true` and the documented deployment secrets are configured.