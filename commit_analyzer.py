import subprocess
import re

class CommitAnalyzer:
    def __init__(self, repo):
        self.repo = repo

    def calculate_time_between_commits(self, arranged_commits):
        time_diffs = dict()
        for author in arranged_commits.keys():
            for i, (index, commit) in enumerate(arranged_commits[author]):
                if i == 0:
                    time_diffs[author] = [(index, 0)]
                else:
                    current_commit_time = commit.committer_date
                    previous_commit_time = arranged_commits[author][i-1][1].committer_date
                    time_diff = (current_commit_time - previous_commit_time).total_seconds()/60 #in minuets
                    time_diffs[author].append((index, time_diff))
        return time_diffs
    
    def calculate_diff_stats(self, arranged_commits):
        diff_stats = dict()
        for author in arranged_commits.keys():
            for i, (index, commit) in enumerate(arranged_commits[author]):
                if index == 0:
                    diff_stats[author] = [(index, 'first')]
                else:
                    diff_stat = ""
                    for file in commit.modified_files:

                        diff_list = file.diff_parsed
                        flattened_diff = []
                        for key, value_list in diff_list.items():
                            for ln, line in value_list:
                                flattened_diff.append((ln, key, line))
                        sorted_diff = sorted(flattened_diff, key=lambda x: x[0])
                        diff_value = ""
                        for ln, key, line in sorted_diff:
                            diff_value += f"{key}: {ln}  {line}"

                        diff_stat += "File name: {}\n".format(m.filename),
                        "Change type: {}\n".format(m.change_type.name),
                        "Changes:\n{}\n".format(diff_value)

                    if author in diff_stats:
                        diff_stats[author].append((index, diff_stat))
                    else:
                        diff_stats[author] = [(index, diff_stat)]
        return diff_stats
'''
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
                else:
                    processed_lines.append(f'Unchanged: {line}')
        
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
'''