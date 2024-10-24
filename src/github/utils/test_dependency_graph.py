from github import Github
from pathlib import Path
import requests

def read_github_token(token_file="~/.ssh/github_token"):
    """Read GitHub token from file"""
    try:
        return Path(token_file).expanduser().read_text().strip()
    except FileNotFoundError:
        print(f"Error: GitHub token file not found: {token_file}")
        print("Please save your GitHub token in the ~/.ssh/github_token file.")
        exit(1)

def get_dependencies_info(owner, repo, token):
    """Get dependencies information using GitHub API"""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}/dependency-graph/sbom"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        sbom_data = response.json()
        dependencies_count = len(sbom_data.get("sbom", {}).get("packages", []))
        return dependencies_count
    else:
        print(f"Error: Unable to fetch dependencies. Status code: {response.status_code}")
        return 0

def get_dependents_info(owner, repo, token):
    """Get dependents information using GitHub API"""
    g = Github(token)
    repo_obj = g.get_repo(f"{owner}/{repo}")
    
    try:
        # Note: This is a network-dependent call and might take some time
        dependents_count = repo_obj.get_dependents().totalCount
        return dependents_count
    except Exception as e:
        print(f"Error fetching dependents info: {e}")
        return 0

if __name__ == "__main__":
    # Read GitHub token
    token = read_github_token()
    
    # Test with a sample repository
    owner = "AUTOMATIC1111"
    repo = "stable-diffusion-webui"
    
    deps_count = get_dependencies_info(owner, repo, token)
    dependents_count = get_dependents_info(owner, repo, token)
    
    print(f"Repository: {owner}/{repo}")
    print(f"Dependencies count: {deps_count}")
    print(f"Dependents count: {dependents_count}")
