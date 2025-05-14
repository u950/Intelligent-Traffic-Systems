import Jetson.GPIO as GPIO
from config import GPIO_PINS

class GPIOController:
    def __init__(self):
        """Initialize GPIO controller"""
        GPIO.setmode(GPIO.BOARD)
        self.setup_pins()
    
    def setup_pins(self):
        """Setup all GPIO pins as outputs and set them to low initially"""
        for direction in GPIO_PINS:
            for color in GPIO_PINS[direction]:
                GPIO.setup(GPIO_PINS[direction][color], GPIO.OUT)
                GPIO.output(GPIO_PINS[direction][color], GPIO.LOW)
    
    def set_all_red(self):
        """Set all traffic lights to red"""
        for direction in GPIO_PINS:
            for color in GPIO_PINS[direction]:
                if color == "red":
                    GPIO.output(GPIO_PINS[direction][color], GPIO.HIGH)
                else:
                    GPIO.output(GPIO_PINS[direction][color], GPIO.LOW)
    
    def set_yellow(self, direction):
        """Set yellow light for specified direction, others red"""
        self.set_all_red()
        GPIO.output(GPIO_PINS[direction]["yellow"], GPIO.HIGH)
    
    def set_green(self, direction):
        """Set green light for specified direction, others red"""
        self.set_all_red()
        GPIO.output(GPIO_PINS[direction]["green"], GPIO.HIGH)
    
    def cleanup(self):
        """Clean up GPIO settings"""
        for direction in GPIO_PINS:
            for color in GPIO_PINS[direction]:
                GPIO.output(GPIO_PINS[direction][color], GPIO.LOW)
        GPIO.cleanup() 