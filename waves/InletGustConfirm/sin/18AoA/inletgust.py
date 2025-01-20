import pandas as pd
import matplotlib.pyplot as plt
import glob
import logging
import os

# Enable LaTeX rendering for text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],
})

# Configure logging
logging.basicConfig(
    filename="plot_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filemode="w",
)

# Configuration
figsize = (16, 9)
grid = True

# Let the user specify which velocity component to plot
print("Specify which velocity component to plot (x, y, z):")
component_to_plot = input("Enter 'x' for velocity_x, 'y' for velocity_y, or 'z' for velocity_z: ").strip().lower()

# Validate user input
if component_to_plot not in ['x', 'y', 'z']:
    print("Invalid input. Please enter 'x', 'y', or 'z'.")
    exit()

# Component mapping
component_map = {'x': 0, 'y': 1, 'z': 2}
component_index = component_map[component_to_plot]
figtitle = f"Time vs Velocity in {component_to_plot.upper()}-direction"

# Glob pattern to find all U files in the directory
u_files = glob.glob("./data/U*")  # Assuming files start with 'U'

if not u_files:
    print("No U files found in the specified directory.")
    exit()

# Initialize variables for plotting
data_list = []
labels = []
default_styles = ["--", "-.", ":"]
default_colors = ["red", "cornflowerblue", "orange", "magenta", "green"]
default_alphas = [0.5, 0.7, 0.9]

line_styles = []
line_colors = []
line_alphas = []

# Process each file
for i, u_file in enumerate(u_files):
    # Extract base filename without directory and extension
    file_base = os.path.splitext(os.path.basename(u_file))[0]

    # Read the U file
    with open(u_file, 'r') as f:
        lines = f.readlines()

    # Parse the data
    time = []
    velocity_x = []
    velocity_y = []
    velocity_z = []
    for line in lines:
        if line.strip() and not line.startswith("Time"):  # Skip empty lines and the header
            parts = line.split(maxsplit=1)  # Split into time and velocity parts
            try:
                time_val = float(parts[0])  # First part is time
                velocity_tuple = parts[1].strip("()\n").split()  # Remove parentheses and split into components
                velocity_x.append(float(velocity_tuple[0]))  # X-component
                velocity_y.append(float(velocity_tuple[1]))  # Y-component
                velocity_z.append(float(velocity_tuple[2]))  # Z-component
                time.append(time_val)  # Append time value
            except (ValueError, IndexError) as e:
                logging.warning(f"Skipping line due to error: {line.strip()} - {e}")
                continue

    # Create a DataFrame for consistent handling
    data = pd.DataFrame({
        'Time': time,
        'Velocity_X': velocity_x,
        'Velocity_Y': velocity_y,
        'Velocity_Z': velocity_z,
    })
    data_list.append(data)
    labels.append(file_base)  # Use the base filename as the label for the plot

    # Assign dynamic styles, colors, and alphas
    line_styles.append(default_styles[i % len(default_styles)])
    line_colors.append(default_colors[i % len(default_colors)])
    line_alphas.append(default_alphas[i % len(default_alphas)])

# Determine the x-range dynamically
if data_list:
    max_time = max(data["Time"].max() for data in data_list)
    xrange = [0, max_time]

# Log the dynamic x-range
logging.info("Dynamically calculated xrange: %s", xrange)

# Plotting
plt.figure(figsize=figsize)
for i, data in enumerate(data_list):
    # Plot the specified velocity component
    component_label = f"Velocity_{component_to_plot.upper()}"
    plt.plot(
        data["Time"], data[component_label],
        label=labels[i],
        linestyle=line_styles[i],
        color=line_colors[i],
        alpha=line_alphas[i]
    )

# Add plot formatting
plt.xlabel("Time (s)")
plt.ylabel(f"Velocity in {component_to_plot.upper()}-direction (m/s)")
plt.title(figtitle)
plt.legend()
plt.grid(grid)
plt.xlim(xrange)
plt.show()