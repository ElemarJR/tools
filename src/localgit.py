import git
import pandas as pd


class LocalGit:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    @staticmethod
    def safe_get(tree, path, default=None):
        try:
            return tree[path]
        except KeyError:
            return default

    def get_commits(self, branch_name, start_date, end_date, as_dataframe=True):
        # Initialize an empty list for commits
        commits = []

        # Fetch commits from the repository
        for commit in self.repo.iter_commits(branch_name, since=start_date, until=end_date):
            for file_name, stats in commit.stats.files.items():
                entry = LocalGit.safe_get(commit.tree, file_name)
                lines = entry.data_stream.read().count(b'\n') + 1 if entry else 0
                commit_info = {
                    'sha': commit.hexsha,
                    'author': commit.author.name,
                    'file': file_name,
                    'changes': stats['lines'],
                    'insertions': stats['insertions'],
                    'deletions': stats['deletions'],
                    'bytes': entry.size if entry else 0,
                    'lines': lines
                }
                commits.append(commit_info)

        # Return either a Pandas DataFrame or plain Python list based on user preference
        if as_dataframe:
            return pd.DataFrame(commits)
        else:
            return commits
