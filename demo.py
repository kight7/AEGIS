"""
AEGIS Explorer Demo
Autonomous Exploration for Gathering Increased Science

This script demonstrates a simulated autonomous rover exploring an environment,
identifying science targets, planning paths, and collecting data.
"""
import time
import argparse
import matplotlib.pyplot as plt

from aegis.environment import Environment
from aegis.rover import Rover
from aegis.visualization import Visualization
from aegis.science_analyzer import ScienceAnalyzer

def parse_args():
    parser = argparse.ArgumentParser(description='AEGIS Explorer Demo')
    parser.add_argument('--width', type=int, default=50, help='Width of the environment')
    parser.add_argument('--height', type=int, default=50, help='Height of the environment')
    parser.add_argument('--obstacles', type=float, default=0.2, help='Obstacle density (0-1)')
    parser.add_argument('--targets', type=int, default=10, help='Number of science targets')
    parser.add_argument('--steps', type=int, default=100, help='Number of simulation steps')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between steps (seconds)')
    parser.add_argument('--save', action='store_true', help='Save final visualization')
    return parser.parse_args()

def main():
    args = parse_args()
    
    print("Initializing AEGIS Explorer Demo...")
    
    print(f"Creating environment ({args.width}x{args.height}) with {args.targets} science targets...")
    env = Environment(width=args.width, height=args.height, 
                     obstacle_density=args.obstacles,
                     science_target_count=args.targets)
    
    print("Deploying rover...")
    rover = Rover(env, start_x=args.width // 10, start_y=args.height // 10)
    
    vis = Visualization(env, rover)
    
    analyzer = ScienceAnalyzer(env)
    
    print(f"Beginning autonomous exploration ({args.steps} steps)...")
    plt.ion()
    
    for step in range(args.steps):
        print(f"\nStep {step+1}/{args.steps}")
        
        result = rover.autonomous_explore()
        
        if not result:
            print("Exploration complete or no valid moves.")
            if not rover.path:
                predictions = analyzer.predict_science_target_locations(rover.visited)
                if predictions:
                    print(f"Using science analyzer to predict interesting locations...")
                    next_target = predictions[0][:2]
                    print(f"Moving to predicted interesting location at {next_target}")
                    rover.plan_path_to_target(next_target)
        
        vis.plot_environment()
        
        if rover.collected_data:
            print(f"Collected data: {len(rover.collected_data)} samples")
        
        time.sleep(args.delay)
    print("\n" + "="*50)
    print("AEGIS Explorer Mission Complete")
    print("="*50)
    print(f"Steps taken: {args.steps}")
    print(f"Area explored: {rover.visited.sum()} grid cells ({rover.visited.sum() / (args.width * args.height) * 100:.1f}% of environment)")
    print(f"Science data collected: {len(rover.collected_data)} samples")
    
    # Print scientific analysis
    if rover.collected_data:
        print("\n" + analyzer.analyze_data(rover.collected_data))
        
        vis.plot_data_collection_summary()
    
    if args.save:
        vis.save_visualization()
    
    print("\nPress Enter to exit...")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()