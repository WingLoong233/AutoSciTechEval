from github import Github
from pathlib import Path
import argparse
import json
import os

# Get the current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Set output directory to 'outputs' folder in the project root
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "outputs")


def read_github_token(token_file="~/.ssh/github_token"):
    """Read GitHub token from file"""
    try:
        return Path(token_file).expanduser().read_text().strip()
    except FileNotFoundError:
        print(f"Error: GitHub token file not found: {token_file}")
        print("Please save your GitHub token in the ~/.ssh/github_token file.")
        exit(1)


def create_github_client():
    """Create and return a GitHub client"""
    token = read_github_token()
    return Github(token)


def build_query(topic, filter_condition):
    """Build the search query string"""
    query = f"topic:{topic}"
    if filter_condition:
        query += f" {filter_condition}"
    return query


def fetch_repositories(g, query, limit):
    """Fetch repositories based on the query"""
    repos = g.search_repositories(query=query)
    results = []
    for i, repo in enumerate(repos if limit is None else repos[:limit], 1):
        repo_info = {
            "name": repo.full_name,
            "stars": repo.stargazers_count,
            "description": repo.description,
            "url": repo.html_url,
        }
        results.append(repo_info)
    return repos.totalCount, results


def create_output_data(topic, filter_condition, total_count, fetched_count, results):
    """Create a dictionary with output data"""
    return {
        "topic": topic,
        "filter_condition": filter_condition,
        "total_count": total_count,
        "fetched_count": fetched_count,
        "repositories": results,
    }


def sanitize_filename(filter_condition):
    """Sanitize filter condition for use in filename"""
    return (
        filter_condition.replace(" ", "_")
        .replace(":", "")
        .replace(">", "_gt_")
        .replace("<", "_lt_")
        .replace("/", "_slash_")
        .replace("\\", "_backslash_")
        .replace("?", "_question_")
        .replace("*", "_asterisk_")
        .replace("|", "_pipe_")
        .replace('"', "_quote_")
        .replace("'", "_apostrophe_")
    )


def save_output(data, topic, safe_filter):
    """Save output data to a JSON file"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"github_repos_{topic}_{safe_filter}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {filepath}")


def get_repos_by_topic(
    topic="text-generation", filter_condition="stars:>100", limit=100
):
    """Main function to get repositories by topic"""
    g = create_github_client()
    query = build_query(topic, filter_condition)
    print(f"Repositories with topic '{topic}' and query: {query}")

    total_count, results = fetch_repositories(g, query, limit)
    fetched_count = len(results)
    print(f"Total repositories found: {total_count}")
    print(f"Repositories fetched: {fetched_count}")

    data = create_output_data(
        topic, filter_condition, total_count, fetched_count, results
    )
    safe_filter = sanitize_filename(filter_condition)
    save_output(data, topic, safe_filter)

    return data


def main():
    """Parse command line arguments and call the main function"""
    parser = argparse.ArgumentParser(description="Analyze GitHub repository")
    parser.add_argument(
        "--topic", default="text-generation", help="Topic to search for"
    )
    parser.add_argument(
        "--filter",
        default="stars:>100",
        help="Additional filter condition. Examples: 'stars:>100', 'language:python', 'stars:>50 language:javascript', 'created:>2022-01-01'",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Limit the number of repositories to fetch",
    )

    args = parser.parse_args()
    get_repos_by_topic(args.topic, filter_condition=args.filter, limit=args.limit)


if __name__ == "__main__":
    main()
