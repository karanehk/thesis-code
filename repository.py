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
import pydriller
import itertools


class Repository:
    def __init__(self, repo_url, min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_weight, standard_density, commits_range):
        self.repo_url = repo_url
        self.repo_path = './tmp/cloned_repo'  # Temporary path for the cloned repository        
        self.increase_git_buffer_size()
        self.repo = pydriller.Repository(self.repo_url)
        #self.repo = pydriller.Repository(self.repo_path)
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
        commits_list = list(self.repo.traverse_commits())

        if len(commits_list) < 2:
            self.delete_repo()
            raise ValueError("Not enough commits in the repository to analyze.")

        if len(commits_list) < self.commits_range[1]:
            self.delete_repo()
            raise ValueError("Less commits in the repo than the specified range.")

        desired_commits = commits_list[self.commits_range[0]:self.commits_range[1]]

        arranged_commits = self._arrange_commits(commits_list, desired_commits)

        '''if len(desired_commits) < 2:
            self.delete_repo()
            raise ValueError("Not enough desired commits in the range to analyze.")'''

        time_diffs = self.commit_analyzer.calculate_time_between_commits(arranged_commits)
        diff_stats = self.commit_analyzer.calculate_diff_stats(self.repo, self.commits_range)
        density_warnings = self.density_analyzer.analyze_density(time_diffs, diff_stats)

        for author in arranged_commits.keys():
            for i, (index, commit) in enumerate(arranged_commits[author]):
                diff_text = next(filter(lambda x: x[0] == index, diff_stats[author]), None)[1]
                density_warning = next(filter(lambda x: x[0] == index, density_warnings[author]), None)[1]
                commit_message_analysis = self.message_analyzer.analyze_commit_message(commit, diff_text, index+1)

                print(f"Commit {index+1} ({commit.msg.strip()}):")

                print(f"Time Diff = {density_warning['time_diff']} minuets")
                print(f"Diff Weight = {density_warning['weight']} lines")
                if density_warning['density'] == "Author's first commit":
                    print(f"Density = {density_warning['density']}")
                else:
                    print(f"Density = {density_warning['density']:.2f}")
                print(f"Commit Message Analysis:\n{commit_message_analysis}")
                print(diff_text)
                if density_warning['time_diff_warning']:
                    print(f"Warning: Time difference {density_warning['time_diff']} is out of bound considering our standards of commiting.")
                if density_warning['weight_warning']:
                    print(f"Warning: Diff weight {density_warning['weight']} exceeds standard {self.density_analyzer.standard_weight}")
                if density_warning['density_warning']:
                    print(f"Warning: Density {density_warning['density']:.2f} exceeds standard {self.density_analyzer.standard_density}")
                print("-" * 80)
                time.sleep(3)

        self.delete_repo()

    def _arrange_commits(self, commits, desired_commits):
        arranged_commits = dict()
        authors = []
        for commit in desired_commits:
            if commit.author.name in arranged_commits:
                arranged_commits[commit.author.name].append((commits.index(commit), commit))
            else:
                arranged_commits[commit.author.name] = [(commits.index(commit), commit)]

        return arranged_commits

'''
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
'''