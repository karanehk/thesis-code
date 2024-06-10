import re

class DensityAnalyzer:
    def __init__(self, min_standard_time_between, max_standard_time_between, unattended_standard_time_between, standard_weight, standard_density):
        self.min_standard_time_between = min_standard_time_between
        self.max_standard_time_between = max_standard_time_between
        self.unattended_standard_time_between = unattended_standard_time_between
        self.standard_weight = standard_weight
        self.standard_density = standard_density

    def analyze_density(self, time_diffs, diff_stats):
        density_warnings = []
        for i in range(len(time_diffs)):
            time_diff = time_diffs[i]
            weight = self._calculate_weight_from_diffstat(diff_stats[i])
            density = weight / time_diff if time_diff != 0 else float('inf')
            
            warnings = {
                'time_diff': time_diff,
                'weight': weight,
                'density': density,
                'time_diff_warning': ((self.min_standard_time_between > time_diff or self.max_standard_time_between < time_diff) and (time_diff < self.unattended_standard_time_between)),
                'weight_warning': weight > self.standard_weight,
                'density_warning': density > self.standard_density
            }
            density_warnings.append(warnings)
        return density_warnings

    def _calculate_weight_from_diffstat(self, diff_stat):
        match = re.search(r'(\d+) insertions?\(\+\), (\d+) deletions?\(\-\)', diff_stat)
        if match:
            lines_added = int(match.group(1))
            lines_removed = int(match.group(2))
            return lines_added + lines_removed
        return 0
