import requests
from github import Github, GithubException


def get_deployed_commit(url: str, version_endpoint: str = "/meta.json", timeout: int = 10) -> dict:
    """
    Fetches the deployed commit SHA from the frontend's version endpoint.
    Expects the endpoint to return JSON like: { "commit": "abc1234..." }
    Returns a dict with: commit, error
    """
    full_url = url.rstrip("/") + version_endpoint
    result = {"commit": None, "error": None}

    try:
        response = requests.get(full_url, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        commit = data.get("commit") or data.get("sha") or data.get("version")
        if not commit:
            result["error"] = f"No 'commit'/'sha'/'version' key found in response: {data}"
        else:
            result["commit"] = commit

    except requests.exceptions.ConnectionError:
        result["error"] = "Frontend unreachable"
    except requests.exceptions.Timeout:
        result["error"] = f"Timed out after {timeout}s"
    except ValueError:
        result["error"] = f"{version_endpoint} did not return valid JSON"
    except requests.exceptions.HTTPError as e:
        result["error"] = f"HTTP error: {e}"

    return result


def get_latest_repo_commit(repo_name: str, branch: str = "main", github_token: str = None) -> dict:
    """
    Fetches the latest commit SHA from a GitHub repo branch.
    Returns a dict with: commit, error
    """
    result = {"commit": None, "error": None}

    try:
        g = Github(github_token) if github_token else Github()
        repo = g.get_repo(repo_name)
        branch_obj = repo.get_branch(branch)
        result["commit"] = branch_obj.commit.sha
    except GithubException as e:
        print(e)
        result["error"] = f"GitHub API error: {e.data.get('message', str(e))}"
    except Exception as e:
        result["error"] = str(e)

    return result


def check_repo_sync(
    url: str,
    repo_name: str,
    branch: str = "main",
    version_endpoint: str = "/meta.json",
    github_token: str = None,
) -> dict:
    """
    Compares the deployed commit on the frontend against the latest commit on GitHub.
    Returns a dict with: in_sync, deployed_commit, latest_commit, error
    """
    result = {
        "in_sync": None,
        "deployed_commit": None,
        "latest_commit": None,
        "error": None,
    }

    deployed = get_deployed_commit(url, version_endpoint)
    if deployed["error"]:
        result["error"] = f"Could not fetch deployed version: {deployed['error']}"
        return result

    latest = get_latest_repo_commit(repo_name, branch, github_token)
    if latest["error"]:
        result["error"] = f"Could not fetch GitHub commit: {latest['error']}"
        return result

    result["deployed_commit"] = deployed["commit"]
    result["latest_commit"] = latest["commit"]

    # Compare just the first 7 chars if lengths differ (short SHA vs full SHA)
    deployed_short = deployed["commit"][:7]
    latest_short = latest["commit"][:7]
    result["in_sync"] = deployed_short == latest_short

    return result
