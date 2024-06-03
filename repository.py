import shutil
from git import Repo
import os
from commit_analyzer import CommitAnalyzer
from message_analyzer import MessageAnalyzer
from density_analyzer import DensityAnalyzer

class Repository:
    def __init__(self, repo_url, standard_time_between, standard_weight, standard_density):
        self.repo_url = repo_url
        self.repo_path = '/tmp/cloned_repo'  # Temporary path for the cloned repository
        self.clone_repo()
        
        self.commit_analyzer = CommitAnalyzer(self.repo)
        self.message_analyzer = MessageAnalyzer()
        self.density_analyzer = DensityAnalyzer(standard_time_between, standard_weight, standard_density)

    def clone_repo(self):
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path)
        self.repo = Repo.clone_from(self.repo_url, self.repo_path)
        if self.repo.bare:
            raise ValueError(f"Repository at {self.repo_url} is bare. Please clone it properly.")

    def delete_repo(self):
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path)

    def analyze_commits(self):
        commits = list(self.repo.iter_commits())
        if len(commits) < 2:
            self.delete_repo()
            raise ValueError("Not enough commits in the repository to analyze.")
        
        time_diffs = self.commit_analyzer.calculate_time_between_commits(commits)
        diff_stats = self.commit_analyzer.calculate_diff_stats(commits)
        density_warnings = self.density_analyzer.analyze_density(time_diffs, diff_stats)

        for i in range(len(time_diffs)):
            commit = commits[i+1]
            diff_stat = diff_stats[i]
            commit_message_score = self.message_analyzer.analyze_commit_message(commit.message.strip(), diff_stat)
            density_warning = density_warnings[i]
            
            print(f"Commit {i+1} -> {i+2}:")
            print(f"Time Diff = {density_warning['time_diff']} seconds")
            print(f"Diff Weight = {density_warning['weight']} lines")
            print(f"Density = {density_warning['density']:.2f}")
            print(f"Commit Message Analysis Score = {commit_message_score:.2f}")
            print(diff_stat)
            if density_warning['time_diff_warning']:
                print(f"Warning: Time difference {density_warning['time_diff']} exceeds standard {self.density_analyzer.standard_time_between}")
            if density_warning['weight_warning']:
                print(f"Warning: Diff weight {density_warning['weight']} exceeds standard {self.density_analyzer.standard_weight}")
            if density_warning['density_warning']:
                print(f"Warning: Density {density_warning['density']:.2f} exceeds standard {self.density_analyzer.standard_density}")
            if commit_message_score < 0.5:  # threshold for commit message relevance
                print(f"Warning: Commit message may not adequately describe the changes")
            print("-" * 80)
        
        self.delete_repo()