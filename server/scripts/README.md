# scripts/

Operational CLI helpers for this backend. Run all from `server/` (or via the shell
wrappers, which `cd` into place automatically).

**Database**: `seed_database.py`, `create_demo_users.py`, `create_admin.py`,
`check_database.py`, `reset_database.py`, `clean_database.py`, `backup_database.py`,
`restore_database.py`, `generate_fake_data.py`

**AI pipeline**: `preprocess_dataset.py`, `train_ai_model.py`, `evaluate_ai_model.py`,
`check_ai_model.py`, `export_model.py`, `download_dataset.py`

**Ops / messaging**: `check_api_health.py`, `check_server.py`, `send_notifications.py`,
`send_alerts.py`, `cron_jobs.py`, `generate_reports.py`

**Process management (shell)**: `install-dependencies.sh`, `build_backend.sh`,
`build_frontend.sh`, `start_backend.sh`, `start_frontend.sh`, `start_project.sh`,
`stop_project.sh`, `restart_project.sh`, `update_dependencies.sh`
