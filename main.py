from repository import Repository

repo_path = '/path/to/local/cloned/repo'
standard_time_between = 3600  # 1 hour in seconds
standard_weight = 50          # 50 lines added or removed
standard_density = 0.5        # example density standard

repository = Repository(repo_path, standard_time_between, standard_weight, standard_density)
repository.analyze_commits()
