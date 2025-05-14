import numpy as np

class ScienceAnalyzer:
    """Analyzes environment data to identify areas of scientific interest."""
    
    def __init__(self, environment):
        self.environment = environment
        
    def analyze_data(self, data_points):
        """Analyze collected scientific data to identify patterns."""
        if not data_points:
            return "No data to analyze"
        
        type_counts = {}
        for data in data_points:
            data_type = data["type"]
            if data_type not in type_counts:
                type_counts[data_type] = 0
            type_counts[data_type] += 1
        
        type_values = {}
        for data in data_points:
            data_type = data["type"]
            if data_type not in type_values:
                type_values[data_type] = []
            type_values[data_type].append(data["value"])
        
        for data_type in type_values:
            type_values[data_type] = np.mean(type_values[data_type])
        
        report = "Scientific Data Analysis:\n"
        report += "========================\n"
        report += f"Total data points: {len(data_points)}\n\n"
        
        report += "Distribution by type:\n"
        for data_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"- {data_type}: {count} samples ({count/len(data_points)*100:.1f}%)\n"
        
        report += "\nAverage value by type:\n"
        for data_type, avg_value in sorted(type_values.items(), key=lambda x: x[1], reverse=True):
            report += f"- {data_type}: {avg_value:.2f}\n"
        
        report += "\nRecommendations:\n"
        highest_value_type = max(type_values.items(), key=lambda x: x[1])[0]
        report += f"- Focus additional exploration on {highest_value_type} deposits\n"
        
        if len(data_points) < 3:
            report += "- Collect more samples for statistically significant analysis\n"
        
        return report
    
    def predict_science_target_locations(self, rover_visited):
        """Predict locations that might contain science targets based on visited areas."""
        
        grid = self.environment.get_grid()
        height, width = grid.shape
        
        potential_targets = []
        
        for y in range(height):
            for x in range(width):
                if rover_visited[y, x] or grid[y, x] == 1:
                    continue
                
                adjacent_to_obstacle = False
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 1:
                        adjacent_to_obstacle = True
                        break
                
                if adjacent_to_obstacle:
                    min_dist_to_visited = float('inf')
                    for y2 in range(height):
                        for x2 in range(width):
                            if rover_visited[y2, x2]:
                                dist = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                                min_dist_to_visited = min(min_dist_to_visited, dist)
                    
                    interest_score = min_dist_to_visited * np.random.uniform(0.8, 1.2)
                    potential_targets.append((x, y, interest_score))
        
        potential_targets.sort(key=lambda x: x[2], reverse=True)
        
        return potential_targets[:10]