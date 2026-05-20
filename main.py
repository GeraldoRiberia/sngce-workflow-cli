#!/usr/bin/env python3
"""
vps-status: Check the health of your hosted project across two Hostinger VPS'.

Usage:
    python main.py                  # run backend + frontend sync checks
    python main.py --backend        # backend health checks only
    python main.py --frontend       # frontend sync checks only
    python main.py --ssl            # SSL certificate expiry checks only
    python main.py --watch 30       # re-run every 30 seconds
    python main.py --config path/to/servers.json
"""

import argparse
from html import parser
import json
import os
import time
import sys

from checker.backend import check_backend
from checker.frontend import check_frontend_sync
from checker.ssl_check import check_ssl
import checker.display as display
from checker.usage import usage
DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "config", "servers.json")


def load_config(path: str) -> dict:
    if not os.path.exists(path):
        example = path.replace("servers.json", "servers.example.json")
        display.console.print(
            f"[red]Config file not found:[/] {path}\n"
            f"Copy [dim]{example}[/] to [dim]{path}[/] and fill in your values."
        )
        sys.exit(1)

    with open(path) as f:
        return json.load(f)


def run_checks(config: dict, backend_only: bool = False, frontend_only: bool = False, vps_only: bool = False, ssl_only: bool = False, args=None):
    servers = config.get("servers", {})
    github_token = config.get("github_token")

    display.print_header()
    for key, server in servers.items():
        label = server.get("label", key)
        # --- SSL check ---
        if ssl_only and "frontend_url" in server:
            ssl_result = check_ssl(server["frontend_url"])
            display.print_ssl_result("SSL", ssl_result)

        # --- Backend check ---
        if not frontend_only and not vps_only and not ssl_only and "backend_url" in server:
            backend_result = check_backend(
                url=server["backend_url"],
                health_endpoint=server.get("health_endpoint", "/health"),
            )
            display.print_backend_result(label, backend_result)

        # --- Frontend sync check ---
        if not backend_only and not vps_only and not ssl_only and "frontend_url" in server:
            frontend_result = check_frontend_sync(
                frontend_url=server["frontend_url"],
                repo_name=config["github_repo"],
                branch=config.get("github_branch", "main"),
                version_endpoint=server.get("version_endpoint", "/meta.json"),
                github_token=github_token,
            )
            display.print_frontend_result(label, frontend_result)
        # --- VPS resource usage check ---
        if vps_only and "ip_address" in server and "username" in server:
            vps_result = usage(server,args )
            display.print_vps_result(label, vps_result) 

    display.print_divider()


def main():
    parser = argparse.ArgumentParser(
        description="Check the status of your hosted project VPS'."
    )
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Path to servers.json config")
    parser.add_argument("--backend", action="store_true", help="Run backend checks only")
    parser.add_argument("--frontend", action="store_true", help="Run frontend checks only")
    parser.add_argument("--ssl", action="store_true", help="Run SSL checks only")
    parser.add_argument("--watch", type=int, metavar="SECONDS",
                        help="Re-run checks every N seconds (Ctrl+C to stop)")
    parser.add_argument("--vps-status", action="store_true", help="Check VPS resource usage (disk, memory, nginx status)")
    parser.add_argument("-p", "--password", help="Password for VPS access")

    args = parser.parse_args()
    vps_flags = [args.vps_status]
    if any(vps_flags) and not args.password:
        parser.error("requires -p/--password")
    config = load_config(args.config)

    if args.watch:
        display.console.print(f"[dim]Watching — refreshing every {args.watch}s. Ctrl+C to stop.[/]\n")
        try:
            while True:
                run_checks(config, backend_only=args.backend,ssl_only=args.ssl, frontend_only=args.frontend, vps_only=args.vps_status, args=args)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            display.console.print("\n[dim]Stopped.[/]")
    else:
        run_checks(config, backend_only=args.backend, ssl_only=args.ssl, frontend_only=args.frontend, vps_only=args.vps_status, args=args)


if __name__ == "__main__":
    main()
