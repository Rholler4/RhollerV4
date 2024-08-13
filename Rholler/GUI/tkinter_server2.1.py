import socket
import threading
import tkinter as tk
from tkinter import ttk

# Global variables to hold data
latitude_var = None
longitude_var = None
tilt_x_var = None
tilt_y_var = None
temperature_var = None
cpu_usage_var = None
ram_usage_var = None
headlight_power_var = None
steering_angle_var = None
throttle_var = None
error_code_var = None


def update_data(data):
    try:
        fields = data.split(',')
        latitude_var.set(f"Latitude: {fields[0]}")
        longitude_var.set(f"Longitude: {fields[1]}")
        tilt_x_var.set(f"Tilt X: {fields[2]} degrees")
        tilt_y_var.set(f"Tilt Y: {fields[3]} degrees")
        temperature_var.set(f"Temperature: {fields[4]}F")
        cpu_usage_var.set(f"CPU Usage: {fields[5]}")
        ram_usage_var.set(f"RAM Usage: {fields[6]}")
        headlight_power_var.set(f"Headlight Power: {fields[7]}")
        steering_angle_var.set(f"Steering Angle: {fields[8]}")
        throttle_var.set(f"Throttle: {fields[9]}")
        error_code_var.set(f"Error Codes: {fields[10]}")
    except IndexError:
        print("Received data format error:", data)

def run_server():
    host = '127.0.0.1'  # Localhost
    port = 8713  # Arbitrary port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening for incoming connections...")

    conn, addr = server_socket.accept()
    print("Connected to:", addr)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received from client: {data}")
        update_data(data)

    conn.close()
    print("Connection closed.")

def start_server_thread():
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

# Tkinter GUI setup (from tkinter_test2.py)
def setup_gui():
    global latitude_var, longitude_var, tilt_x_var, tilt_y_var, temperature_var
    global cpu_usage_var, ram_usage_var, headlight_power_var, steering_angle_var, throttle_var, error_code_var

    root = tk.Tk()
    root.title("Vehicle Dashboard")

    # GPS Data
    gps_frame = ttk.LabelFrame(root, text="GPS Data")
    gps_frame.pack(fill="both", expand=1, padx=10, pady=5)

    latitude_var = tk.StringVar(value="Latitude: Empty")
    longitude_var = tk.StringVar(value="Longitude: Empty")
    tk.Label(gps_frame, textvariable=latitude_var).pack()
    tk.Label(gps_frame, textvariable=longitude_var).pack()

    # Tilt in Degrees
    tilt_frame = ttk.LabelFrame(root, text="Tilt")
    tilt_frame.pack(fill="both", expand=1, padx=10, pady=5)

    tilt_x_var = tk.StringVar(value="Tilt X: Empty degrees")
    tilt_y_var = tk.StringVar(value="Tilt Y: Empty degrees")
    tk.Label(tilt_frame, textvariable=tilt_x_var).pack()
    tk.Label(tilt_frame, textvariable=tilt_y_var).pack()

    # Temperature
    temperature_frame = ttk.LabelFrame(root, text="Temperature")
    temperature_frame.pack(fill="both", expand=1, padx=10, pady=5)

    temperature_var = tk.StringVar(value="Temperature: EmptyF")
    tk.Label(temperature_frame, textvariable=temperature_var).pack()

    # CPU and RAM Usage
    system_frame = ttk.LabelFrame(root, text="System Usage")
    system_frame.pack(fill="both", expand=1, padx=10, pady=5)

    cpu_usage_var = tk.StringVar(value="CPU Usage: Empty")
    ram_usage_var = tk.StringVar(value="RAM Usage: Empty")
    tk.Label(system_frame, textvariable=cpu_usage_var).pack()
    tk.Label(system_frame, textvariable=ram_usage_var).pack()

    # Headlight Power
    headlight_frame = ttk.LabelFrame(root, text="Headlight Power")
    headlight_frame.pack(fill="both", expand=1, padx=10, pady=5)

    headlight_power_var = tk.StringVar(value="Headlight Power: Empty")
    tk.Label(headlight_frame, textvariable=headlight_power_var).pack()

    # Error Codes
    error_frame = ttk.LabelFrame(root, text="Error Codes")
    error_frame.pack(fill="both", expand=1, padx=10, pady=5)

    error_code_var = tk.StringVar(value="Error Codes: Empty")
    tk.Label(error_frame, textvariable=error_code_var).pack()

    # Drivetrain Information
    drivetrain_frame = ttk.LabelFrame(root, text="Drivetrain")
    drivetrain_frame.pack(fill="both", expand=1, padx=10, pady=5)

    steering_angle_var = tk.StringVar(value="Steering Angle: Empty")
    throttle_var = tk.StringVar(value="Throttle: Empty")
    tk.Label(drivetrain_frame, textvariable=steering_angle_var).pack()
    tk.Label(drivetrain_frame, textvariable=throttle_var).pack()

    # Start the server thread
    start_server_thread()

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
