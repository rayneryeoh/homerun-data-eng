# Homerun data engineering

Data preparation for an agentic system that recommends resale flats.

## Repository layout

- `packages/homerun_geo/`: Python package for ArcPy service areas, school counts and CSV exports.
- `packages/homerun_housing/`: Python package for housing master data, resale transactions, listings and accessibility ingestion.
- `data/raw/`: Original source files, preserved unchanged.
- `data/interim/`: Intermediate processing outputs.
- `data/processed/`: Validated outputs ready for downstream use.
- `configs/`: Portable settings and an example of laptop-specific paths.
- `pipelines/`: Future entry points that coordinate package functions.
- `contracts/`: Dataset conventions and export provenance.
- `tests/`: Future tests using small synthetic fixtures.
- `notebooks/`: Exploratory merges, dataset generation and quality checks.

The processing modules are placeholders. No ingestion, geoprocessing or recommendation pipeline is implemented yet.

## Local development

Use Python 3.10 or later. On this laptop, create a virtual environment and install the housing package:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e packages/homerun_housing
```

For notebook development, install the optional dependencies into your chosen Python environment:

```sh
python -m pip install -e 'packages/homerun_housing[notebooks]'
python -m jupyterlab
```


For geospatial code development, install its package in the same environment:

```sh
python -m pip install -e packages/homerun_geo
```

Installing the geo package does not install ArcPy. Keep ArcPy imports within geospatial implementation modules, so package imports and independent utilities remain usable without ArcGIS.

## Licensed laptop

Copy or clone this repository to the licensed laptop. Use its ArcGIS Pro Python environment, or a suitable clone of that environment, and install the geo package there:

```sh
python -m pip install -e packages/homerun_geo
```

Use a Python version supported by that laptop's ArcGIS installation. ArcPy operations and service-area results must be verified there; this laptop can support editing and verification of logic that does not depend on ArcPy.

Copy `configs/local.example.json` to `configs/local.json` and fill in local paths. Repeat this separately on each laptop. Relative data paths are defined relative to the repository root. Future pipeline entry points should explicitly load these settings; no loader is implemented yet.

## Data workflow

1. Place original housing and spatial inputs in the appropriate `data/raw/` directory.
2. Run the geospatial workflow on the licensed laptop, using `data/interim/` for intermediate outputs.
3. Export accessibility CSVs and their manifests into a dated snapshot under `data/processed/accessibility/`.
4. Transfer those snapshots to the same relative location on this laptop.
5. Prepare housing outputs and join accessibility features through a stable `block_id`.

Actual datasets, geodatabases and generated outputs are excluded from Git. Transfer them separately or use shared storage. Commit only code, configuration templates and documentation; put small synthetic test fixtures under `tests/fixtures/`.

See `contracts/README.md` for dataset and export conventions.

