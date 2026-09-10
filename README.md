# GitHub Repository Analyzer

Python CLI developer tool for analyzing public GitHub repositories and generating transparent heuristic software structure reports.

## Overview

GitHub Repository Analyzer inspects repository metadata, activity indicators, file structures, and documentation to produce structured software health reports. It helps developers, reviewers, and team leads quickly evaluate repository hygiene across key structural dimensions.

## Features

- **Flexible Target Specification**: Supports `owner/repository` format or direct GitHub URLs (`https://github.com/owner/repo`).
- **Comprehensive Metadata Extraction**: Retrieves stargazers, forks, open issues, language distribution, default branch, push activity, and license type.
- **Transparent Heuristic Categories**:
  - **Documentation**: Evaluates README existence/size, open-source License, and CONTRIBUTING guidelines.
  - **Testing & QA**: Scans for test directories (`tests/`, `spec/`) and CI configuration (`.github/workflows`, Travis, CircleCI).
  - **Maintenance & Activity**: Inspects archive status, recent push activity, and primary language definition.
  - **Repository Structure**: Checks for `.gitignore`, `.env.example`, and clean file organization.
- **Dual Export Modes**: Beautiful terminal output format and machine-readable `--json` export.
- **Robust Error Handling**: Gracefully handles 404 missing repositories, 403 API rate limits, malformed URLs, and unauthenticated limits.

## Tech Stack

- **Language**: Python 3.10+
- **HTTP & API**: Requests, GitHub REST API v3
- **Data Validation**: Pydantic v2
- **Testing**: Pytest & Unittest.mock

## Architecture

```
[ Target Input: owner/repo OR URL ] ──> [ URL Parser ]
                                             │
                                   [ GitHub Client (REST API) ]
                                             │
                            ┌────────────────┴────────────────┐
                            ▼                                 ▼
                 [ Metadata & Structure ]            [ Scorer Engine ]
                            │                                 │
                            └────────────────┬────────────────┘
                                             ▼
                                  [ Terminal / JSON Formatter ]
```

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Dev4life2026/github-repo-analyzer.git
cd github-repo-analyzer
```

2. Create virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Analyze a Repository via Terminal Output

```bash
PYTHONPATH=. python3 app/cli.py owner/repository
```

Or using full GitHub URL:
```bash
PYTHONPATH=. python3 app/cli.py https://github.com/fastapi/fastapi
```

### Export JSON Report

```bash
PYTHONPATH=. python3 app/cli.py Dev4life2026/knowledge-ai --json
```

### Save Output to File

```bash
PYTHONPATH=. python3 app/cli.py Dev4life2026/knowledge-ai --output report.json
```

## Sample Terminal Output

```
====================================================================
  GITHUB REPOSITORY HEALTH & STRUCTURE REPORT: owner/repository
====================================================================
URL:          https://github.com/owner/repository
Description:  Full-stack AI document intelligence system
Primary Lang: TypeScript  | Stars: 120 | Forks: 14 | Issues: 2
License:      MIT  | Default Branch: main
Pushed At:    2026-09-10  | Created: 2026-09-01
--------------------------------------------------------------------
OVERALL HEURISTIC HEALTH SCORE: [92.5 / 100]
--------------------------------------------------------------------
CATEGORY BREAKDOWN:

  • Documentation                  [██████████] 100.0%
    Passed Checks:
      [✓] README file exists
      [✓] Comprehensive README size (4851 bytes)
      [✓] Open source License defined (MIT)
      [✓] CONTRIBUTING guidelines present

  • Maintenance & Activity         [██████████] 100.0%
    Passed Checks:
      [✓] Active non-archived repository
      [✓] Recent push activity (2026-09-10)

--------------------------------------------------------------------
DISCLAIMER: Note: Health scores are heuristic indicators based on repository metadata and structure. They do not objectively evaluate code functionality or architecture.
====================================================================
```

## Testing

Run the unit test suite using `pytest`:

```bash
source .venv/bin/activate
PYTHONPATH=. pytest -v
```

Tests use fixtures and `unittest.mock` to test URL parsing, score calculations, missing values, and API error states without sending live requests to GitHub.

## Project Structure

```
github-repo-analyzer/
├── app/
│   ├── cli.py               # Command line interface & argument parsing
│   ├── client.py            # GitHub REST API client & URL parser
│   ├── analyzer.py          # Orchestration pipeline
│   ├── scorer.py            # Heuristic category scoring algorithms
│   ├── models.py            # Pydantic data models
│   └── formatter.py         # Terminal & JSON formatters
├── tests/                   # Pytest suite with mocked API
│   ├── test_cli.py
│   ├── test_client.py
│   ├── test_scorer.py
│   └── test_analyzer.py
├── .env.example
├── .gitignore
└── README.md
```

## Future Improvements

- Add asynchronous batch processing for multi-repository comparison.
- Add GitHub Actions CI matrix analyzer.
- Integrate dependency vulnerability scanners.

## License

MIT License. Free for open-source evaluation and development.
