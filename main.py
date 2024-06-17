from repository import Repository

repo_url = 'https://github.com/zohreab/Software_eng_lab1.git'  # Replace with the actual repository URL
min_standard_time_between = 3600  # 1 hour in seconds
max_standard_time_between = 7200  # 2 hours in seconds
unattended_standard_time_between = 18000  # 5 hours in seconds
standard_weight = 50          # 50 lines added or removed
standard_density = 0.5        # example density standard
commits_range = (5, 5)

repository = Repository(repo_url, min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_weight, standard_density, commits_range)
repository.analyze_commits()
