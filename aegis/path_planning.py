import numpy as np
import heapq

class AStar:
    """A* pathfinding algorithm implementation."""
    
    def __init__(self, environment):
        self.environment = environment
    
    def find_path(self, start, end):
        """Find a path from start to end using A* algorithm."""
        open_set = []
        closed_set = set()
        
        heapq.heappush(open_set, (0, start, []))
        
        while open_set:
            f, current, path = heapq.heappop(open_set)
            
            if current == end:
                return path + [current]
            
            if current in closed_set:
                continue
            
            closed_set.add(current)
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                x, y = current[0] + dx, current[1] + dy
                
                if not self.environment.is_valid_position(x, y):
                    continue
                
                neighbor = (x, y)
                
                if neighbor in closed_set:
                    continue
                
                g = len(path) + 1
                
                h = abs(x - end[0]) + abs(y - end[1])
                f = g + h
                
                heapq.heappush(open_set, (f, neighbor, path + [current]))
        
        return None


class RandomWalk:
    """Random walk exploration strategy."""
    
    def __init__(self, environment):
        self.environment = environment
    
    def get_next_move(self, current_pos):
        """Get the next random valid move from the current position."""
        x, y = current_pos
        possible_moves = []
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.environment.is_valid_position(new_x, new_y):
                possible_moves.append((dx, dy))
        
        if possible_moves:
            return possible_moves[np.random.randint(0, len(possible_moves))]
        return None