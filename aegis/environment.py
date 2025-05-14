import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

class Environment:
    """Simulated planetary environment with obstacles and points of scientific interest."""
    def __init__(self, width=100, height=100, obstacle_density=0.2, science_target_count=5):
        self.width = width
        self.height = height
        self.obstacle_density = obstacle_density
        self.science_target_count = science_target_count
        
        self.grid = np.zeros((height, width))
        
        self._generate_obstacles()
        
        self._generate_science_targets()
        
    def _generate_obstacles(self):
        """Generate random obstacles in the environment."""
        obstacle_mask = np.random.random((self.height, self.width)) < self.obstacle_density
        self.grid[obstacle_mask] = 1
        for _ in range(int(self.width * self.height * 0.01)):
            x, y = np.random.randint(0, self.width-3), np.random.randint(0, self.height-3)
            size = np.random.randint(2, 6)
            if x + size >= self.width:
                size = self.width - x - 1
            if y + size >= self.height:
                size = self.height - y - 1
            self.grid[y:y+size, x:x+size] = 1
    
    def _generate_science_targets(self):
        """Generate random science targets in the environment."""
        targets_placed = 0
        attempts = 0
        
        while targets_placed < self.science_target_count and attempts < 1000:
            x, y = np.random.randint(0, self.width), np.random.randint(0, self.height)
            if self.grid[y, x] == 0:
                self.grid[y, x] = 2
                targets_placed += 1
            attempts += 1
    
    def is_valid_position(self, x, y):
        """Check if the position is valid (within bounds and not an obstacle)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x] != 1
        return False
    
    def is_science_target(self, x, y):
        """Check if the position contains a science target."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x] == 2
        return False
    
    def collect_science_data(self, x, y):
        """Collect science data from a target."""
        if self.is_science_target(x, y):
            self.grid[y, x] = 0
            return True
        return False
    
    def get_grid(self):
        """Return a copy of the grid."""
        return self.grid.copy()