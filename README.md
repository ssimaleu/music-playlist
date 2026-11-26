# Playlist Manager 🎵

A simple Python CLI app for managing a music playlist — built as a
CI/CD lab exercise with GitHub Actions.

## Features

- Add songs (title, artist, duration in seconds)
- Compute total playlist playtime
- Filter songs by artist
- Sort songs by duration
- Export the playlist as JSON

## Usage

```bash
python main.py add "Ocean Eyes" "Billie Eilish" 200
python main.py total            # e.g. 0:00 for empty playlist
```

## Run tests

```bash
python -m unittest -v
```

## CI/CD

GitHub Actions workflows live in `.github/workflows/`:

- `ci.yml` — runs unit tests on Python 3.10 & 3.12 for every push/PR
- `cd.yml` — packages the app and creates a GitHub Release on `v*` tags

See [CI_CD.md](CI_CD.md) for the full pipeline documentation.

> Note: this is a standalone exercise project, separate from the group project.
