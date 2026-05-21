from github import Github


def get_repo_info(repo_url: str):

    """
    Fetch GitHub repository information.
    """

    try:

        # Convert URL → owner/repo
        repo_name = repo_url.replace(
            "https://github.com/",
            ""
        ).strip("/")

        # Initialize GitHub client
        g = Github()

        # Fetch repository
        repo = g.get_repo(repo_name)

        # Return useful metadata
        return {

            "name": repo.name,

            "full_name": repo.full_name,

            "description": repo.description,

            "stars": repo.stargazers_count,

            "forks": repo.forks_count,

            "issues": repo.open_issues_count,

            "language": repo.language,

            "watchers": repo.watchers_count,

            "url": repo.html_url,

            "owner": repo.owner.login
        }

    except Exception as e:

        print("GitHub API Error:", e)

        return None