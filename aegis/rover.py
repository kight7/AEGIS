import numpy as np
from aegis.path_planning import AStar

class Rover:
    """Autonomous rover with exploration capabilities."""
    
    def __init__(self, environment, start_x=5, start_y=5):
        self.environment = environment
        self.x = start_x
        self.y = start_y
        self.path_planner = AStar(environment)
        self.collected_data = []
        self.visited = np.zeros((environment.height, environment.width), dtype=bool)
        self.visited[start_y, start_x] = True
        self.path = []
        self.current_target = None
    
    def move(self, dx, dy):
        """Move the rover by the specified delta if the move is valid."""
        new_x, new_y = self.x + dx, self.y + dy
        
        if self.environment.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y
            self.visited[new_y, new_x] = True
            
            if self.environment.is_science_target(self.x, self.y):
                self.collect_data()
            
            return True
        return False
    
    def collect_data(self):
        """Collect scientific data at the current position."""
        if self.environment.collect_science_data(self.x, self.y):
            data_point = {
                "position": (self.x, self.y),
                "type": self._determine_science_type(),
                "value": np.random.randint(50, 100)
            }
            self.collected_data.append(data_point)
            print(f"Collected science data: {data_point}")
            return data_point
        return None
    
    def _determine_science_type(self):
        """Determine the type of science data found."""
        science_types = ["mineral deposit", "organic material", "water ice", 
                         "unusual formation", "radiation source"]
        return np.random.choice(science_types)
    
    def find_nearest_science_target(self):
        """Find the nearest science target using the environment grid."""
        grid = self.environment.get_grid()
        science_positions = np.where(grid == 2)
        
        if len(science_positions[0]) == 0:
            return None
        
        min_dist = float('inf')
        closest_target = None
        
        for i in range(len(science_positions[0])):
            y, x = science_positions[0][i], science_positions[1][i]
            dist = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
            
            if dist < min_dist:
                min_dist = dist
                closest_target = (x, y)
        
        return closest_target
    
    def plan_path_to_target(self, target=None):
        """Plan a path to the specified target or nearest science target."""
        if target is None:
            target = self.find_nearest_science_target()
        
        if target is None:
            return None
        
        self.current_target = target
        start = (self.x, self.y)
        end = target
        
        self.path = self.path_planner.find_path(start, end)
        return self.path
    
    def follow_path_step(self):
        """Follow one step of the planned path."""
        if not self.path:
            return False
        
        next_pos = self.path.pop(0)
        dx = next_pos[0] - self.x
        dy = next_pos[1] - self.y
        
        return self.move(dx, dy)
    
    def autonomous_explore(self):
        """Perform one step of autonomous exploration."""
        if not self.path:
            new_path = self.plan_path_to_target()
            if new_path is None:
                print("No more targets to explore!")
                return False
            print(f"Planning path to target at {self.current_target}")
        
        result = self.follow_path_step()
        return result
    
    def get_collected_data_summary(self):
        """Get a summary of the collected scientific data."""
        if not self.collected_data:
            return "No scientific data collected yet."
        
        summary = f"Collected {len(self.collected_data)} data points:\n"
        
        data_by_type = {}
        for data in self.collected_data:
            if data["type"] not in data_by_type:
                data_by_type[data["type"]] = []
            data_by_type[data["type"]].append(data)
        
        for data_type, items in data_by_type.items():
            summary += f"- {data_type}: {len(items)} samples\n"
        
        return summary