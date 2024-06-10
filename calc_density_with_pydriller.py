from pydriller import RepositoryMining
from datetime import datetime, timedelta

# Path to the repository
repo_path = "/path/to/your/repo"

# Initialize a list to store commit data
commit_data = []

# Traverse the commits using PyDriller
for commit in RepositoryMining(repo_path).traverse_commits():
    commit_hash = commit.hash
    commit_date = commit.committer_date
    lines_added = sum(mod.added for mod in commit.modifications)
    lines_deleted = sum(mod.removed for mod in commit.modifications)
    net_changes = lines_added + lines_deleted  # Total lines changed

    commit_data.append({
        'hash': commit_hash,
        'date': commit_date,
        'lines_added': lines_added,
        'lines_deleted': lines_deleted,
        'net_changes': net_changes
    })

# Calculate the density for each commit
commit_density = []

for i in range(1, len(commit_data)):
    current_commit = commit_data[i]
    previous_commit = commit_data[i-1]

    time_interval = (current_commit['date'] -
                     previous_commit['date']).total_seconds()
    mass_of_changes = current_commit['net_changes']

    # Avoid division by zero for very quick successive commits
    if time_interval == 0:
        density = float('inf')
    else:
        density = mass_of_changes / time_interval

    commit_density.append({
        'hash': current_commit['hash'],
        'date': current_commit['date'],
        'density': density,
        'time_interval': time_interval,
        'mass_of_changes': mass_of_changes
    })

# Print the results
for cd in commit_density:
    print(f"Commit: {cd['hash']}, Date: {cd['date']}, Density: {cd['density']:.4f}, Time Interval: {cd['time_interval']}s, Mass of Changes: {cd['mass_of_changes']}")
