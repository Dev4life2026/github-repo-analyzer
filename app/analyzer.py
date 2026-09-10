from app.client import GitHubClient, parse_repo_target
from app.scorer import calculate_heuristic_scores
from app.models import RepositoryAnalysis

def analyze_repository(target_input: str, token: str = None) -> RepositoryAnalysis:
    """
    Parses repository target, fetches GitHub API data, and builds structured analysis report.
    """
    target = parse_repo_target(target_input)
    client = GitHubClient(token=token)
    
    repo_data, languages, contents = client.get_repo_details(target.owner, target.repo)
    category_scores, overall_score = calculate_heuristic_scores(repo_data, languages, contents)

    content_names = [c.get("name", "").lower() for c in contents if isinstance(c, dict)]
    readme_item = next((c for c in contents if c.get("name", "").lower().startswith("readme")), None)

    return RepositoryAnalysis(
        full_name=repo_data.get("full_name", f"{target.owner}/{target.repo}"),
        html_url=repo_data.get("html_url", f"https://github.com/{target.owner}/{target.repo}"),
        description=repo_data.get("description") or "No description provided.",
        is_private=repo_data.get("private", False),
        is_archived=repo_data.get("archived", False),
        stars=repo_data.get("stargazers_count", 0),
        forks=repo_data.get("forks_count", 0),
        open_issues=repo_data.get("open_issues_count", 0),
        created_at=repo_data.get("created_at", "")[:10],
        updated_at=repo_data.get("updated_at", "")[:10],
        pushed_at=repo_data.get("pushed_at", "")[:10],
        default_branch=repo_data.get("default_branch", "main"),
        license=repo_data.get("license", {}).get("name") if repo_data.get("license") else "None",
        primary_language=repo_data.get("language") or "Unknown",
        languages=languages,
        has_readme=readme_item is not None,
        readme_size_bytes=readme_item.get("size", 0) if readme_item else 0,
        has_license=bool(repo_data.get("license")) or any("license" in name for name in content_names),
        has_ci_config=any(name in [".github", ".travis.yml", ".circleci"] for name in content_names),
        has_tests=any(name in ["test", "tests", "spec", "specs"] for name in content_names),
        has_contributing=any("contributing" in name for name in content_names),
        has_env_example=any(name in [".env.example", ".env.sample"] for name in content_names),
        category_scores=category_scores,
        overall_health_score=overall_score
    )
