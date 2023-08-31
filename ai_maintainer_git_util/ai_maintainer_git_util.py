"""Main module."""

import subprocess
import base64
import os
import tempfile


class GitRepo:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self._credentials = f"{self.username}:{self.password}"
        self._encoded_credentials = base64.b64encode(
            self._credentials.encode("utf-8")
        ).decode()
        self.auth_header = (
            f"http.extraHeader=Authorization: Basic {self._encoded_credentials}"
        )

    def _print_std_streams(self, result):
        if result:
            if result.stderr:
                print(result.stderr.decode())
            if result.stdout:
                print(result.stdout.decode())

    def clone(self, directory):
        command = ["git", "-c", self.auth_header, "clone", self.url, directory]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def fetch(self, directory):
        command = ["git", "-C", directory, "-c", self.auth_header, "fetch"]
        print(" ".join(command))
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def pull(self, directory, branch=None):
        command = ["git", "-C", directory, "-c", self.auth_header, "pull", "origin"]
        if branch:
            command.append(branch)
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def push(self, directory, branch=None, force=False):
        command = ["git", "-C", directory, "-c", self.auth_header, "push", "origin"]
        if branch:
            command.append(branch)
        if force:
            command.append("--force")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def checkout(self, directory, branch=None):
        if not branch:
            raise ValueError("Branch name must be provided for checkout.")
        command = ["git", "-C", directory, "checkout", branch]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def create_branch(self, directory, branch=None):
        if not branch:
            raise ValueError("Branch name must be provided for creating a branch.")
        command = ["git", "-C", directory, "checkout", "-b", branch]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def merge(self, directory, branch=None):
        if not branch:
            raise ValueError("Branch name must be provided for merge.")
        command = ["git", "-C", directory, "merge", branch]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def add(self, directory, files=".", all=False):
        command = ["git", "-C", directory, "add"]
        if all:
            command.append("--all")
        else:
            command.append(files)
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def commit(self, directory, message):
        if not message:
            raise ValueError("Commit message must be provided.")

        command = ["git", "-C", directory, "commit", "-m", message]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self._print_std_streams(result)

    def has_changes(self, directory):
        command = ["git", "-C", directory, "status", "--porcelain"]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        output = result.stdout.decode().strip()

        # If the output is empty, there are no changes to commit
        if output:
            print("There are changes to commit.")
            return True
        else:
            print("There are no changes to commit.")
            return False

    def fork(self, fork_url, force=False):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the original repository into the temporary directory
            self.clone(temp_dir)

            # Change to the temporary directory
            command = ["git", "-C", temp_dir, "remote", "add", "fork", fork_url]
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            # Push the contents to the fork URL, with force if specified
            push_command = [
                "git",
                "-C",
                temp_dir,
                "-c",
                self.auth_header,
                "push",
                "fork",
                "--all",
            ]
            if force:
                push_command.append("--force")

            result = subprocess.run(
                push_command,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                check=True,
            )
            self._print_std_streams(result)

        # The temporary directory and its contents will be deleted when the context is exited


def create_url(host: str, owner: str, repo: str) -> str:
    return f"{host}/{owner}/{repo}"


if __name__ == "__main__":
    GIT_HOST = "http://git-server:8080"
    CLIENT_USERNAME = "test_user1"
    CLIENT_PASSWORD = "F@k3awefawefawef"
    CLIENT_CODE_OWNER = CLIENT_USERNAME
    CLIENT_CODE_REPO = "repo1"
    OPERATOR_USERNAME = "test_user2"
    OPERATOR_PASSWORD = "F@k3awefawefawef"
    OPERATOR_CODE_OWNER = OPERATOR_USERNAME
    OPERATOR_CODE_REPO = "repo2"
    TEMP_DIR = "./deleteme"

    url = create_url(GIT_HOST, OPERATOR_CODE_OWNER, OPERATOR_CODE_REPO)
    gitrepo = GitRepo(
        url,
        OPERATOR_USERNAME,
        OPERATOR_PASSWORD,
    )
    path = os.path.join(TEMP_DIR, CLIENT_CODE_REPO)
    gitrepo.clone(path)
