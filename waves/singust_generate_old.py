import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Updated parameters for generated sine wave
positive_peak = 0.085
negative_peak = -0.11
frequency = 2  # in Hz
period = 1 / frequency  # in seconds
sampling_rate = 1000  # Sampling points per second
duration = period  # seconds

# Time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
t_norm = t / period  # Normalized time

# Amplitude and offset calculations
amplitude = (positive_peak - negative_peak) / 2  # New amplitude
offset = (positive_peak + negative_peak) / 2     # New offset
phase_shift = np.arcsin(-offset / amplitude)  # Phase shift to start at y = 0
sin_wave = amplitude * np.sin(2 * np.pi * frequency * t + phase_shift) + offset

# Directory containing the CSV files
data_folder = './data'
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Initialize variables for specific datasets
sinwave_exp_2_5c = None
sinwave_exp_0_5c = None

# Plotting the generated sine wave
plt.figure(figsize=(10, 5))
plt.plot(t_norm, sin_wave, label=f"Reconstructed sin gust (Frequency: {frequency} Hz)", linewidth=2)

# Loop through each CSV file, read the data, and plot
for file in csv_files:
    file_path = os.path.join(data_folder, file)
    data = pd.read_csv(file_path)  # Read the CSV file
    
    # Assuming the CSV files have two columns: 'Time' and 'Amplitude'
    time_data = data['Time'].values  # Time array
    amplitude_data = data['Amplitude'].values  # Amplitude array

    # Identify specific files for shading
    if 'sinwave_exp_2.5c' in file:
        sinwave_exp_2_5c = (time_data, amplitude_data)
        print(f"Found sinwave_exp_2.5c in {file}")
    elif 'sinwave_exp_0.5c' in file:
        sinwave_exp_0_5c = (time_data, amplitude_data)
        print(f"Found sinwave_exp_0.5c in {file}")
    # Remove file extension from the label
    base_name = os.path.splitext(file)[0]

    # Plotting the sine wave from the file
    plt.plot(time_data, amplitude_data, label=f"{base_name}", linestyle='--', linewidth=1.5)

# Handle inconsistent time arrays and fill the area
if sinwave_exp_2_5c and sinwave_exp_0_5c:
    time_2_5c, amplitude_2_5c = sinwave_exp_2_5c
    time_0_5c, amplitude_0_5c = sinwave_exp_0_5c
    print("Filling area between sinwave_exp_2.5c and sinwave_exp_0.5c")
    
    # Find overlapping time range
    common_start = max(time_2_5c.min(), time_0_5c.min())
    common_end = min(time_2_5c.max(), time_0_5c.max())
    common_time = np.linspace(common_start, common_end, num=1000)  # Define a common time grid
    
    # Interpolate both signals onto the common time grid
    amplitude_2_5c_interp = np.interp(common_time, time_2_5c, amplitude_2_5c)
    amplitude_0_5c_interp = np.interp(common_time, time_0_5c, amplitude_0_5c)

    # Fill the area between the interpolated sine waves
    plt.fill_between(common_time, amplitude_0_5c_interp, amplitude_2_5c_interp, color='grey', alpha=0.5, label='Variation Area')

# Adding details to the plot
plt.axhline(positive_peak, color='k', linestyle='--', label='Positive Peak')
plt.axhline(negative_peak, color='k', linestyle=':', label='Negative Peak')

# Customizing the legend
legend = plt.legend(
    loc='lower left',         # Position the legend
    fontsize=10,              # Set font size
    ncol=1,                   # Single-column legend
    frameon=True,             # Enable border
    shadow=False,             # Add shadow
    fancybox=True,            # Rounded corners
    framealpha=0.8            # Slightly transparent background
)

# Customizing legend frame and text
legend.get_frame().set_facecolor('lightyellow')  # Background color
legend.get_frame().set_edgecolor('black')       # Border color
plt.title("Comparison of Generated Sine Wave and Data from Files")
plt.xlabel("$t/T$")
plt.ylabel("$v/U$")
plt.grid()
plt.show()