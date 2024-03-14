# ABANDONED ===============

import subprocess

# Define the IP address and port of the receiving PC
receiver_ip = "192.168.1.189"  # Change to the IP address of your receiver PC
receiver_port = "5005"         # Change to your preferred port

# Command to capture video from the camera using libcamera-vid
capture_command = [
    'libcamera-vid',
    '-t', '0',                     # Keep running indefinitely
    '--inline',                    # Necessary for H264 streaming
    '--codec', 'h264',             # Use H264 codec
    '-o', '-'                      # Output to stdout
]

# Command to stream video using ffmpeg over UDP
stream_command = [
    'ffmpeg',
    '-i', '-',                     # Input from stdin
    '-f', 'mpegts',                # Format for streaming
    'udp://{}:{}'.format(receiver_ip, receiver_port)  # Destination IP and port
]

# Set up the libcamera-vid process
capture_process = subprocess.Popen(capture_command, stdout=subprocess.PIPE)

# Set up the ffmpeg streaming process
stream_process = subprocess.Popen(stream_command, stdin=capture_process.stdout)

try:
    capture_process.wait()  # Wait for the capture process to finish (which should be never under normal circumstances)
except KeyboardInterrupt:
    # Handle Ctrl+C to gracefully close both processes
    capture_process.terminate()
    stream_process.terminate()
