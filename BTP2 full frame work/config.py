import time

# DeepStream configuration
MAX_DISPLAY_LEN = 64
PGIE_CLASS_ID_MOTORCYCLE = "motorcycle"
PGIE_CLASS_ID_TRUCK = "truck"
PGIE_CLASS_ID_CAR = "car"
PGIE_CLASS_ID_BUS = "bus"
PGIE_CLASS_ID_AUTORICKSHAW = "autorickshaw"
MUXER_OUTPUT_WIDTH = 1280
MUXER_OUTPUT_HEIGHT = 720
MUXER_BATCH_TIMEOUT_USEC = 4000000
TILED_OUTPUT_WIDTH = 640 * 2
TILED_OUTPUT_HEIGHT = 480 * 2
GST_CAPS_FEATURES_NVMM = "memory:NVMM"
OSD_PROCESS_MODE = 0
OSD_DISPLAY_TEXT = 0
PGIE_CLASSES_STR = ["motorcycle", "truck", "car", "bus", "autorickshaw"]

# GPIO configuration
GPIO_PINS = {
    "north": {"red": 11, "yellow": 13, "green": 15},
    "south": {"red": 19, "yellow": 21, "green": 23},
    "east": {"red": 29, "yellow": 31, "green": 33},
    "west": {"red": 35, "yellow": 37, "green": 38}
}

# Traffic control parameters
MIN_GREEN_TIME = 10  # Minimum time a lane gets green light
MAX_GREEN_TIME = 60  # Maximum green time for any lane
TIME_LOST_DURING_SWITCH = 5  # Seconds lost during phase switches
BASE_TIME_PER_OBJECT = 0.5  # Base seconds per detected object
CONGESTION_THRESHOLD = 20  # Number of objects that indicates congestion
STARVATION_TIME = 45  # Maximum time a lane should wait

# PCU values for different vehicle types
PCU_VALUES = {
    "motorcycle": 0.5,
    "truck": 2.2,
    "car": 1.0,
    "bus": 2.2,
    "autorickshaw": 1.2
}

# Traffic control parameters
ROAD_WIDTH = 14  # meters (assuming 4 lanes of 3.5m each)
LANE_WIDTH = 3.5  # meters
SATURATION_FLOW = 1800  # PCU/hr/lane
SATURATION_FLOW_PER_SEC = SATURATION_FLOW / 3600  # PCU/sec/lane

# Weight coefficients for lane selection
ALPHA = 0.4  # PCU weight
BETA = 0.3   # Waiting time weight
GAMMA = 0.2  # Emergency vehicle weight
DELTA = 0.1  # Priority vehicle weight

# Static timer configuration
STATIC_TIMER_DURATION = 30  # seconds for each direction in static mode
MIN_VEHICLE_THRESHOLD = 2  # minimum vehicles to consider detection reliable
STATIC_TIMER_ORDER = ["north", "east", "south", "west"]

# Initialize lanes data structure
def init_lanes():
    return {
        "north": {
            "vehicle_counts": {
                "motorcycle": 0,
                "truck": 0,
                "car": 0,
                "bus": 0,
                "autorickshaw": 0
            },
            "total_pcu": 0,
            "waiting_time": 0,
            "emergency_vehicles": 0,
            "priority_vehicles": 0,
            "green_time": 0,
            "is_green": False,
            "last_green": time.time()
        },
        "east": {
            "vehicle_counts": {
                "motorcycle": 0,
                "truck": 0,
                "car": 0,
                "bus": 0,
                "autorickshaw": 0
            },
            "total_pcu": 0,
            "waiting_time": 0,
            "emergency_vehicles": 0,
            "priority_vehicles": 0,
            "green_time": 0,
            "is_green": False,
            "last_green": time.time()
        },
        "south": {
            "vehicle_counts": {
                "motorcycle": 0,
                "truck": 0,
                "car": 0,
                "bus": 0,
                "autorickshaw": 0
            },
            "total_pcu": 0,
            "waiting_time": 0,
            "emergency_vehicles": 0,
            "priority_vehicles": 0,
            "green_time": 0,
            "is_green": False,
            "last_green": time.time()
        },
        "west": {
            "vehicle_counts": {
                "motorcycle": 0,
                "truck": 0,
                "car": 0,
                "bus": 0,
                "autorickshaw": 0
            },
            "total_pcu": 0,
            "waiting_time": 0,
            "emergency_vehicles": 0,
            "priority_vehicles": 0,
            "green_time": 0,
            "is_green": False,
            "last_green": time.time()
        }
    } 