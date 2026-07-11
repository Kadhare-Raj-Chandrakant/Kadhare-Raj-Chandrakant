#!/usr/bin/env python3
"""
README Dynamic Updater
Fetches live GitHub data and updates README placeholders.
"""

import os
import re
import subprocess
import sys

try:
    import requests
except ImportError:
    print("Installing requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests


def get_env(name, default=None):
    return os.getenv(name, default)


def github_api(url, token):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_stats(username, token):
    stats = {}

    user = github_api(f"https://api.github.com/users/{username}", token)
    stats["followers"] = user.get("followers", 0)
    stats["public_repos"] = user.get("public_repos", 0)

    repos = github_api(f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated", token)
    stats["repos"] = len(repos)

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    stats["stars"] = total_stars

    total_forks = sum(r.get("forks_count", 0) for r in repos)
    stats["forks"] = total_forks

    total_commits = 0
    for repo in repos[:10]:
        try:
            commits = github_api(
                f"https://api.github.com/repos/{username}/{repo['name']}/commits?per_page=1&author={username}",
                token,
            )
            commit_count = int(resp.headers.get("X-Total-Count", 0)) if hasattr(resp := requests.get(
                f"https://api.github.com/repos/{username}/{repo['name']}/commits?per_page=1&author={username}",
                headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
                timeout=15,
            ), "headers") else 0
            total_commits += commit_count
        except Exception:
            pass

    stats["contributions"] = total_commits

    return stats


def update_readme(readme_path, stats):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        "repos": str(stats.get("repos", 8)),
        "followers": str(stats.get("followers", 1)),
        "stars": str(stats.get("stars", 0)),
        "contributions": str(stats.get("contributions", 0)),
    }

    updated = content
    for key, value in replacements.items():
        pattern = rf"(<!-- DYN:{key} -->)(.*?)(<!-- /DYN:{key} -->)"
        updated = re.sub(pattern, rf"\g<1>{value}\3", updated)

    if updated == content:
        print("No changes made to README")
        return False

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"Updated README with: {replacements}")
    return True


def git_commit_and_push(repo_path, message):
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if result.returncode == 0:
            print("No changes to commit")
            return False
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print("Committed and pushed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr.decode() if e.stderr else e}")
        return False
    finally:
        os.chdir(original_dir)


def main():
    username = get_env("GITHUB_USERNAME") or get_env("GITHUB_REPOSITORY", "").split("/")[0]
    token = get_env("GITHUB_TOKEN")

    if not username or not token:
        print("Error: GITHUB_USERNAME and GITHUB_TOKEN are required")
        sys.exit(1)

    readme_path = get_env("README_PATH", "README.md")
    repo_path = get_env("REPO_PATH", ".")

    print(f"Fetching stats for {username}...")
    stats = fetch_stats(username, token)
    print(f"Stats: {stats}")

    print("Updating README...")
    changed = update_readme(readme_path, stats)

    if changed:
        print("Committing and pushing...")
        git_commit_and_push(repo_path, f"chore: update profile stats [{username}]")
    else:
        print("README is already up to date")


if __name__ == "__main__":
    main()
