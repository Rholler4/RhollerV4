"""
This script parses selected Python modules from the Rholler4/RhollerV4 repository
and extracts high–level information about the sensor classes defined therein.

The goal is to demonstrate how we can programmatically interact with code pulled
from a GitHub repository and derive meaningful metadata. We embed the raw
source code of several modules as multi‑line strings, then use Python's
``ast`` module to parse these strings into abstract syntax trees. From each AST
we look for top‑level ``ClassDef`` nodes and record the class name, any
docstring associated with the class, and the names and docstrings of all
methods defined on that class. The resulting summary is printed in a
readable format.

The modules included here correspond to sensor abstractions such as GPS,
temperature, gyroscope, and sonar. They were fetched via an internal
connector and reproduced verbatim below to allow offline analysis. The
analysis itself is generic and could be applied to any collection of Python
files.
"""

import ast
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MethodInfo:
    """Simple container to hold method metadata."""
    name: str
    doc: Optional[str] = None


@dataclass
class ClassInfo:
    """Container to hold class metadata and the methods it defines."""
    name: str
    doc: Optional[str] = None
    methods: List[MethodInfo] = field(default_factory=list)



def parse_module(name: str, source: str) -> List[ClassInfo]:
    """Parse a Python module string and extract class and method information.

    Parameters
    ----------
    name:
        The name of the module being parsed. Used only for logging.
    source:
        The raw source code of the module.

    Returns
    -------
    List[ClassInfo]
        A list of ``ClassInfo`` objects summarising the classes defined in
        ``source``.
    """
    tree = ast.parse(source, filename=name)
    classes: List[ClassInfo] = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node)
            class_info = ClassInfo(name=node.name, doc=class_doc)

            # iterate over class body to find functions (methods)
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_doc = ast.get_docstring(item)
                    class_info.methods.append(MethodInfo(name=item.name, doc=method_doc))

            classes.append(class_info)

    return classes



def main() -> None:
    """Parse all embedded modules and print a summary of their classes and methods."""
    files: Dict[str, str] = {
        "rho_temp.py": '''
# Then ready data in JSON to send to tkinter

# temp_sensor_module.py

import board
import adafruit_mcp9808


class TempSensor:
    def __init__(self):
        # Initialize I2C
        self.i2c = board.I2C()

        # Initialize MCP9808 temperature sensor
        self.sensor = adafruit_mcp9808.MCP9808(self.i2c)

    def read_temperature(self):
        """
        Reads the current temperature from the sensor.

        Returns:
            float: The current temperature in Fahrenheit.
        """
        tempC = self.sensor.temperature
        tempF = tempC * 9 / 5 + 32
        return tempF
''',
        "rho_gps.py": '''
# rho_gps.py
import time
import serial
import adafruit_gps


class GPSReader:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600):
        self.uart = serial.Serial(port, baudrate=baudrate, timeout=10)
        self.gps = adafruit_gps.GPS(self.uart, debug=False)
        # Modify the number of 1s in this to change functionality.
        # 0 means no data, 1 means every update, 2 means every second update, etc.
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # PMTK, 1000 is 1000 milliseconds between updates. 1 update/sec. 500 is 2/sec
        self.gps.send_command(b'PMTK220,500')

    def update(self):
        self.gps.update()

    def get_position(self):
        """
        Retrieves the current GPS position as latitude and longitude.

        Returns:
            tuple: A tuple containing an error message (if any) and the latitude and longitude.
                   If the GPS has not fixed on a location, 'Waiting for fix...'
                   is returned with None values for latitude and longitude.

                   If a fix is available, the tuple contains None for the error message
                   and the actual latitude and longitude values.
        """
        if not self.gps.has_fix:
            return 'Waiting for fix...', None, None
        latitude = self.gps.latitude if self.gps.latitude is not None else 'No Data'
        longitude = self.gps.longitude if self.gps.longitude is not None else 'No Data'
        return None, latitude, longitude
''',
        "rho_gyro.py": '''
# Send raw tilt data in JSON for laptop to decide on
# Laptop will indicate tilt risk and display in tkinter

# rho_gyro

import board
import digitalio
import adafruit_lis3dh


class GyroSensor:
    def __init__(self, threshold=10):
        # Initialize I2C
        self.i2c = board.I2C()

        # Set the correct pin for the interrupt
        int1 = digitalio.DigitalInOut(board.D6)

        # Initialize LIS3DH accelerometer
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(self.i2c, int1=int1)
        self.lis3dh.range = adafruit_lis3dh.RANGE_4_G

        # Set the threshold for tilt detection
        self.threshold = threshold

    def read_acceleration(self):
        """
        Reads the current acceleration and checks for tilt and significant Z-axis acceleration.

        Returns:
            dict: A dictionary containing the x and y tilt, and a flag indicating if the device has been picked up.
        """
        x, y, z = self.lis3dh.acceleration  # Read acceleration values
        tilt_detected = self.check_tilt(x, y)
        picked_up = self.check_pick_up(z)

        return {"x_tilt": x, "y_tilt": y, "picked_up": picked_up}

    def check_tilt(self, x, y):
        """
        Checks if the device is tilting beyond the specified threshold.

        Parameters:
            x (float): Acceleration in the X direction.
            y (float): Acceleration in the Y direction.

        Returns:
            bool: True if tilt is beyond the threshold, False otherwise.
        """
        tilt = max(abs(x), abs(y))  # Simplified tilt calculation
        return tilt > self.threshold

    def check_pick_up(self, z, pick_up_threshold=2):
        """
        Checks for significant Z-axis acceleration, indicating the device might have been picked up.

        Parameters:
            z (float): Acceleration in the Z direction.
            pick_up_threshold (float): The acceleration threshold to indicate a pick up.

        Returns:
            bool: True if significant Z-axis acceleration is detected, False otherwise.
        """
        # Assuming normal Z acceleration due to gravity is 1g (~9.8 m/s^2),
        # and any significant increase might indicate a pick up.
        return abs(z) > pick_up_threshold
''',
        "rho_sonar.py": '''
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
'''
    }

    # Parse each embedded module
    all_classes: Dict[str, List[ClassInfo]] = {}
    for filename, source in files.items():
        classes = parse_module(filename, source)
        all_classes[filename] = classes

    # Print a structured summary
    for module_name, classes in all_classes.items():
        print(f"Module: {module_name}\n" + "=" * (len(module_name) + 8))
        if not classes:
            print("  (No classes found)\n")
            continue
        for cls in classes:
            print(f"  Class: {cls.name}")
            if cls.doc:
                # indent docstring and limit long lines
                doc_lines = cls.doc.strip().splitlines()
                indented = ["    " + line.strip() for line in doc_lines]
                print("\n".join(indented))
            for method in cls.methods:
                print(f"    Method: {method.name}")
                if method.doc:
                    method_lines = method.doc.strip().splitlines()
                    indented = ["      " + line.strip() for line in method_lines]
                    print("\n".join(indented))
            print()


if __name__ == "__main__":
    main()
