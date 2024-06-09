import subprocess
import re

class CommitAnalyzer:
    def __init__(self, repo):
        self.repo = repo

    def calculate_time_between_commits(self, commits):
        time_diffs = []
        for i in range(1, len(commits)):
            current_commit_time = commits[i].committed_datetime
            previous_commit_time = commits[i-1].committed_datetime
            time_diff = (current_commit_time - previous_commit_time).total_seconds()
            time_diffs.append(time_diff)
        return time_diffs
    
    def calculate_diff_stats(self, commits):
        diff_stats = []
        for i in range(1, len(commits)):
            current_commit = commits[i]
            previous_commit = commits[i-1]
            diff = self.repo.git.diff(previous_commit, current_commit)
            diff_stat = self._get_diffstat(diff)
            diff_data = []
            for parent in commits[i].parents:
                diff_index = parent.diff(commits[i], create_patch=True)
                for diff_item in diff_index.iter_change_type('M'):
                    diff_data.append({
                        'file_name': diff_item.b_path,
                        'diff_text': diff_item.diff.decode('utf-8', 'replace'),
                    })
            print(diff_data)
        return diff_stats

    def _get_diffstat(self, diff):
        process = subprocess.Popen(['diffstat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=diff)
        if process.returncode != 0:
            raise RuntimeError(f"diffstat error: {stderr}")
        return stdout
