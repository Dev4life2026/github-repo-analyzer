from unittest.mock import patch, MagicMock
from app.analyzer import analyze_repository

@patch("app.analyzer.GitHubClient")
def test_analyze_repository_mocked(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    
    mock_repo_data = {
        "full_name": "Dev4life2026/knowledge-ai",
        "html_url": "https://github.com/Dev4life2026/knowledge-ai",
        "description": "Full-stack AI document intelligence system",
        "private": False,
        "archived": False,
        "stargazers_count": 12,
        "forks_count": 2,
        "open_issues_count": 0,
        "created_at": "2026-09-10T22:00:00Z",
        "pushed_at": "2026-09-10T22:30:00Z",
        "default_branch": "main",
        "language": "Python",
        "license": {"name": "MIT License"}
    }
    
    mock_languages = {"Python": 12000, "TypeScript": 18000}
    mock_contents = [
        {"name": "README.md", "type": "file", "size": 1500},
        {"name": "LICENSE", "type": "file", "size": 1000},
        {"name": "backend", "type": "dir"},
        {"name": ".gitignore", "type": "file"}
    ]

    mock_client.get_repo_details.return_value = (mock_repo_data, mock_languages, mock_contents)

    analysis = analyze_repository("Dev4life2026/knowledge-ai")
    
    assert analysis.full_name == "Dev4life2026/knowledge-ai"
    assert analysis.stars == 12
    assert analysis.has_readme is True
    assert analysis.overall_health_score > 50.0
