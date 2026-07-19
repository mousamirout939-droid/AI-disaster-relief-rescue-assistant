# Monitoring

This project ships with basic file-based logging (`server/logs/app.log`, `server/logs/error.log`)
via `config/logging.py`, plus request timing logs from `middleware/logger.py`.

For production, wire these into a hosted log/metrics service, for example:
- **Render**: built-in log streaming, no extra setup needed.
- **Self-hosted / Kubernetes**: ship `logs/*.log` to something like Loki, ELK, or Datadog
  using a sidecar or log-forwarding agent; scrape `/health` with Prometheus's blackbox exporter.
