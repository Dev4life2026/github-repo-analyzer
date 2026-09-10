import os
import re
import requests
from typing import Tuple, Dict, Any, Optional, List
from app.models import RepoTarget

class GitHubAPIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

def parse_repo_target(target_input: str) -> RepoTarget:
    """
    Parses 'owner/repository' or 'https://github.com/owner/repository' into a RepoTarget.
    """
    cleaned = target_input.strip()
    
    # URL pattern match
    url_pattern = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/\s]+)'
    url_match = re.search(url_pattern, cleaned)
    if url_match:
        owner = url_match.group(1)
        repo = url_match.group(2).removesuffix('.git')
        return RepoTarget(owner=owner, repo=repo)

    # Simple owner/repo match
    simple_pattern = r'^([a-zA-Z0-9_\-\.]+)/([a-zA-Z0-9_\-\.]+)$'
    simple_match = re.match(simple_pattern, cleaned)
    if simple_match:
        return RepoTarget(owner=simple_match.group(1), repo=simple_match.group(2).removesuffix('.git'))

    raise ValueError(f"Invalid repository specification '{target_input}'. Expected format 'owner/repo' or GitHub repository URL.")

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.session = requests.Session()
        auth_token = token or os.getenv("GITHUB_TOKEN")
        if auth_token:
            self.session.headers.update({"Authorization": f"token {auth_token}"})
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Repo-Analyzer/1.0"
        })

    def get_repo_details(self, owner: str, repo: str) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]]]:
        """
        Fetches repository metadata, language breakdown, and root directory tree contents.
        """
        # Fetch metadata
        meta_url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        res = self.session.get(meta_url, timeout=10)
        
        if res.status_code == 404:
            raise GitHubAPIError(f"Repository '{owner}/{repo}' not found or is private.", status_code=404)
        elif res.status_code == 403:
            raise GitHubAPIError("GitHub API rate limit exceeded or access forbidden.", status_code=403)
        elif res.status_code != 200:
            raise GitHubAPIError(f"GitHub API error (HTTP {res.status_code}): {res.text}", status_code=res.status_code)

        repo_data = res.json()

        # Fetch languages
        lang_url = repo_data.get("languages_url", f"{self.BASE_URL}/repos/{owner}/{repo}/languages")
        lang_res = self.session.get(lang_url, timeout=10)
        languages = lang_res.json() if lang_res.status_code == 200 else {}

        # Fetch contents (root directory tree)
        contents_url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents"
        contents_res = self.session.get(contents_url, timeout=10)
        contents = contents_res.json() if contents_res.status_code == 200 and isinstance(contents_res.json(), list) else []

        return repo_data, languages, contents
