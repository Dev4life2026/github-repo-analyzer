import sys
import argparse
from app.analyzer import analyze_repository
from app.formatter import format_terminal_report, format_json_report
from app.client import GitHubAPIError

def main():
    parser = argparse.ArgumentParser(
        prog="repo-analyzer",
        description="Analyze public GitHub repositories and generate transparent heuristic software structure reports."
    )
    
    parser.add_argument(
        "target",
        help="Repository target specified as 'owner/repo' or 'https://github.com/owner/repo'"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full analysis report in JSON format"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Path to save report output file (e.g., report.json or report.txt)"
    )

    parser.add_argument(
        "--token", "-t",
        help="Optional GitHub Personal Access Token to increase API rate limits"
    )

    args = parser.parse_args()

    try:
        analysis = analyze_repository(args.target, token=args.token)
        
        if args.json or (args.output and args.output.endswith(".json")):
            output_str = format_json_report(analysis)
        else:
            output_str = format_terminal_report(analysis)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_str)
            print(f"[✓] Analysis report saved to '{args.output}'.")
        else:
            print(output_str)

    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except GitHubAPIError as e:
        print(f"GitHub API Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error during analysis: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
