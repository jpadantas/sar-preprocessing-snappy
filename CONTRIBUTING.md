# Contributing

Thanks for your interest!

## Setup
1. Install SNAP and configure `snappy-conf`.
2. Create a virtualenv and install `requirements.txt`.

## Development
- Keep functions pure and modular.
- Prefer small PRs focused on one change.
- Add docstrings and comments for SNAP operator parameters.

## Testing
- Use a small SAR sample file (e.g., a clipped product) to validate the pipeline.
- Verify output GeoTIFF opens in QGIS.

## Commit
Use conventional messages when possible:
- feat: add new feature
- fix: bug fix
- docs: documentation only
