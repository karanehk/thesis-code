from repository import Repository

# repo_url = 'https://github.com/zohreab/Software_eng_lab1'  # Replace with the actual repository URL
repo_url = input("Enter the URL of the GitHub repository to analyze: ")
min_standard_time_between = 15  # 15 mins
max_standard_time_between = 120  # 2 hours in minuets
unattended_standard_time_between = 300  # 5 hours in minuets
standard_mass = 80          # 100 lines added or removed
standard_density = 5.5        # example density standard
commits_range = (int(input("Enter the start of the commits: "))-1, int(input("Enter the end of the commits: ")))

repository = Repository(repo_url, min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_mass, standard_density, commits_range)
repository.analyze_commits()
'''try:
    repository.analyze_commits()
except:
    repository.delete_repo()
'''