import tkinter as tk
from tkinter import ttk

# Init variables
cpu_usage_data = str("Empty")
ram_usage_data = str("Empty")
latitude_data = str("Empty")
longitude_data = str("Empty")
tilt_x_data = str("Empty")
tilt_y_data = str("Empty")
temperature_data = str("Empty")
headlight_power_data = str("Empty")
steering_angle_data = str("Empty")
throttle_data = str("Empty")
error_code_data = str("Empty")

# Function to toggle sonar status
def toggle_sonar():
    global sonar_status
    sonar_status = not sonar_status
    sonar_status_var.set("On" if sonar_status else "Off")

# Initialize the main window
root = tk.Tk()
root.title("Vehicle Dashboard")

# Use a global variable for sonar status for demonstration
sonar_status = False

# GPS Data
gps_frame = ttk.LabelFrame(root, text="GPS Data")
gps_frame.pack(fill="both", expand="yes", padx=10, pady=5)

latitude_var = tk.StringVar(value="Latitude: " + latitude_data)
longitude_var = tk.StringVar(value="Longitude: " + longitude_data)
tk.Label(gps_frame, textvariable=latitude_var).pack()
tk.Label(gps_frame, textvariable=longitude_var).pack()

# Tilt in Degrees
tilt_frame = ttk.LabelFrame(root, text="Tilt")
tilt_frame.pack(fill="both", expand="yes", padx=10, pady=5)

tilt_x_var = tk.StringVar(value="Tilt X: " + tilt_x_data + " degrees")
tilt_y_var = tk.StringVar(value="Tilt Y: " + tilt_y_data + " degrees")
tk.Label(tilt_frame, textvariable=tilt_x_var).pack()
tk.Label(tilt_frame, textvariable=tilt_y_var).pack()

# Temperature
temperature_frame = ttk.LabelFrame(root, text="Temperature")
temperature_frame.pack(fill="both", expand="yes", padx=10, pady=5)

temperature_var = tk.StringVar(value="Temperature: " + temperature_data + "F")
tk.Label(temperature_frame, textvariable=temperature_var).pack()

# CPU and RAM Usage
system_frame = ttk.LabelFrame(root, text="System Usage")
system_frame.pack(fill="both", expand="yes", padx=10, pady=5)

cpu_usage_var = tk.StringVar(value="CPU Usage: " + cpu_usage_data)
ram_usage_var = tk.StringVar(value="RAM Usage: " + ram_usage_data)
tk.Label(system_frame, textvariable=cpu_usage_var).pack()
tk.Label(system_frame, textvariable=ram_usage_var).pack()

# Headlight Power
headlight_frame = ttk.LabelFrame(root, text="Headlight Power")
headlight_frame.pack(fill="both", expand="yes", padx=10, pady=5)

headlight_power_var = tk.StringVar(value="Headlight Power: " + headlight_power_data)
tk.Label(headlight_frame, textvariable=headlight_power_var).pack()

# Error Codes
error_frame = ttk.LabelFrame(root, text="Error Codes")
error_frame.pack(fill="both", expand="yes", padx=10, pady=5)

error_code_var = tk.StringVar(value="Error Codes: " + error_code_data)
tk.Label(error_frame, textvariable=error_code_var).pack()

# Sonar Status
sonar_frame = ttk.LabelFrame(root, text="Sonar Status")
sonar_frame.pack(fill="both", expand="yes", padx=10, pady=5)

sonar_status_var = tk.StringVar(value="Off")
tk.Label(sonar_frame, textvariable=sonar_status_var).pack()
tk.Button(sonar_frame, text="Toggle Sonar", command=toggle_sonar).pack()

# Drivetrain Information
drivetrain_frame = ttk.LabelFrame(root, text="Drivetrain")
drivetrain_frame.pack(fill="both", expand="yes", padx=10, pady=5)

steering_angle_var = tk.StringVar(value="Steering Angle: " + steering_angle_data)
throttle_var = tk.StringVar(value="Throttle: " + throttle_data)
tk.Label(drivetrain_frame, textvariable=steering_angle_var).pack()
tk.Label(drivetrain_frame, textvariable=throttle_var).pack()

# Start the main loop
root.mainloop()
