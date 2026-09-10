from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class RepoTarget(BaseModel):
    owner: str
    repo: str

class HeuristicCategoryScore(BaseModel):
    category: str
    score: float = Field(..., ge=0.0, le=100.0)
    passed_checks: List[str]
    failed_checks: List[str]

class RepositoryAnalysis(BaseModel):
    full_name: str
    html_url: str
    description: Optional[str] = "No description provided."
    is_private: bool = False
    is_archived: bool = False
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    created_at: str = ""
    updated_at: str = ""
    pushed_at: str = ""
    default_branch: str = "main"
    license: Optional[str] = "None"
    primary_language: str = "Unknown"
    languages: Dict[str, int] = Field(default_factory=dict)
    
    # Structure & file indicators
    has_readme: bool = False
    readme_size_bytes: int = 0
    has_license: bool = False
    has_ci_config: bool = False  # .github/workflows, .travis.yml, etc.
    has_tests: bool = False      # tests/, test/, spec/
    has_contributing: bool = False
    has_env_example: bool = False
    
    # Heuristic report
    category_scores: List[HeuristicCategoryScore] = Field(default_factory=list)
    overall_health_score: float = 0.0
    disclaimer: str = (
        "Note: Health scores are heuristic indicators based on repository metadata and structure. "
        "They do not objectively evaluate code functionality or architecture."
    )
