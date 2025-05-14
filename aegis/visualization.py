import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

class Visualization:
    """Visualization tools for the AEGIS explorer simulation."""
    
    def __init__(self, environment, rover):
        self.environment = environment
        self.rover = rover
        self.fig = None
        self.ax = None
        
        colors = ['lightgray', 'black', 'red', 'blue', 'yellow']
        self.cmap = ListedColormap(colors)
    
    def plot_environment(self):
        """Plot the environment, rover, and science targets."""
        grid = self.environment.get_grid().copy()
        
        rover_grid = np.zeros_like(grid)
        rover_grid[self.rover.y, self.rover.x] = 3 
        
        visited_grid = np.zeros_like(grid)
        visited_grid[self.rover.visited] = 4
        
       
        combined_grid = np.zeros_like(grid)
        combined_grid[grid == 1] = 1 
        combined_grid[grid == 2] = 2 
        combined_grid[visited_grid == 4] = 4
        combined_grid[rover_grid == 3] = 3
        
        if self.fig is None or self.ax is None:
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
        else:
            self.ax.clear()
        
        self.ax.imshow(combined_grid, cmap=self.cmap)
        
        if self.rover.path:
            path_x = [p[0] for p in self.rover.path]
            path_y = [p[1] for p in self.rover.path]
            self.ax.plot(path_x, path_y, 'b-', linewidth=2, alpha=0.7)
        
        self.ax.text(0.01, 0.01, "Blue: Rover\nRed: Science Target\nBlack: Obstacle\nYellow: Visited\nGray: Empty", 
                transform=self.ax.transAxes, fontsize=12, verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        self.ax.set_title("AEGIS Explorer Simulation")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(False)
        
        plt.draw()
        plt.pause(0.1)
    
    def plot_data_collection_summary(self):
        """Plot a summary of the collected scientific data."""
        if not self.rover.collected_data:
            return
        
        data_types = {}
        for data in self.rover.collected_data:
            data_type = data["type"]
            if data_type not in data_types:
                data_types[data_type] = []
            data_types[data_type].append(data["value"])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        types = list(data_types.keys())
        avg_values = [np.mean(data_types[t]) for t in types]
        
        ax.bar(types, avg_values, color='skyblue')
        ax.set_title('Average Value by Science Data Type')
        ax.set_xlabel('Data Type')
        ax.set_ylabel('Average Value')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        plt.show()
    
    def save_visualization(self, filename="aegis_simulation.png"):
        """Save the current visualization to a file."""
        if self.fig is not None:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {filename}")