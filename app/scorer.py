from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
from app.models import HeuristicCategoryScore

def calculate_heuristic_scores(
    repo_data: Dict[str, Any],
    languages: Dict[str, int],
    contents: List[Dict[str, Any]]
) -> Tuple[List[HeuristicCategoryScore], float]:
    """
    Evaluates repository against transparent heuristic quality & structure categories.
    """
    content_names = [c.get("name", "").lower() for c in contents if isinstance(c, dict)]
    content_types = {c.get("name", "").lower(): c.get("type", "") for c in contents if isinstance(c, dict)}

    readme_item = next((c for c in contents if c.get("name", "").lower().startswith("readme")), None)
    has_readme = readme_item is not None
    readme_size = readme_item.get("size", 0) if readme_item else 0
    has_license = bool(repo_data.get("license")) or any("license" in name for name in content_names)
    has_contributing = any("contributing" in name for name in content_names)
    has_tests = any(name in ["test", "tests", "spec", "specs", "pytest.ini"] for name in content_names)
    has_ci = any(name in [".github", ".travis.yml", ".circleci", "Jenkinsfile"] for name in content_names)
    has_gitignore = ".gitignore" in content_names
    has_env_example = any(name in [".env.example", ".env.sample", ".env.template"] for name in content_names)

    categories: List[HeuristicCategoryScore] = []

    # 1. Documentation Category (Weight: 30)
    doc_passed, doc_failed = [], []
    doc_score = 0.0
    if has_readme:
        doc_score += 12.0
        doc_passed.append("README file exists")
        if readme_size > 300:
            doc_score += 8.0
            doc_passed.append(f"Comprehensive README size ({readme_size} bytes)")
        else:
            doc_failed.append("README size is small (< 300 bytes)")
    else:
        doc_failed.append("Missing README file")

    if has_license:
        doc_score += 6.0
        doc_passed.append(f"Open source License defined ({repo_data.get('license', {}).get('spdx_id', 'Custom')})")
    else:
        doc_failed.append("Missing License file")

    if has_contributing:
        doc_score += 4.0
        doc_passed.append("CONTRIBUTING guidelines present")
    else:
        doc_failed.append("Missing CONTRIBUTING guidelines")

    categories.append(HeuristicCategoryScore(
        category="Documentation",
        score=round((doc_score / 30.0) * 100, 1),
        passed_checks=doc_passed,
        failed_checks=doc_failed
    ))

    # 2. Testing & QA Category (Weight: 25)
    test_passed, test_failed = [], []
    test_score = 0.0
    if has_tests:
        test_score += 15.0
        test_passed.append("Dedicated test directory / configuration found")
    else:
        test_failed.append("No explicit test directory (tests/, spec/) detected in root")

    if has_ci:
        test_score += 10.0
        test_passed.append("Continuous Integration (CI) configuration found")
    else:
        test_failed.append("Missing CI workflow (.github/workflows or Travis/CircleCI)")

    categories.append(HeuristicCategoryScore(
        category="Testing & Quality Assurance",
        score=round((test_score / 25.0) * 100, 1),
        passed_checks=test_passed,
        failed_checks=test_failed
    ))

    # 3. Maintenance & Activity Category (Weight: 25)
    maint_passed, maint_failed = [], []
    maint_score = 0.0
    
    if not repo_data.get("archived", False):
        maint_score += 10.0
        maint_passed.append("Active non-archived repository")
    else:
        maint_failed.append("Repository is archived")

    pushed_at = repo_data.get("pushed_at", "")
    if pushed_at:
        maint_score += 10.0
        maint_passed.append(f"Recent push activity ({pushed_at[:10]})")
    else:
        maint_failed.append("No recorded push timestamps")

    if repo_data.get("language"):
        maint_score += 5.0
        maint_passed.append(f"Primary language defined ({repo_data.get('language')})")
    else:
        maint_failed.append("Primary programming language not set")

    categories.append(HeuristicCategoryScore(
        category="Maintenance & Activity",
        score=round((maint_score / 25.0) * 100, 1),
        passed_checks=maint_passed,
        failed_checks=maint_failed
    ))

    # 4. Repository Structure Category (Weight: 20)
    struct_passed, struct_failed = [], []
    struct_score = 0.0

    if has_gitignore:
        struct_score += 10.0
        struct_passed.append(".gitignore file present")
    else:
        struct_failed.append("Missing .gitignore file")

    if has_env_example:
        struct_score += 10.0
        struct_passed.append(".env.example template present")
    else:
        struct_failed.append("No .env.example configuration template")

    categories.append(HeuristicCategoryScore(
        category="Repository Structure",
        score=round((struct_score / 20.0) * 100, 1),
        passed_checks=struct_passed,
        failed_checks=struct_failed
    ))

    # Calculate overall weighted score
    weights = [0.30, 0.25, 0.25, 0.20]
    total_score = sum(cat.score * w for cat, w in zip(categories, weights))
    overall_health = round(total_score, 1)

    return categories, overall_health
