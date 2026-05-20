from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime

console = Console()


def _status_icon(ok: bool) -> str:
    return "[bold green]✔[/]" if ok else "[bold red]✘[/]"


def print_header():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(Panel(f"[bold]VPS Status Check[/]  [dim]{now}[/]", box=box.ROUNDED))


def print_backend_result(label: str, result: dict):
    console.print(f"\n[bold underline]{label}[/]")

    if result["reachable"] and not result["error"]:
        console.print(f"  {_status_icon(True)} Reachable  "
                      f"[dim]status {result['status_code']}[/]  "
                      f"[dim]Response Time: {result['response_time_ms']}ms[/]")
    elif result["reachable"] and result["error"]:
        # Reachable but bad status
        console.print(f"  [bold yellow]⚠[/] Degraded  "
                      f"[dim]{result['error']}[/]  "
                      f"[dim]{result['response_time_ms']}ms[/]")
    else:
        console.print(f"  {_status_icon(False)} Unreachable  [red]{result['error']}[/]")


def print_ssl_result(label: str, result: dict):
    console.print(f"\n[bold underline]{label} — SSL Certificate[/]")

    if result["error"]:
        console.print(f"  {_status_icon(False)} Error: [red]{result['error']}[/]")
        return

    days = result["days_remaining"]
    expires = result["expires_on"]

    if days > 30:
        color = "green"
        icon = _status_icon(True)
    elif days > 7:
        color = "yellow"
        icon = "[bold yellow]⚠[/]"
    else:
        color = "red"
        icon = _status_icon(False)

    console.print(f"  {icon} [{color}]{days} days remaining[/]  [dim]expires {expires}[/]")


def print_repo_result(label: str, result: dict):
    console.print(f"\n[bold underline]{label} — Repo Sync[/]")

    if result["error"]:
        console.print(f"  {_status_icon(False)} Error: [red]{result['error']}[/]")
        return

    deployed = result["deployed_commit"][:7] if result["deployed_commit"] else "unknown"
    latest = result["latest_commit"][:7] if result["latest_commit"] else "unknown"

    if result["in_sync"]:
        console.print(f"  {_status_icon(True)} Up to date  [dim]commit {deployed}[/]")
    else:
        console.print(f"  {_status_icon(False)} Out of sync  "
                      f"[red]deployed {deployed}[/] → [green]latest {latest}[/]")

def print_vps_result(label: str, result: dict):
    console.print(f"\n[bold underline]{label} — VPS Resource Usage[/]")

    # if result["error"]:
    #     console.print(f"  {_status_icon(False)} Error: [red]{result['error']}[/]")
    #     return

    disk = result.get("disk_usage", "N/A")
    memory = result.get("memory_usage", "N/A")
    nginx = result.get("nginx_status", "N/A")

    console.print(f"\n[red]Disk Usage: [white]\n{disk}  \n\n[blue]Memory Usage: \n[white]{memory}  \n\n[yellow]Nginx: \n[white]{nginx}")
def print_divider():
    console.print()
