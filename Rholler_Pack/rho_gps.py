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


"""
HOW TO USE THIS SHIT

from rho_gps import GPSReader

# Initialize the GPS reader
gps_reader = GPSReader(port="/dev/ttyAMA0", baudrate=9600)

# Main loop
while True:
    gps_reader.update()  # Call update to refresh GPS data
    
    error, latitude, longitude = gps_reader.get_position()
    if error:
        print(error)  # Handle the case where GPS fix is not yet available
    else:
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        # Include latitude and longitude in your JSON payload here

    time.sleep(1)  # Adjust based on how frequently you want to poll the GPS

"""