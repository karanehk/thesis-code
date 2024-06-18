import shutil
from git import Repo
import git
import os
from commit_analyzer import CommitAnalyzer
from message_analyzer import MessageAnalyzer
from density_analyzer import DensityAnalyzer
import pandas as pd
import subprocess
import time

class Repository:
    def __init__(self, repo_url, min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_weight, standard_density, commits_range):
        self.repo_url = repo_url
        self.repo_path = './tmp/cloned_repo'  # Temporary path for the cloned repository
        self.increase_git_buffer_size()
        self.clone_repo()
        #self.fetch_full_history()

        self.commits_range = commits_range
        
        self.commit_analyzer = CommitAnalyzer(self.repo)
        self.message_analyzer = MessageAnalyzer()
        self.density_analyzer = DensityAnalyzer(min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_weight, standard_density)

    def increase_git_buffer_size(self):
        try:
            subprocess.run(['git', 'config', '--global', 'http.postBuffer', '524288000'], check=True)
            print("Increased git buffer size to 500MB")
        except subprocess.CalledProcessError as e:
            print(f"Failed to increase buffer size: {e}")

    def clone_repository(self, repo_url, clone_dir, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                repo = git.Repo.clone_from(repo_url, clone_dir)
                print(f"Successfully cloned repository to {clone_dir}")
                return repo
            except git.exc.GitCommandError as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                attempt += 1
                time.sleep(5)  # Wait before retrying
        raise Exception("Failed to clone repository after multiple attempts")
    
    def fetch_full_history(self, step=30, max_retries=3):
        attempt = 0
        while True:
            try:
                self.repo.git.fetch(f"--depth={step}")
                print(f"Successfully deepened clone by {step} commits")
                time.sleep(5)
                step += step  # Increase the depth for the next fetch
                self.repo.git.fetch('--unshallow')  # Try to unshallow if possible
                time.sleep(5)
                print("Successfully fetched full history")
                break
            except git.exc.GitCommandError as e:
                print(f"Deepen attempt {attempt + 1}/{max_retries} failed: {e}")
                attempt += 1
                if attempt >= max_retries:
                    raise Exception("Failed to deepen clone after multiple attempts")
                time.sleep(5)  # Wait before retrying

    def clone_repository_with_depth(self, repo_url, clone_dir, depth=1, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                repo = git.Repo.clone_from(repo_url, clone_dir, depth=depth)
                print(f"Successfully cloned repository to {clone_dir} with depth {depth}")
                return repo
            except git.exc.GitCommandError as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                attempt += 1
                time.sleep(5)  # Wait before retrying
        raise Exception("Failed to clone repository after multiple attempts")

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

        if len(commits) < self.commits_range[1]:
            self.delete_repo()
            raise ValueError("Less commits in the repo than the specified range.")

        commits.reverse()
        desired_commits = commits[self.commits_range[0]-1:self.commits_range[1]]

        '''if len(desired_commits) < 2:
            self.delete_repo()
            raise ValueError("Not enough desired commits in the range to analyze.")'''

        time_diffs = self.commit_analyzer.calculate_time_between_commits(commits, self.commits_range)
        diff_stats = self.commit_analyzer.calculate_diff_stats(commits, self.commits_range)
        density_warnings = self.density_analyzer.analyze_density(time_diffs, diff_stats)

        for i in range(len(desired_commits)):
            commit = desired_commits[i]
            diff_stat = diff_stats[i]
            density_warning = density_warnings[i]

            parents = commit.parents
            if len(parents) == 1:
                diffs = commit.diff(parents[0], create_patch=True)
            else:
                # Handle the initial commit or merge commits with multiple parents
                diffs = commit.diff(None, create_patch=True)
        
            
            cleaned_diffs = self.commit_analyzer.process_diff(diffs)
            df = pd.DataFrame(cleaned_diffs)

            diff_text = ""
            for index, row in df.iterrows():
                diff_text += f"File Path: {row['file_path']}\n"\
                f"Change Type: {row['change_type']}\n"\
                f"Diff:\n{row['diff']}"\
                "\n" + "*"*50 + "\n"

            print(f"Commit {self.commits_range[0]+i} ({commit.message.strip()}):")

            commit_message_analysis = self.message_analyzer.analyze_commit_message(commit, diff_text)

            print(f"Time Diff = {density_warning['time_diff']} seconds")
            print(f"Diff Weight = {density_warning['weight']} lines")
            print(f"Density = {density_warning['density']:.2f}")
            print(f"Commit Message Analysis:\n{commit_message_analysis}")
            print(diff_stat)
            if density_warning['time_diff_warning']:
                print(f"Warning: Time difference {density_warning['time_diff']} is out of bound considering our standards of commiting.")
            if density_warning['weight_warning']:
                print(f"Warning: Diff weight {density_warning['weight']} exceeds standard {self.density_analyzer.standard_weight}")
            if density_warning['density_warning']:
                print(f"Warning: Density {density_warning['density']:.2f} exceeds standard {self.density_analyzer.standard_density}")
            print("-" * 80)
            time.sleep(3)

        self.delete_repo()
