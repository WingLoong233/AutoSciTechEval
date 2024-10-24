from github import Github
from pathlib import Path


def read_github_token(token_file="~/.ssh/github_token"):
    """Read GitHub token from file"""
    try:
        return Path(token_file).expanduser().read_text().strip()
    except FileNotFoundError:
        print(f"Error: GitHub token file not found: {token_file}")
        print("Please save your GitHub token in the ~/.ssh/github_token file.")
        exit(1)


class ForkAnalyzer:
    """Class for analyzing repository forks"""
    
    @staticmethod
    def print_fork_info(forks, show_repos=True):
        """Print basic fork information"""
        print(f"\nSelected forks: {len(forks) if forks else 0}")
        if forks and show_repos:
            for fork in forks:
                print(f"- {fork['full_name']} (Stars: {fork['stars']})")


def get_fork_info(fork):
    """Extract relevant information from a fork"""
    return {
        "full_name": fork.full_name,
        "name": fork.name,
        "url": fork.html_url,
        "stars": fork.stargazers_count,
        "created_at": fork.created_at.isoformat(),
        "description": fork.description,
        "updated_at": fork.updated_at.isoformat(),
        "language": fork.language,
    }


def get_forks(owner, repo, include_same_name=False, min_stars=0):
    """
    Get repository forks with basic filtering
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        include_same_name (bool): Whether to include forks with same name
        min_stars (int): Minimum number of stars required
    """
    github_client = Github(read_github_token())
    
    try:
        repository = github_client.get_repo(f"{owner}/{repo}")
        total_forks = repository.forks_count
        print(f"Total forks: {total_forks}")
        forks_list = []

        for fork in repository.get_forks():
            # 先判断是否包含同名仓库
            if not include_same_name and fork.name == repo:
                continue
                
            # 再判断星标数
            if min_stars == 0 or fork.stargazers_count >= min_stars:
                forks_list.append(get_fork_info(fork))

        return forks_list
    except Exception as e:
        print(f"Error getting fork information: {str(e)}")
        return None


if __name__ == "__main__":
    # owner = "THUDM"
    # repo = "MRT"
    owner = "hcengineering"
    repo = "platform"
    
    # 简化的测试用例
    analyzer = ForkAnalyzer()
    
    # 获取所有 fork
    forks = get_forks(owner, repo, min_stars=5)
    # forks = get_forks(owner, repo, include_same_name=True, min_stars=100)
    analyzer.print_fork_info(forks)
