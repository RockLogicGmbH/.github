from __future__ import annotations

import base64
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

import requests

load_dotenv()

GITHUB_API = "https://api.github.com"
ORG = os.environ["GITHUB_ORG"]
TOKEN = os.environ["GITHUB_TOKEN"]

SOURCE_FILE = Path(__file__).with_name("sync-labels.yml")
TARGET_PATH = ".github/workflows/sync-labels.yml"
DRY_RUN = "--dry-run" in sys.argv

COMMIT_MESSAGE = "CHORE: sync sync-labels.yml workflow"
PR_TITLE = "CHORE: sync sync-labels.yml workflow"
PR_BODY = "This PR rolls out the sync-labels.yml workflow file."
BRANCH_NAME = "chore/sync-labels-workflow"


def github_headers() -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def list_repos(org: str) -> list[dict]:
    repos = []
    page = 1

    while True:
        response = requests.get(
            f"{GITHUB_API}/orgs/{org}/repos",
            headers=github_headers(),
            params={"per_page": 100, "page": page},
            timeout=30,
        )
        response.raise_for_status()

        batch = response.json()
        if not batch:
            break

        repos.extend(batch)
        page += 1

    return repos


def get_branch(owner: str, repo: str, branch: str) -> dict:
    response = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/branches/{branch}",
        headers=github_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def create_branch(owner: str, repo: str, branch: str, sha: str) -> None:
    response = requests.post(
        f"{GITHUB_API}/repos/{owner}/{repo}/git/refs",
        headers=github_headers(),
        json={"ref": f"refs/heads/{branch}", "sha": sha},
        timeout=30,
    )

    # 422 usually means the branch already exists
    if response.status_code not in (201, 422):
        response.raise_for_status()


def get_file(owner: str, repo: str, path: str, ref: str) -> dict | None:
    response = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
        headers=github_headers(),
        params={"ref": ref},
        timeout=30,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()


def put_file(owner: str, repo: str, path: str, content: bytes, branch: str, sha: str | None) -> None:
    payload = {
        "message": COMMIT_MESSAGE,
        "content": base64.b64encode(content).decode("utf-8"),
        "branch": branch,
    }

    if sha:
        payload["sha"] = sha

    response = requests.put(
        f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
        headers=github_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()


def create_pr(owner: str, repo: str, head: str, base: str) -> str | None:
    response = requests.post(
        f"{GITHUB_API}/repos/{owner}/{repo}/pulls",
        headers=github_headers(),
        json={
            "title": PR_TITLE,
            "head": head,
            "base": base,
            "body": PR_BODY,
        },
        timeout=30,
    )

    # 422 usually means PR already exists or no diff
    if response.status_code == 422:
        return None

    response.raise_for_status()
    return response.json()["html_url"]


def main() -> int:
    if not SOURCE_FILE.exists():
        print(f"Source file not found: {SOURCE_FILE}", file=sys.stderr)
        return 1

    content = SOURCE_FILE.read_bytes()

    try:
        repos = list_repos(ORG)
    except requests.HTTPError as error:
        print(f"Failed to list repositories: {error}", file=sys.stderr)
        return 1

    for repo in repos:
        repo_name = repo["name"]
        owner = repo["owner"]["login"]
        default_branch = repo["default_branch"]

        try:
            branch_info = get_branch(owner, repo_name, default_branch)
            base_sha = branch_info["commit"]["sha"]

            existing = get_file(owner, repo_name, TARGET_PATH, default_branch)
            existing_sha = existing["sha"] if existing else None

            if DRY_RUN:
                action = "UPDATE" if existing else "CREATE"
                print(
                    f"[DRY-RUN] {action} {owner}/{repo_name}:{TARGET_PATH} "
                    f"on branch {BRANCH_NAME} -> PR to {default_branch}"
                )
                continue

            create_branch(owner, repo_name, BRANCH_NAME, base_sha)

            put_file(owner, repo_name, TARGET_PATH, content, BRANCH_NAME, existing_sha)
            pr_url = create_pr(owner, repo_name, BRANCH_NAME, default_branch)

            if pr_url:
                print(f"PR CREATED {owner}/{repo_name}: {pr_url}")
            else:
                print(f"SKIPPED {owner}/{repo_name}: PR already exists or no changes")

        except requests.HTTPError as error:
            print(f"FAILED {owner}/{repo_name}: {error}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())