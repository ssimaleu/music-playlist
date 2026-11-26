# CI/CD Workflow Documentation — Playlist Manager

This project uses **GitHub Actions** to automate testing and delivery.

## Pipeline Overview

```
push / pull request ──> [CI: ci.yml]            test on Python 3.10 & 3.12
                                   │
                                   ▼ (all green = merge allowed)
tag v* push ──────────> [CD: cd.yml]            re-run tests (gate)
                                   │
                                   ▼
                            package app as zip ──> GitHub Release
```

## Workflows

### 1. Continuous Integration — `.github/workflows/ci.yml`

| | |
|---|---|
| **Trigger** | `push` to `main`, and every `pull_request` targeting `main` |
| **Runner** | `ubuntu-latest` |
| **Strategy** | Matrix across Python `3.10` and `3.12` |
| **Steps** | 1. `actions/checkout@v4` — fetch code<br>2. `actions/setup-python@v5` — install Python<br>3. `python -m unittest -v` — run unit tests<br>4. Smoke test the CLI |

Purpose: every change is verified before it lands on `main`. A failing
pipeline blocks the pull request from being merged.

### 2. Continuous Delivery — `.github/workflows/cd.yml`

| | |
|---|---|
| **Trigger** | push of a version tag (`v*`, e.g. `v1.0.0`) |
| **Runner** | `ubuntu-latest` |
| **Steps** | 1. Checkout → 2. Setup Python → 3. **Re-run tests as a release gate** → 4. `zip` the app into `dist/` → 5. Create a GitHub Release with the artifact and auto-generated notes |

Purpose: publishing a release is fully automated. To ship a version:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The CD workflow then builds and attaches `playlist-v1.0.0.zip` to a new
GitHub Release.

## How to run it yourself

1. Create a GitHub repository and push this project:
   ```bash
   git remote add origin git@github.com:<user>/music-playlist.git
   git push -u origin main
   ```
2. Open the **Actions** tab on GitHub — the CI workflow runs on every push.
3. To test the CD workflow, push a tag as shown above.

## Possible extensions

- Add `ruff` / `flake8` linting and `black` format checks to CI.
- Add a `docker build` + push job for containerized deployment.
- Add branch protection rules requiring CI to pass before merging.
