import json
from app.models import RepositoryAnalysis

def format_terminal_report(analysis: RepositoryAnalysis) -> str:
    lines = []
    lines.append("=" * 68)
    lines.append(f"  GITHUB REPOSITORY HEALTH & STRUCTURE REPORT: {analysis.full_name}")
    lines.append("=" * 68)
    
    lines.append(f"URL:          {analysis.html_url}")
    lines.append(f"Description:  {analysis.description}")
    lines.append(f"Primary Lang: {analysis.primary_language}  | Stars: {analysis.stars} | Forks: {analysis.forks} | Issues: {analysis.open_issues}")
    lines.append(f"License:      {analysis.license}  | Default Branch: {analysis.default_branch}")
    lines.append(f"Pushed At:    {analysis.pushed_at}  | Created: {analysis.created_at}")
    lines.append("-" * 68)

    lines.append(f"OVERALL HEURISTIC HEALTH SCORE: [{analysis.overall_health_score} / 100]")
    lines.append("-" * 68)
    lines.append("CATEGORY BREAKDOWN:")

    for cat in analysis.category_scores:
        score_bar = "█" * int(cat.score // 10) + "░" * (10 - int(cat.score // 10))
        lines.append(f"\n  • {cat.category:<30} [{score_bar}] {cat.score}%")
        
        if cat.passed_checks:
            lines.append("    Passed Checks:")
            for p in cat.passed_checks:
                lines.append(f"      [✓] {p}")
        if cat.failed_checks:
            lines.append("    Failed / Warning Checks:")
            for f in cat.failed_checks:
                lines.append(f"      [!] {f}")

    lines.append("\n" + "-" * 68)
    lines.append(f"DISCLAIMER: {analysis.disclaimer}")
    lines.append("=" * 68)

    return "\n".join(lines)

def format_json_report(analysis: RepositoryAnalysis) -> str:
    return json.dumps(analysis.model_dump(), indent=2)
