import subprocess
import re

class CommitAnalyzer:
    def __init__(self, repo):
        self.repo = repo

    def calculate_time_between_commits(self, commits, index_range):
        time_diffs = []
        for i in range(index_range[0]-1, index_range[1]):
            if i == 0:
                time_diffs.append(0)
            else:
                current_commit_time = commits[i].committed_datetime
                previous_commit_time = commits[i-1].committed_datetime
                time_diff = (current_commit_time - previous_commit_time).total_seconds()
                time_diffs.append(time_diff)
        return time_diffs
    
    def calculate_diff_stats(self, commits, index_range):
        diff_stats = []
        for i in range(index_range[0]-1, index_range[1]):
            if i == 0:
                diff_stats.append('first')
            else:
                current_commit = commits[i]
                previous_commit = commits[i-1]
                diff = self.repo.git.diff(previous_commit, current_commit)
                diff_stat = self._get_diffstat(diff)
                diff_stats.append(diff_stat)
            '''
            diff_data = []
            for parent in commits[i].parents:
                diff_index = parent.diff(commits[i], create_patch=True)
                for diff_item in diff_index.iter_change_type('M'):
                    diff_data.append({
                        'file_name': diff_item.b_path,
                        'diff_text': diff_item.diff.decode('utf-8', 'replace'),
                    })
            print(diff_data)
            '''
        return diff_stats

    def process_diff(self, diff):
        cleaned_diff = []
        for change in diff:
            if change.new_file:
                change_type = 'new_file'
            elif change.deleted_file:
                change_type = 'deleted_file'
            elif change.renamed_file:
                change_type = 'renamed_file'
            else:
                change_type = 'modified_file'
            
            # Process the diff text to label each line
            diff_text = change.diff.decode('utf-8', errors='ignore') if change.diff else ''
            processed_lines = []
        
            for line in diff_text.splitlines():
                if line.startswith('+++') or line.startswith('---'):
                    continue  # Ignore file path lines
                elif line.startswith('+'):
                    #TODO
                    processed_lines.append(f'Removed: {line[1:]}')
                elif line.startswith('-'):
                    processed_lines.append(f'Added: {line[1:]}')
                '''else:
                    processed_lines.append(f'Unchanged: {line}')'''
        
            processed_diff_text = '\n'.join(processed_lines)
        
            cleaned_diff.append({
                'file_path': change.b_path,
                'change_type': change_type,
                'diff': processed_diff_text
            })

        return cleaned_diff


    def _get_diffstat(self, diff):
        process = subprocess.Popen(['diffstat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=diff)
        if process.returncode != 0:
            raise RuntimeError(f"diffstat error: {stderr}")
        return stdout
