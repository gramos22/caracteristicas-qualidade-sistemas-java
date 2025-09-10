import subprocess
from app.core.interfaces.repository_cloner import RepositoryCloner

class GitCloner(RepositoryCloner):
    def clone(self, repo_url: str, local_path: str) -> bool:
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, local_path],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False