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

def get_query(topic, filter_condition):
    """Build search query string"""
    query = f"topic:{topic}"
    if filter_condition:
        query += f" {filter_condition}"
    return query

def fetch_repositories(github_client, query):
    """Fetch repositories and append additional information"""
    repos = github_client.search_repositories(query=query)
    results = []
    for repo in repos:
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
    """Sanitize filter condition for filename"""
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
    """Save output data to JSON file"""
    # Create topic-specific directory inside outputs
    topic_dir = os.path.join(OUTPUT_DIR, topic)
    os.makedirs(topic_dir, exist_ok=True)
    
    # Change filename format to remove 'github_repos_' prefix
    filename = f"{topic}_{safe_filter}.json"
    filepath = os.path.join(topic_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {filepath}")

def get_repos_by_topic(topic, filter_condition="", github_client=None):
    """Main function to get repositories by topic and append additional information"""
    if github_client is None:
        github_client = create_github_client()

    query = get_query(topic, filter_condition)
    print(f"Fetching repositories with topic '{topic}' and query: {query}")

    total_count, results = fetch_repositories(github_client, query)
    fetched_count = len(results)
    print(f"Total repositories found: {total_count}")
    print(f"Repositories fetched: {fetched_count}")

    data = create_output_data(
        topic, filter_condition, total_count, fetched_count, results
    )
    safe_filter = sanitize_filename(filter_condition)
    save_output(data, topic, safe_filter)

    return data

def analyze_repos(topic="image-generation", filter_condition="stars:>200"):
    """Function to analyze repositories with given parameters"""
    return get_repos_by_topic(topic, filter_condition)

if __name__ == "__main__":
    # Example usage
    analyze_repos("image-generation", "stars:>2000")
