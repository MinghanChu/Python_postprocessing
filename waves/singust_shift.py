import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Enable LaTeX rendering for text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],
})

# Configure logging
logging.basicConfig(
    filename="comparison_plot_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filemode="w",
)

# Configuration
figsize = (16, 9)
grid = True

# Directory paths
data_U_folder = "./data_shift"

# Freestream velocity and normalization factors
freestream_velocity = 20  # Normalization factor for velocity
time_normalization = 0.5  # Period for time normalization

# Load U* files
u_files = glob.glob(os.path.join(data_U_folder, "U*"))
if not u_files:
    print(f"No U files found in {data_U_folder}")
    exit()

# User input for velocity component
print("Specify which velocity component to plot (x, y, z):")
component_to_plot = input("Enter 'x' for velocity_x, 'y' for velocity_y, or 'z' for velocity_z: ").strip().lower()

if component_to_plot not in ['x', 'y', 'z']:
    print("Invalid input. Please enter 'x', 'y', or 'z'.")
    exit()

# Get user-defined offset values for x, y, z, and time
try:
    x_offset = float(input("Enter x-axis offset value: "))
    y_offset = float(input("Enter y-axis offset value: "))
    z_offset = float(input("Enter z-axis offset value: "))
    time_offset = float(input("Enter time shift value: "))  # New time shift input
except ValueError:
    print("Invalid input. Please enter numeric values for offsets.")
    exit()

# Component mapping
component_map = {'x': 0, 'y': 1, 'z': 2}
component_index = component_map[component_to_plot]
figtitle = f"Time vs Velocity in {component_to_plot.upper()}-direction"

# Process U* files
output_file = "shifted_data.txt"
with open(output_file, "w") as out_f:
    out_f.write("# Probe 0 (-1 0 0)\n")
    out_f.write("# Time        0\n")

    for u_file in u_files:
        file_base = os.path.splitext(os.path.basename(u_file))[0]

        # Parse U* files
        with open(u_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("Time"):
                    parts = line.split(maxsplit=1)
                    try:
                        time_val = float(parts[0]) / time_normalization + time_offset  # Apply time shift
                        velocity_tuple = parts[1].strip("()\n").split()
                        velocity_x = float(velocity_tuple[0]) / freestream_velocity + x_offset
                        velocity_y = float(velocity_tuple[1]) / freestream_velocity + y_offset
                        velocity_z = float(velocity_tuple[2]) / freestream_velocity + z_offset

                        # Write formatted output
                        out_f.write(f"{time_val:.7f}     ({velocity_x:.4f} {velocity_y:.6e} {velocity_z:.6f})\n")

                    except (ValueError, IndexError) as e:
                        logging.warning(f"Skipping line in {u_file} due to error: {e}")
                        continue

print(f"Shifted data has been saved to {output_file}")