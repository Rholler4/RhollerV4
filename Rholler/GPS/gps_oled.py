import time
import serial
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import busio
from board import SCL, SDA
import adafruit_gps

# Setup for GPS
uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
gps.send_command(b'PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1')  # Turn on the basic GGA and RMC info
gps.send_command(b'PMTK220,1000')  # Set update rate to once a second

# Setup for OLED display
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(0)  # Clear the display
display.show()
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    gps.update()
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Clear the screen
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)

    if not gps.has_fix:
        print('Waiting for fix...')
        draw.text((0, 0), 'Waiting for fix...', font=font, fill=255)
    else:
        # Print the GPS data
        latitude = gps.latitude if gps.latitude is not None else 'No Data'
        longitude = gps.longitude if gps.longitude is not None else 'No Data'
        print(f'Latitude: {latitude}, Longitude: {longitude}, Time: {current_time}')
        draw.text((0, 0), f'Lat: {latitude}', font=font, fill=255)
        draw.text((0, 15), f'Long: {longitude}', font=font, fill=255)

    # Display the image
    display.image(image)
    display.show()

    # Wait a bit before the next loop
    time.sleep(1)
