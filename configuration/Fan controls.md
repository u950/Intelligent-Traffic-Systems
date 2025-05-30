### enter in terminal for quick fan operations
```
sudo sh -c 'echo 255 > /sys/devices/pwm-fan/target_pwm'
```

# jetson-fan-ctl
Automagic fan control for the Nvidia Jetson Nano

## Requirements:

### Hardware
You will need a 5V PWM fan for this to make any sense.  
I used the **Noctua nf-a4x20 5V PWM** fan.

Also, I think you should use the barrel jack with a 4A power supply.  

### Software
I will assume you use the standard image on your Jetson Nano.

Python 3 should be pre-installed on the Jetson Nano.  
You can check this using <code>python3 --version</code>  
(3.5 or higher should be fine.)  
otherwise, you can install it with  

    sudo apt install python3-dev


## How to install:
run

    sudo ./install.sh

The script will automatically run at boot time.

It's a set-it-and-forget-it type thing, unless you want to mess with the fan speeds.

## How to customize:
open /etc/automagic-fan/config.json with your favorite editor (I'm using nano):  

    sudo nano /etc/automagic-fan/config.json

you will find the following lines:

    {
    "FAN_OFF_TEMP":20,
    "FAN_MAX_TEMP":50,
    "UPDATE_INTERVAL":2,
    "MAX_PERF":1
    }

<code>FAN_OFF_TEMP</code> is the temperature (°C) below which the fan is turned off.  
<code>FAN_MAX_TEMP</code> is the temperature (°C) above which the fan is at 100% speed.  
The script interpolates linearly between these two points.

<code>UPDATE_INTERVAL</code> tells the script how often to update the fan speed (in seconds).  
<code>MAX_PERF</code> values greater than 0 maximize system performance by setting the CPU and GPU clock speeds to the maximum. 

You can use either integers (like 20) or floating point numbers (like 20.125) in each of these fields.  
The temperature precision of the thermal sensors is 0.5 (°C), so don't expect this to be too precise.

Any changes in the script will be will be applied after the next reboot.  
You can run

    sudo service automagic-fan restart

to apply changes immediately.

If you suspect something went wrong, please check:

    sudo service automagic-fan status
