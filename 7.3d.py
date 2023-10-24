# Import necessary libraries
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time

# GPIO pin configurations
led = 21                       # GPIO pin for controlling LED brightness
trigger = 18                   # GPIO pin for ultrasonic sensor trigger
echo = 24                      # GPIO pin for ultrasonic sensor echo

# Set up GPIO mode and pin configurations
GPIO.setwarnings(False)        
GPIO.setmode(GPIO.BCM)         
GPIO.setup(led, GPIO.OUT)      
GPIO.setup(trigger, GPIO.OUT)  
GPIO.setup(echo, GPIO.IN)      

# Set up PWM for LED control
pwm = GPIO.PWM(led, 100)       # Initialize PWM on LED pin with frequency 100 Hz
pwm.start(0)                    # Start PWM with duty cycle 0

# Function to measure distance using ultrasonic sensor
def distance():
    GPIO.output(trigger, True) 
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    Start = time.time()
    Stop = time.time()

    while GPIO.input(echo) == 0:
        Start = time.time()

    while GPIO.input(echo) == 1:
        Stop = time.time()

    TimeElapsed = Stop - Start
    distance = (TimeElapsed * 34300) / 2  # Calculate distance in centimeters using speed of sound

    return distance

try:
    while True:                      

        dist = distance()            # Measure distance using ultrasonic sensor
        print("Measured Distance = %.1f cm" % dist) 

        if dist > 400:              # If distance is greater than 400 cm, set brightness to 0 (LED off)
            x = 0
        else:
            x = 100 - (dist / 4)    # Calculate brightness based on distance (closer the object, brighter the LED)

        pwm.ChangeDutyCycle(x)       # Set LED brightness
        time.sleep(0.01)             # Delay to stabilize readings and reduce CPU usage

except KeyboardInterrupt:
    pass

# Cleanup GPIO configurations and stop PWM
pwm.stop()
GPIO.cleanup()
