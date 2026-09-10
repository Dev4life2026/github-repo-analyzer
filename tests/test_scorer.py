from app.scorer import calculate_heuristic_scores

def test_calculate_heuristic_scores_complete_repo():
    repo_data = {
        "full_name": "owner/repo",
        "archived": False,
        "pushed_at": "2026-09-10T10:00:00Z",
        "language": "Python",
        "license": {"spdx_id": "MIT"}
    }
    languages = {"Python": 10000}
    contents = [
        {"name": "README.md", "type": "file", "size": 1200},
        {"name": "LICENSE", "type": "file", "size": 1000},
        {"name": "CONTRIBUTING.md", "type": "file", "size": 500},
        {"name": "tests", "type": "dir"},
        {"name": ".github", "type": "dir"},
        {"name": ".gitignore", "type": "file"},
        {"name": ".env.example", "type": "file"}
    ]

    categories, overall_score = calculate_heuristic_scores(repo_data, languages, contents)
    assert len(categories) == 4
    assert overall_score > 85.0
    assert any(cat.category == "Documentation" for cat in categories)

def test_calculate_heuristic_scores_bare_repo():
    repo_data = {"full_name": "owner/bare", "archived": True, "pushed_at": "", "language": None}
    languages = {}
    contents = []

    categories, overall_score = calculate_heuristic_scores(repo_data, languages, contents)
    assert overall_score < 40.0
