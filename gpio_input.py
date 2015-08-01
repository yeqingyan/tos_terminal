import RPi.GPIO as GPIO

# IMPORTANT
# This code is only for Raspberry Pi Model B, Pin number might change in different Model
# We use BCM for GPIO pin numbering
GPIO.setmode(GPIO.BCM)

led = 14
button = 18

GPIO.setup(led, GPIO.OUT)
