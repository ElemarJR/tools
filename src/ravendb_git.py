from localgit import LocalGit
import os
import pandas as pd
import numpy as np


class Commits:
    def __init__(self, commits):
        self.commits = commits

    def get_summary_by_file(self):
        return self.get_summary_by('file')

    def get_summary_by_author(self):
        return self.get_summary_by('author')

    def get_summary_by_root(self):
        return self.get_summary_by('root')

    def get_summary_by_code_project(self):
        return self.get_summary_by('code_project')

    def get_summary_by(self, by):
        result = self.commits.groupby(by)['changes'].sum().reset_index()
        total_changes = result['changes'].sum()
        result['perc'] = result['changes'] / total_changes * 100
        return result.sort_values(by='changes', ascending=False)

    def get_histogram_by(self, by):
        data = self.get_summary_by(by)['changes']

        counts, bin_edges = np.histogram(data, bins=10)

        hist_df = pd.DataFrame(
            {'Bin Min': [bin_edges[i] for i in range(len(bin_edges) - 1)],
             'Bin Max': [bin_edges[i + 1] for i in range(len(bin_edges) - 1)],
             'Frequency': counts}
            )

        return hist_df

    def get_projects_of_author(self, author):
        commits_of_author_df = self.commits[self.commits['author'] == author]
        result = commits_of_author_df.groupby('code_project')['changes'].sum().reset_index()
        changes = result['changes'].sum()
        result['perc'] = result['changes'] / changes * 100
        return result.sort_values(by='changes', ascending=False)

    def get_authors_of_project(self, project):
        commits_of_project_df = self.commits[self.commits['code_project'] == project]
        result = commits_of_project_df.groupby('author')['changes'].sum().reset_index()
        changes = result['changes'].sum()
        result['perc'] = result['changes'] / changes * 100
        return result.sort_values(by='changes', ascending=False)

class RavenDB_git:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = LocalGit(repo_path)

    def get_commits(self, branch_name, start_date, end_date):
        result = self.repo.get_commits(branch_name, start_date, end_date)

        # Filtering without creating a new copy directly
        result = result[result['file'] != 'src/Raven.Studio/package-lock.json']

        # Extract directory names using vectorized operations
        result['root'] = result['file'].apply(lambda x: x.split(os.sep)[0] if len(x.split(os.sep)) > 1 else None)
        result['code_project'] = result['file'].apply(
            lambda x: x.split(os.sep)[1] if len(x.split(os.sep)) > 2 else None
            )

        # Consolidate author name replacements using a mapping dictionary
        author_corrections = {
            'Arkadiusz Palinski': 'Arkadiusz Paliński',
            'Pawel Pekrol': 'Paweł Pekról',
            'Mateusz': 'Mateusz Bartosik',
            'mateuszbartosik': 'Mateusz Bartosik'
        }
        result['author'] = result['author'].replace(author_corrections)

        return Commits(result)
