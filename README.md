# sngce-workflow-cli

A CLI tool to check the health of Sngce Workflow across Hostinger VPS.

It can validate:
- Backend health endpoint reachability and response time
- Frontend deployment sync by comparing deployed commit to GitHub
- SSL certificate expiry for frontend URLs via `--ssl`
- VPS resource usage via SSH (disk, memory, nginx status)

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create your config
```bash
cp config/servers.example.json config/servers.json
```

Edit `config/servers.json` with your actual values.

---

## Usage

```bash
# Runs (Frontend + Backend Checks by Default)
python main.py

# Backend checks only (health checks for backend URLs)
python main.py --backend

# Repo sync checks  (Frontend + Backend Repo sync checks)
python main.py --repo

# SSL certificate expiry checks only
python main.py --ssl

# VPS resource usage checks only
python main.py --vps-status -p YOUR_PASSWORD

# Watch mode — re-run every 30 seconds
python main.py --watch 30

# Watch only backend checks
python main.py --backend --watch 30

# Custom config location
python main.py --config /path/to/myconfig.json
```

### Notes
- `--backend` runs backend health checks only.
- `--repo` runs repo sync checks for frontend and backend.
- `--ssl` runs SSL certificate expiry checks only for `frontend_url` entries.
- `--vps-status` runs SSH-based VPS checks for servers with `ip_address` and `username`.
- `-p/--password` is required when `--vps-status` is used.
- Use `--config` to point to a custom config file instead of `config/servers.json`.

---

## Config reference

```json
{
  "servers": {
    "vps1": {
      "label": "Backend (VPS 1)",
      "backend_url": "https://api.yourproject.com",
      "health_endpoint": "/health",
      "github_repo": "yourusername/your-backend-repo",
      "github_branch": "main",
      "ip_address" : "187.xxx.xxx.xxx",
      "username" : "username"
    },
    "vps2": {
      "label": "Frontend (VPS 2)",
      "frontend_url": "https://yourproject.com",
      "version_endpoint": "/meta.json",
      "github_repo": "yourusername/your-frontend-repo",
      "github_branch": "main",
      "ip_address" : "187.xxx.xxx.xxx",
      "username" : "username"
    }
  },
  "github_token": "your_github_token_here"
}
```

### Config field details
- `label`: Friendly name for the server.
- `backend_url`: Base URL for backend health checks.
- `health_endpoint`: Health endpoint path (default: `/health`).
- `frontend_url`: Base URL for frontend/SSL checks.
- `version_endpoint`: Endpoint returning deployed commit metadata (default: `/meta.json`).
- `github_repo`: GitHub repo slug, e.g. `owner/repo`.
- `github_branch`: Branch to compare against (default: `main`).
- `ip_address`: IP for SSH VPS checks.
- `username`: SSH user for VPS checks.
- `github_token`: Optional GitHub token for authenticated API access and higher GitHub rate limits.

---

## Dependencies

The project depends on:
- `requests`
- `rich`
- `PyGithub`
- `paramiko`



