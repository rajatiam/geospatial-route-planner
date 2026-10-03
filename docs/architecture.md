# Geospatial Route Planner: architecture

## Dijkstra with stable tie ordering

The supplied network is a directed weighted graph. Validation prohibits negative/nonfinite weights, duplicate edges and unknown nodes. A heap explores the current cheapest path; blocked links are excluded. Stable path ordering makes equal-cost decisions reproducible.

## Module boundaries

`geospatial_route_planner/core.py` contains the algorithm and persistence operations. `cli.py` validates arguments and prints JSON. The package entrypoint translates input and storage errors into structured stderr with exit status 2. Domain-specific unsuccessful results can use exit status 1. There is no shared runtime dependency on the portfolio folder.

## Failure and operational boundaries

A destination may be unreachable, which is reported explicitly with an empty path and exit status 1. Zero-cost cycles terminate through settled-node tracking. Costs are supplied model values; real geospatial routing would require road data, coordinate systems and additional constraints.

## Verification

Core tests cover valid results and failure boundaries. Process-level CLI tests run the committed examples in temporary copies, inspect JSON output and verify domain outcomes. CI runs on Python 3.11 and 3.13, Linux and Windows, checks package installation, and builds and executes the non-root Docker image.

## Extension choices

The standard-library implementation keeps local execution inspectable and offline. A hosted or distributed version would require workload-specific authorization, resource limits, durable coordination and observability. Extend the core through tested functions rather than adding infrastructure without a scaling requirement.
