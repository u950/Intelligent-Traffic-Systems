from app import get_vehicle_counts
import random
import time
import threading

# Initialize traffic lanes with vehicle counts
lanes = {
    "north": {"vehicle_count": 0, "green_time": 0},
    "east": {"vehicle_count": 0, "green_time": 0},
    "south": {"vehicle_count": 0, "green_time": 0},
    "west": {"vehicle_count": 0, "green_time": 0},
}

# Parameters
minimum_green_time = 10  # Minimum time a lane gets green light
time_lost_during_switch = 5  # Seconds lost during phase switches

# Function to fetch vehicle counts from DeepStream pipeline
def fetch_vehicle_counts():
    # Get counts from app.py
    counts = get_vehicle_counts()
    return {
        "north": counts[0],
        "east": counts[1], 
        "south": counts[2],
        "west": counts[3],
    }

def calculate_probabilities(lanes):
    total_vehicles = sum(lane["vehicle_count"] for lane in lanes.values())
    if total_vehicles == 0:
        # Prevent division by zero
        return {direction: 1 / len(lanes) for direction in lanes}
    probabilities = {
        direction: lane["vehicle_count"] / total_vehicles for direction, lane in lanes.items()
    }
    return probabilities

# Function to select the next lane to turn green
def select_next_lane(probabilities):
    directions = list(probabilities.keys())
    weights = list(probabilities.values())
    return random.choices(directions, weights=weights, k=1)[0]

# Create a flag to control the traffic scheduling loop
running = True

# Add state tracking for current green light
current_green = None
last_switch_time = 0

def start_traffic_control():
    """Start the traffic control in a separate thread"""
    global running
    running = True  # Ensure running is True when starting
    thread = threading.Thread(target=dynamic_traffic_control)
    thread.daemon = True  # Thread will exit when main program exits
    thread.start()
    return thread

def stop_traffic_control():
    """Stop the traffic control loop"""
    global running, current_green
    running = False
    current_green = None  # Reset state

def dynamic_traffic_control():
    """Main traffic control loop"""
    global running, current_green, last_switch_time
    
    while running:
        try:
            # Step 1: Fetch vehicle counts from cameras
            vehicle_counts = fetch_vehicle_counts()
            if not vehicle_counts:
                print("Warning: No vehicle counts received")
                time.sleep(1)
                continue
                
            for direction, count in vehicle_counts.items():
                lanes[direction]["vehicle_count"] = count

            # Step 2: Calculate probabilities
            probabilities = calculate_probabilities(lanes)

            # Step 3: Select the next lane to turn green
            next_lane = select_next_lane(probabilities)
            
            # Avoid switching to the same lane unless it's the only option
            if current_green and next_lane == current_green and len(lanes) > 1:
                # Remove current lane from options and recalculate
                filtered_probs = {k:v for k,v in probabilities.items() if k != current_green}
                if filtered_probs:
                    next_lane = select_next_lane(filtered_probs)

            # Print counts and selected lane
            print("\nCurrent Vehicle Counts:")
            for direction, data in lanes.items():
                print(f"{direction}: {data['vehicle_count']} vehicles")
            
            # Step 4: Calculate green time based on traffic volume
            green_time = max(minimum_green_time, 
                           min(lanes[next_lane]["vehicle_count"] * 2, 30))  # Cap at 30 seconds
            
            current_time = time.time()
            time_since_last_switch = current_time - last_switch_time
            
            # Ensure minimum time between switches
            if time_since_last_switch < minimum_green_time:
                time.sleep(minimum_green_time - time_since_last_switch)
            
            print(f"\nGreen light for {next_lane} lane for {green_time} seconds")
            current_green = next_lane
            last_switch_time = time.time()

            # Step 5: Simulate green light duration
            time.sleep(green_time)

            # Step 6: Simulate phase switch delay
            print(f"Switching phase... (Time lost: {time_lost_during_switch} seconds)")
            time.sleep(time_lost_during_switch)

        except Exception as e:
            print(f"Error in traffic control loop: {e}")
            time.sleep(1)  # Prevent tight loop in case of errors

if __name__ == "__main__":
    # This allows testing the traffic scheduling algorithm independently
    print("Testing traffic scheduling algorithm...")
    control_thread = start_traffic_control()
    
    try:
        # Run for 60 seconds then exit
        time.sleep(60)
    except KeyboardInterrupt:
        print("\nStopping traffic control...")
    finally:
        stop_traffic_control()
        control_thread.join()
