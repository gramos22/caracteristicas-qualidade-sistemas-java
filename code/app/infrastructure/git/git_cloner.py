import subprocess
import shutil
import os
import stat
from contextlib import contextmanager
from app.core.interfaces.repository_cloner import RepositoryCloner

def _remove_readonly(func, path, _):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

class GitCloner(RepositoryCloner):
    @contextmanager
    def clone(self, repo_url: str, local_path: str):
        if os.path.exists(local_path):
            shutil.rmtree(local_path, onerror=_remove_readonly)
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            subprocess.run(
                ["git", "clone", "--depth", "1", "--single-branch", repo_url, local_path],
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            yield local_path
        finally:
            if os.path.exists(local_path):
                shutil.rmtree(local_path, onerror=_remove_readonly)