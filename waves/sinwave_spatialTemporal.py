import numpy as np
import matplotlib.pyplot as plt

# Parameters
positive_peak = 0.085
negative_peak = -0.12
frequency = 2  # in Hz
wavelength = 1  # in meters
sampling_rate = 1000  # Sampling points per second
duration = 1  # in seconds
speed = wavelength * frequency  # Wave speed (m/s)

# Time and space arrays
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)  # Time array
x = np.linspace(0, 2 * wavelength, 500)  # Space array over two wavelengths

# Amplitude and offset
amplitude = (positive_peak - negative_peak) / 2
offset = (positive_peak + negative_peak) / 2
wavenumber = 2 * np.pi / wavelength  # k

# Oscillating wave (only time-dependent)
oscillating_wave = amplitude * np.sin(2 * np.pi * frequency * t) + offset

# Travelling wave (time and space-dependent)
X, T = np.meshgrid(x, t)  # Create 2D grids for space and time
travelling_wave = amplitude * np.sin(2 * np.pi * frequency * T - wavenumber * X) + offset

# Plotting
plt.figure(figsize=(15, 6))

# Subplot 1: Oscillating wave
plt.subplot(1, 2, 1)
plt.plot(t, oscillating_wave, label="Oscillating Wave")
plt.title("Oscillating Wave (Time-dependent)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

# Subplot 2: Travelling wave at different times
for time_index in [0, int(sampling_rate / 4), int(sampling_rate / 2), int(3 * sampling_rate / 4)]:
    plt.subplot(1, 2, 2)
    plt.plot(x, travelling_wave[time_index, :], label=f"t = {t[time_index]:.2f} s")
plt.title("Travelling Wave (Time and Space-dependent)")
plt.xlabel("Position (m)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()