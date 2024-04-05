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
        if not self.gps.has_fix:
            return 'Waiting for fix...', None, None
        latitude = self.gps.latitude if self.gps.latitude is not None else 'No Data'
        longitude = self.gps.longitude if self.gps.longitude is not None else 'No Data'
        return None, latitude, longitude
