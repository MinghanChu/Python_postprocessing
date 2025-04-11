from config import *
from file_processing import load_u_files, load_csv_files
from plotting import plot_velocity_data, plot_csv_data, plot_generated_wave, finalize_plot
import numpy as np

# Set figure size once here
plt.figure(figsize=(16, 9))

custom_colors = ["green", "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

# Load data
data_list_u, labels_u = load_u_files(data_U_folder, freestream_velocity, time_normalization)
data_list_csv, labels_csv, sinwave_exp_2_5c, sinwave_exp_0_5c = load_csv_files(data_csv_folder)

# Plot data
component_to_plot = "z"
plot_velocity_data(data_list_u, labels_u, component_to_plot, custom_colors)
plot_csv_data(data_list_csv, labels_csv, custom_colors)



# Generated sine wave parameters
positive_peak = 0.085
negative_peak = -0.11
frequency = 2  # in Hz
period = 1 / frequency  # in seconds
sampling_rate = 1000  # Sampling points per second

# Time array for the sine wave
t = np.linspace(0, period, int(sampling_rate * period), endpoint=False)
t_norm = t / period  # Normalized time

# Amplitude and offset calculations
amplitude = (positive_peak - negative_peak) / 2  # New amplitude
offset = (positive_peak + negative_peak) / 2     # New offset
phase_shift = np.arcsin(-offset / amplitude)  # Phase shift to start at y = 0
sin_wave = amplitude * np.sin(2 * np.pi * frequency * t + phase_shift) + offset

original_sin_wave = amplitude * np.sin(2 * np.pi * frequency * t) 

# Generate sine wave and plot
#t_norm = np.linspace(0, 1, 1000)
#sin_wave = np.sin(2 * np.pi * t_norm)
#original_sin_wave = sin_wave
plot_generated_wave(t_norm, sin_wave, original_sin_wave)


# Finalize plot
finalize_plot("Comparison of Velocity Data", component_to_plot, grid, 0.085, -0.11)

