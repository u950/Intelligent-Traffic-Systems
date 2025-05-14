import time
from config import (
    MIN_GREEN_TIME, MAX_GREEN_TIME, TIME_LOST_DURING_SWITCH,
    PCU_VALUES, ROAD_WIDTH, LANE_WIDTH, SATURATION_FLOW_PER_SEC,
    ALPHA, BETA, GAMMA, DELTA, STATIC_TIMER_DURATION,
    MIN_VEHICLE_THRESHOLD, STATIC_TIMER_ORDER
)

class TrafficScheduler:
    def __init__(self):
        self.current_green_lane = None
        self.current_static_index = 0
        self.lanes = None
        self.should_stop = False
    
    def set_lanes(self, lanes):
        self.lanes = lanes
    
    def get_total_vehicles(self, lane_data):
        """Get total number of vehicles in a lane"""
        return sum(lane_data["vehicle_counts"].values())
    
    def calculate_total_pcu(self, lane_data):
        """Calculate total PCU for a lane based on vehicle counts"""
        total_pcu = 0
        for vehicle_type, count in lane_data["vehicle_counts"].items():
            total_pcu += count * PCU_VALUES[vehicle_type]
        return total_pcu
    
    def calculate_green_time(self, lane_data):
        """Calculate required green time based on PCU and saturation flow"""
        # Calculate number of lanes
        num_lanes = int(ROAD_WIDTH / LANE_WIDTH)
        
        # Calculate total saturation flow
        total_saturation_flow = SATURATION_FLOW_PER_SEC * num_lanes
        
        # Calculate required green time
        if total_saturation_flow > 0:
            required_time = lane_data["total_pcu"] / total_saturation_flow
        else:
            required_time = MIN_GREEN_TIME
        
        # Ensure time is within bounds
        green_time = max(MIN_GREEN_TIME, min(required_time, MAX_GREEN_TIME))
        
        return int(green_time)
    
    def should_use_static_timer(self):
        """Check if we should switch to static timer based on vehicle counts"""
        for direction in self.lanes:
            if self.get_total_vehicles(self.lanes[direction]) >= MIN_VEHICLE_THRESHOLD:
                return False
        return True
    
    def get_next_static_direction(self):
        """Get next direction in round-robin sequence"""
        direction = STATIC_TIMER_ORDER[self.current_static_index]
        self.current_static_index = (self.current_static_index + 1) % len(STATIC_TIMER_ORDER)
        return direction
    
    def select_next_lane(self, current_time):
        """Select the next lane based on weight factor calculation"""
        lane_scores = {}
        previous_lane = self.current_green_lane
        
        for direction, data in self.lanes.items():
            # Skip the previous lane to avoid consecutive selection
            if direction == previous_lane:
                continue
            
            # Calculate waiting time factor
            wait_time = current_time - data["last_green"]
            data["waiting_time"] = wait_time
            
            # Calculate weight factor using the formula:
            # Wf = α × PCUdirection + β × Tw + γ × Ev + δ × Pv
            weight_factor = (
                ALPHA * data["total_pcu"] +
                BETA * (wait_time / 60) +  # Normalize waiting time to minutes
                GAMMA * data["emergency_vehicles"] +
                DELTA * data["priority_vehicles"]
            )
            
            # If no vehicles, set score to 0
            if data["total_pcu"] == 0:
                weight_factor = 0
                
            lane_scores[direction] = weight_factor
        
        # Select lane with highest score
        return max(lane_scores.items(), key=lambda x: x[1])[0]
    
    def schedule_traffic_lights(self):
        """Schedule traffic lights based on current conditions"""
        current_time = time.time()
        
        # Update PCU values for all lanes
        for direction in self.lanes:
            self.lanes[direction]["total_pcu"] = self.calculate_total_pcu(self.lanes[direction])
        
        # Check if we should use static timer
        if self.should_use_static_timer():
            print("Switching to static timer due to low vehicle detection")
            next_lane = self.get_next_static_direction()
            green_time = STATIC_TIMER_DURATION
        else:
            print("Using dynamic timing based on vehicle detection")
            next_lane = self.select_next_lane(current_time)
            green_time = self.calculate_green_time(self.lanes[next_lane])
        
        # Update lane data
        self.lanes[next_lane]["green_time"] = green_time
        self.lanes[next_lane]["last_green"] = current_time
        
        # Set the next lane as current green lane
        self.current_green_lane = next_lane
        
        # Print the traffic schedule with detailed information
        print("\nTraffic Schedule Update at {}:".format(time.strftime("%H:%M:%S")))
        print("Current vehicle counts and wait times:")
        for direction, data in self.lanes.items():
            wait_time = current_time - data["last_green"]
            total_vehicles = self.get_total_vehicles(data)
            print("{}: {} vehicles, waiting for {:.1f} seconds".format(
                direction, 
                total_vehicles,
                wait_time
            ))
        print("Selected lane: {} for {} seconds".format(next_lane, green_time))
        print("Mode: {}".format("Static Timer" if self.should_use_static_timer() else "Dynamic Timing"))
        
        return next_lane, green_time 