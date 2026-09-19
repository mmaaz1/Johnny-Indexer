import os
import subprocess
from collections.abc import Callable
from datetime import datetime

from johnny_indexer.config import ConfigHelper
from johnny_indexer.file import File

_PUSH_TIMEOUT_SECONDS = 60


class GitCommitter:
    """
    Commits and pushes the notes directory to git before the indexer runs, so every run
    has a restore point. Failures are reported but never raised, so the indexer still
    runs.
    """

    @staticmethod
    def auto_commit(root_file: File) -> None:
        repo_path = root_file.get_abs_path()
        if GitCommitter._enabled("auto_commit"):
            GitCommitter._run_safely("Auto-commit", GitCommitter._commit, repo_path)
        if GitCommitter._enabled("auto_push"):
            GitCommitter._run_safely("Auto-push", GitCommitter._push, repo_path)

    @staticmethod
    def _enabled(key: str) -> bool:
        try:
            value = ConfigHelper.load_from_config(key)
            if not isinstance(value, bool):
                raise ValueError(f"must be true or false, got '{value}'")
            return value
        except Exception as e:
            print(f"⚠️  {key} skipped: {e}")
            return False

    @staticmethod
    def _run_safely(name: str, action: Callable[[str], None], repo_path: str) -> None:
        try:
            action(repo_path)
        except Exception as e:
            print(f"⚠️  {name} skipped: {e}")

    @staticmethod
    def _commit(repo_path: str) -> None:
        if not GitCommitter._git(repo_path, "status", "--porcelain", "."):
            return

        message = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        GitCommitter._git(repo_path, "add", "-A", ".")
        GitCommitter._git(repo_path, "commit", "-m", message)
        print(f"Committed notes before indexing: {message}")

    @staticmethod
    def _push(repo_path: str) -> None:
        # Runs even without a new commit, so commits from an earlier failed push are retried
        GitCommitter._git(repo_path, "push", "--quiet", timeout=_PUSH_TIMEOUT_SECONDS)

    @staticmethod
    def _git(repo_path: str, *args: str, timeout: float | None = None) -> str:
        """Runs a git command in repo_path and returns its output, raising on failure."""
        result = subprocess.run(
            ["git", "-C", repo_path, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            # Fail instead of waiting on a credentials prompt nobody will answer
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or f"git {args[0]} exited with {result.returncode}"
            )
        return result.stdout.strip()
