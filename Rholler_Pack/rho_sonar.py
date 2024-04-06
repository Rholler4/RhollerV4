# Needs to run sonar turning script and log data
# Send angle and distance in JSON to laptop
import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from adafruit_servokit import ServoKit
from time import sleep
import socket


class SweepingSonar:
    def __init__(self):
        # Set gpiozero to use the pigpio pin factory
        gpiozero.Device.pin_factory = PiGPIOFactory()

        # Initialize distance sensors
        self.sensor1 = DistanceSensor(echo=27, trigger=17)
        self.sensor2 = DistanceSensor(echo=23, trigger=22)

        # Initialize servos
        self.kit = ServoKit(channels=16)
        self.setup_servos()

        # Scanning state
        self.scanning = False

        # Initialize scan data storage
        self.scan_data = []

    def setup_servos(self):
        def setup_servos(self):
            # Set frequency
            # TODO Check this frequency shit
            pca.frequency = 100
            self.kit.servo[0].actuation_range = 270
            self.kit.servo[1].actuation_range = 270
            self.kit.servo[0].set_pulse_width_range(500, 2500)
            self.kit.servo[1].set_pulse_width_range(500, 2500)
            # Initial angles
            self.current_angle_0 = 0
            self.current_angle_1 = 0
            self.kit.servo[0].angle = self.current_angle_0
            self.kit.servo[1].angle = self.current_angle_1

    def start_scan(self):
        self.scan_data = []  # Reset scan data
        self.scanning = True
        self.perform_scan()

    def stop_scan(self):
        self.scanning = False
        # Optional: Reset servos to default position

    def perform_scan(self):
        while self.scanning:
            # TODO Perform scanning logic here...
            # Update self.scan_data with the results

            # Example:
            distance1 = self.sensor1.distance * 100  # Convert to centimeters
            distance2 = self.sensor2.distance * 100  # Convert to centimeters
            current_angle_0, current_angle_1 = self.get_current_angles()

            # Append scan result to scan_data
            self.scan_data.append({
                "distance1": distance1,
                "distance2": distance2,
                "angle1": current_angle_0,
                "angle2": current_angle_1
            })

            sleep(1)  # Adjust delay as needed

    def get_current_angles(self):
        # Logic to get current servo angles
        return current_angle_0, current_angle_1

    def get_scan_data(self):
        return self.scan_data

"""
HOW THIS SHIT WORKS

sonar = SweepingSonar()
sonar.start_scan()  # Start scanning

# Later, when you want to stop scanning and retrieve data
sonar.stop_scan()
scan_data = sonar.get_scan_data()

# Add scan_data to your JSON payload
payload = {
    "sonar_data": scan_data
}

"""