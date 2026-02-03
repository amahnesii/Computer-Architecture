#"""
#Traffic Light System using Raspberry Pi GPIO
#--------------------------------------------

#Idle State:
#- Car: Green ON, Red OFF, Amber OFF
#- Pedestrian: Red ON, Green OFF

#Button Press Sequence:
#1) Car Amber ON (3 seconds)
#2) Car Red ON
#3) Pedestrian Green ON (15 seconds)
#4) Pedestrian Green blinks 5 times then OFF
#5) Pedestrian Red ON
#6) Car Red + Amber ON (3 seconds)
#7) Car Green ON (return to idle)
#"""

import RPi.GPIO as GPIO
import time

# -----------------------------
# GPIO PIN DEFINITIONS
# -----------------------------
CAR_RED = 17
CAR_AMBER = 27
CAR_GREEN = 22

PED_RED = 23
PED_GREEN = 24

BUTTON_PIN = 25

# -----------------------------
# SETUP GPIO MODE
# -----------------------------
GPIO.setmode(GPIO.BCM)

# Set LED pins as outputs
GPIO.setup(CAR_RED, GPIO.OUT)
GPIO.setup(CAR_AMBER, GPIO.OUT)
GPIO.setup(CAR_GREEN, GPIO.OUT)

GPIO.setup(PED_RED, GPIO.OUT)
GPIO.setup(PED_GREEN, GPIO.OUT)

# Set button as input with internal pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def set_car_lights(red=False, amber=False, green=False):
    """Turn car traffic LEDs ON/OFF."""
    GPIO.output(CAR_RED, red)
    GPIO.output(CAR_AMBER, amber)
    GPIO.output(CAR_GREEN, green)


def set_ped_lights(red=False, green=False):
    """Turn pedestrian LEDs ON/OFF."""
    GPIO.output(PED_RED, red)
    GPIO.output(PED_GREEN, green)


def idle_state():
    """
    Default state:
    - Car green ON
    - Ped red ON
    """
    set_car_lights(red=False, amber=False, green=True)
    set_ped_lights(red=True, green=False)


def pedestrian_blink_green(times=5, blink_delay=0.5):
    """
    Blink pedestrian green LED a number of times.
    After blinking, green is OFF.
    """
    for _ in range(times):
        GPIO.output(PED_GREEN, True)
        time.sleep(blink_delay)
        GPIO.output(PED_GREEN, False)
        time.sleep(blink_delay)


def button_sequence():
    """
    Run the full traffic light + pedestrian crossing sequence.
    """
    # Step 1: Car amber ON for 3 seconds
    set_car_lights(red=False, amber=True, green=False)
    time.sleep(3)

    # Step 2: Car red ON
    set_car_lights(red=True, amber=False, green=False)

    # Step 3: Pedestrian green ON, red OFF
    set_ped_lights(red=False, green=True)
    time.sleep(15)

    # Step 4: Pedestrian green blink 5 times then OFF
    pedestrian_blink_green(times=5, blink_delay=0.5)

    # Step 5: Pedestrian red ON (green OFF already)
    set_ped_lights(red=True, green=False)

    # Step 6: Car red + amber ON for 3 seconds
    set_car_lights(red=True, amber=True, green=False)
    time.sleep(3)

    # Step 7: Return to idle state (car green ON)
    idle_state()


# -----------------------------
# MAIN PROGRAM LOOP
# -----------------------------
try:
    print("Traffic Light System Running...")
    print("Press the button to start the pedestrian crossing sequence.")

    # Start system in idle state
    idle_state()

    while True:
        # Button press detection (active LOW)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed! Starting sequence...")

            # Debounce delay (prevents multiple triggers)
            time.sleep(0.3)

            # Run the crossing sequence
            button_sequence()

            # Wait until button released (prevents retrigger while held down)
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.1)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    # Turn everything OFF before cleanup
    set_car_lights(False, False, False)
    set_ped_lights(False, False)
    GPIO.cleanup()
    print("GPIO cleaned up. Exiting.")
