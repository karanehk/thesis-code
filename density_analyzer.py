import re

class DensityAnalyzer:
    def __init__(self, min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_weight, standard_density):
        self.min_standard_time_between = min_standard_time_between
        self.max_standard_time_between = max_standard_time_between
        self.unattended_standard_time_between = unattended_standard_time_between
        self.standard_weight = standard_weight
        self.standard_density = standard_density

    def analyze_density(self, time_diffs, diff_stats):
        density_warnings = dict()        
        for author, time_diffs_list in time_diffs.items():
            for i, (index, time_diff) in enumerate(time_diffs_list):
                weight = next(filter(lambda x: x[0] == index, diff_stats[author]), None)[2]
                density = (weight / time_diff) if time_diff != 0 else ("Author's first commit" if i == 0 else float('inf'))
                
                warnings = {
                    'time_diff': time_diff if time_diff != 0 else ("Author's first commit" if i == 0 else "No time between author's commits!"),
                    'weight': weight,
                    'density': density,
                    'time_diff_warning': False if i == 0 else (((self.min_standard_time_between > time_diff or self.max_standard_time_between < time_diff) and (time_diff < self.unattended_standard_time_between))),
                    'weight_warning': weight > self.standard_weight,
                    'density_warning': False if density == "Author's first commit" else density > self.standard_density
                }
                if author in density_warnings:
                    density_warnings[author].append((index, warnings))
                else:
                    density_warnings[author] = [(index, warnings)]

        return density_warnings
'''
    def _calculate_weight_from_diffstat(self, diff_stat):
        match = re.search(r'(\d+) insertions?\(\+\), (\d+) deletions?\(\-\)', diff_stat)
        if match:
            lines_added = int(match.group(1))
            lines_removed = int(match.group(2))
            return lines_added + lines_removed
        return 0
'''