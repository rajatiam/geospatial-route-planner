# Geospatial Route Planner

Weighted graph routing with blocked links and deterministic shortest paths. An independent Python 3.11+ project using the standard library, with a real command-line interface and no runtime package dependencies.

## Run locally

From the cloned repository, run:

```sh
python -m geospatial_route_planner route examples/network.json depot customer
python -m geospatial_route_planner route examples/network.json depot customer --blocked depot:bridge
python -m geospatial_route_planner validate examples/network.json
```

Examples contain synthetic data. First use requires no cloud account, API key or package download. Optionally install the CLI using `python -m pip install .` and run `geospatial-route-planner --help`.

## Verify

```sh
python -m unittest discover -v
```

GitHub Actions checks Python 3.11 and 3.13 on Linux and Windows, verifies package installation, and builds/runs the non-root Docker image.

```sh
docker build -t geospatial-route-planner .
docker run --rm geospatial-route-planner --help
```

Mount a working directory at `/workspace` to process your own files. The container runs as UID 10001; provide appropriate write permissions for outputs.

## Architecture and scope

Business algorithms live in `geospatial_route_planner/core.py`; `geospatial_route_planner/cli.py` owns argument parsing and JSON output. Tests exercise success cases and failure boundaries, with temporary storage for mutations. See [design decisions](docs/architecture.md).

Uses Dijkstra over supplied directed nonnegative costs; it does not query maps or calculate road geometry. Results are deterministic and provide the traversed path and total modeled cost.

This project demonstrates implemented engineering practices. It does not claim production deployment history or external certifications.
