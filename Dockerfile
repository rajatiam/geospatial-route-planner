FROM python:3.13-slim
WORKDIR /app
COPY geospatial_route_planner ./geospatial_route_planner
RUN useradd --uid 10001 --create-home runner
USER runner
WORKDIR /workspace
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "-m", "geospatial_route_planner"]
CMD ["--help"]
