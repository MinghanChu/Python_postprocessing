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
data_U_folder = "./data_U"
data_csv_folder = "./data"


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

# Component mapping
component_map = {'x': 0, 'y': 1, 'z': 2}
component_index = component_map[component_to_plot]
figtitle = f"Time vs Velocity in {component_to_plot.upper()}-direction"

# Process U* files
data_list_u = []
labels_u = []
for u_file in u_files:
    file_base = os.path.splitext(os.path.basename(u_file))[0]

    # Parse U* files
    time, velocity_x, velocity_y, velocity_z = [], [], [], []
    with open(u_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith("Time"):
                parts = line.split(maxsplit=1)
                try:
                    time_val = float(parts[0]) / time_normalization  # Normalize time
                    velocity_tuple = parts[1].strip("()\n").split()
                    velocity_x.append(float(velocity_tuple[0]) / freestream_velocity)  # Normalize velocity
                    velocity_y.append(float(velocity_tuple[1]) / freestream_velocity)
                    velocity_z.append(float(velocity_tuple[2]) / freestream_velocity)
                    time.append(time_val)
                except (ValueError, IndexError) as e:
                    logging.warning(f"Skipping line in {u_file} due to error: {e}")
                    continue

    data = pd.DataFrame({
        'Time': time,
        'Velocity_X': velocity_x,
        'Velocity_Y': velocity_y,
        'Velocity_Z': velocity_z,
    })
    data_list_u.append(data)
    labels_u.append(file_base)

# Load CSV files
csv_files = [f for f in os.listdir(data_csv_folder) if f.endswith('.csv')]
if not csv_files:
    print(f"No CSV files found in {data_csv_folder}")
    exit()

# Process CSV files
data_list_csv = []
labels_csv = []
sinwave_exp_2_5c = None
sinwave_exp_0_5c = None

for csv_file in csv_files:
    file_path = os.path.join(data_csv_folder, csv_file)
    data = pd.read_csv(file_path)
    if 'Time' in data.columns and 'Amplitude' in data.columns:
        data_list_csv.append(data)
        labels_csv.append(os.path.splitext(csv_file)[0])

        # Identify specific files for filling
        if 'sinwave_exp_2.5c' in csv_file:
            sinwave_exp_2_5c = (data['Time'].values, data['Amplitude'].values)
        elif 'sinwave_exp_0.5c' in csv_file:
            sinwave_exp_0_5c = (data['Time'].values, data['Amplitude'].values)
    else:
        logging.warning(f"Skipping {csv_file} as it does not contain required columns.")

# Generated sine wave parameters
positive_peak = 0.085
negative_peak = -0.11
frequency = 2  # in Hz
period = 1 / frequency  # in seconds
sampling_rate = 1000  # Sampling points per second
duration = period  # seconds
free_stream_velocity = 20  # m/s

# Time array for the sine wave
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
t_norm = t / period  # Normalized time

# Amplitude and offset calculations
amplitude = (positive_peak - negative_peak) / 2  # New amplitude
offset = (positive_peak + negative_peak) / 2     # New offset
phase_shift = np.arcsin(-offset / amplitude)  # Phase shift to start at y = 0
sin_wave = amplitude * np.sin(2 * np.pi * frequency * t + phase_shift) + offset

original_sin_wave = amplitude * np.sin(2 * np.pi * frequency * t) 

# Plotting
plt.figure(figsize=figsize)

# Define a list of custom colors for lines and markers
custom_colors = ["green", "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]  # Add more as needed

# Plot OpenFOAM inlet gust U* data
for i, data in enumerate(data_list_u):
    component_label = f"Velocity_{component_to_plot.upper()}"
    #(len(data_list_u))
    plt.plot(
        data["Time"], data[component_label],
        label=f"OF Inlet gust: {labels_u[i]}",
        linestyle=None, 
        linewidth=1.5,
        color = custom_colors[i % len(custom_colors)],
        #color=f"C{i}", #The C{i} syntax in Matplotlib is shorthand for accessing the default color cycle. 
        #color = custom_colors[i % len(custom_colors)],
        marker="o",                    # Open circle marker
        markersize=1,                  # Size of the marker
        markerfacecolor="none",        # Open marker
        markeredgewidth=1.5,           # Thickness of marker edge
        #color=custom_colors[i % len(custom_colors)],           # Line color
        markeredgecolor=custom_colors[i % len(custom_colors)]  # Marker edge color
    )


# Plot CSV data
for i, data in enumerate(data_list_csv):
    plt.plot(
        data['Time'], data['Amplitude'],
        label=f"CSV Data: {labels_csv[i]}",
        linestyle=":",
        linewidth=1.5, 
        marker="o",                    # Open circle marker
        markersize=6,                  # Size of the marker
        markerfacecolor="none",        # Open marker
        markeredgewidth=1.5,           # Thickness of marker edge
        color=custom_colors[i + 1 % len(custom_colors)],           # Line color
        markeredgecolor=custom_colors[i+1 % len(custom_colors)]  # Marker edge color
        #color=f"C{i + len(data_list_u)}" # Automatically generate distinct colors
    )

# Plot generated sine wave
plt.plot(
    t_norm, sin_wave,
    label="Reconstructed ($A\sin(\omega t + 0.128559) -0.25$)",
    linestyle="-", 
    linewidth=2,
    color="red",
    alpha=0.5
)

# Plot generated sine wave
plt.plot(
    t_norm, original_sin_wave,
    label="$A\sin(\omega t)$",
    linestyle="-", 
    linewidth=2,
    color="k",
    alpha=0.5
)

# Fill area between specific CSV datasets
if sinwave_exp_2_5c and sinwave_exp_0_5c:
    time_2_5c, amplitude_2_5c = sinwave_exp_2_5c
    time_0_5c, amplitude_0_5c = sinwave_exp_0_5c
    
    # Find overlapping time range
    common_start = max(time_2_5c.min(), time_0_5c.min())
    common_end = min(time_2_5c.max(), time_0_5c.max())
    common_time = np.linspace(common_start, common_end, num=1000)
    
    # Interpolate onto the common time grid
    amplitude_2_5c_interp = np.interp(common_time, time_2_5c, amplitude_2_5c)
    amplitude_0_5c_interp = np.interp(common_time, time_0_5c, amplitude_0_5c)
    
    # Fill the area
    plt.fill_between(
        common_time, amplitude_0_5c_interp, amplitude_2_5c_interp,
        color='grey', alpha=0.3, label='Variation Area'
    )

# Add horizontal lines for positive and negative peaks
plt.axhline(positive_peak, color="grey", linestyle="--", label="Positive Peak")
plt.axhline(negative_peak, color="grey", linestyle="-.", label="Negative Peak")

# Customizing the legend
legend = plt.legend(
    loc='lower left',         # Position the legend
    fontsize=10,              # Set font size
    ncol=1,                   # Single-column legend
    frameon=True,             # Enable border
    shadow=False,             # Add shadow
    fancybox=True,            # Rounded corners
    framealpha=0.9            # Slightly transparent background
)

# Customizing legend frame and text
legend.get_frame().set_facecolor('lightyellow')  # Background color (lightyellow)
legend.get_frame().set_edgecolor('black')       # Border color

# Add plot formatting
plt.title("Comparison of Velocity Data from OF InletGust, Experiment, and Reconstructed Sine Wave")
plt.xlabel("$t/T$")
plt.ylabel(f"$v/U$ for {component_to_plot.upper()}-direction")
plt.grid(grid)

plt.savefig(f"results/sinGust_comp.pdf", bbox_inches='tight', format='pdf')

plt.show()