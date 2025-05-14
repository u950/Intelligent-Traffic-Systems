#!/usr/bin/env python3

import sys
import threading
import time
from config import init_lanes
from traffic_scheduler import TrafficScheduler
from gpio_controller import GPIOController
from deepstream_pipeline import DeepStreamPipeline

def control_traffic_lights(traffic_scheduler, gpio_controller):
    """Control traffic lights based on scheduler decisions"""
    while not traffic_scheduler.should_stop:
        if traffic_scheduler.current_green_lane:
            direction = traffic_scheduler.current_green_lane
            green_time = traffic_scheduler.lanes[direction]["green_time"]
            
            # Set current direction to green, others to red
            gpio_controller.set_green(direction)
            print("\nGreen light ON for {} direction for {} seconds".format(direction, green_time))
            
            start_time = time.time()
            elapsed_time = 0
            
            # Monitor traffic while green light is on
            while elapsed_time < green_time and not traffic_scheduler.should_stop:
                time.sleep(1)
                elapsed_time = time.time() - start_time
                
                # Optionally end early if traffic is very low
                if elapsed_time > 10 and traffic_scheduler.get_total_vehicles(traffic_scheduler.lanes[direction]) < 2:
                    print("Early termination due to low traffic")
                    break
            
            # Yellow light phase
            print("Yellow light ON for {} direction".format(direction))
            gpio_controller.set_yellow(direction)
            time.sleep(3)  # Yellow light duration
            
            # Set all signals to red
            gpio_controller.set_all_red()
            print("Green light OFF for {} direction after {:.1f} seconds".format(
                direction, elapsed_time))
            
            # Sleep for transition period
            print("Transition period: {} seconds".format(5))
            time.sleep(5)
            
            traffic_scheduler.current_green_lane = None
        else:
            time.sleep(0.1)  # Small sleep to prevent CPU hogging

def main():
    # Initialize components
    traffic_scheduler = TrafficScheduler()
    gpio_controller = GPIOController()
    
    # Initialize lanes data
    lanes = init_lanes()
    traffic_scheduler.set_lanes(lanes)
    
    # Start traffic control thread
    traffic_control_thread = threading.Thread(
        target=control_traffic_lights,
        args=(traffic_scheduler, gpio_controller)
    )
    traffic_control_thread.start()
    
    try:
        # Check input arguments
        if len(sys.argv) < 2:
            sys.stderr.write("usage: %s <uri1> [uri2] ... [uriN]\n" % sys.argv[0])
            sys.exit(1)

        # Ensure we have exactly 4 sources for the 4 directions
        if len(sys.argv) != 5:  # 1 for program name + 4 for sources
            sys.stderr.write("Please provide exactly 4 video sources for traffic monitoring\n")
            sys.stderr.write("usage: %s <north_src> <east_src> <south_src> <west_src>\n" % sys.argv[0])
            sys.exit(1)
        
        # Create and run DeepStream pipeline
        pipeline = DeepStreamPipeline(traffic_scheduler)
        if pipeline.create_pipeline(sys.argv[1:]):
            pipeline.run()
        else:
            sys.stderr.write("Failed to create pipeline\n")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Cleanup
        traffic_scheduler.should_stop = True
        if traffic_control_thread:
            traffic_control_thread.join()
        
        # Cleanup GPIO
        gpio_controller.cleanup()
        
        # Cleanup pipeline
        if 'pipeline' in locals():
            pipeline.cleanup()
        
        print("Exiting application")

if __name__ == '__main__':
    main() 