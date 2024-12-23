import numpy as np
import matplotlib.pyplot as plt

# Define parameters
U_freestream_magnitude = 20      # Freestream velocity magnitude (m/s)
angle_deg = 10                   # Angle of the freestream velocity (degrees)
angle_rad = np.radians(angle_deg)  # Convert angle to radians

# Compute components of freestream velocity
U_freestream_x = U_freestream_magnitude * np.cos(angle_rad)  # x-component
U_freestream_y = U_freestream_magnitude * np.sin(angle_rad)  # y-component

amplitude = 2.0        # Amplitude of fluctuations in the z-direction
period = 0.5           # Time period of the wave (s)
omega = 2.0 * np.pi / period  # Angular frequency (rad/s)
k = 1                # Wavenumber for spatial dependence

t = np.linspace(0, 2, 1000)  # Time from 0 to 2 seconds


# Define wave components
x_position = U_freestream_x * t  # Wave moving in the x-direction
y_position = U_freestream_y * t  # Wave moving in the y-direction
z_wave1 = amplitude * np.sin(omega * t + k * y_position)  # A*sin(omega*t + k*y)
z_wave2 = amplitude * (1 - np.cos(omega * t + k * y_position))  # A*(1 - cos(omega*t + k*y))

# Combine components into vector representation
vector_wave1 = np.vstack((x_position, y_position, z_wave1))  # Wave 1 (x, y, z)
vector_wave2 = np.vstack((x_position, y_position, z_wave2))  # Wave 2 (x, y, z)

# Plot the waves
plt.figure(figsize=(10, 6))

# Plot z-components (amplitude fluctuations) as a function of distance in x
plt.plot(x_position, z_wave1, label=r"$A \sin(\omega t + k y)$", color="blue", linewidth=2)
plt.plot(x_position, z_wave2, label=r"$A(1 - \cos(\omega t + k y))$", color="red", linestyle="--", linewidth=2)

# Add labels, legend, and grid
plt.title("Wave Propagation with Amplitude Affected by y-Position", fontsize=16)
plt.xlabel("Position in x-Direction (m)", fontsize=14)
plt.ylabel("Amplitude in z-Direction (m)", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# Show the plot
plt.show()

# Print the vector representation for inspection
print("Vector representation of wave 1 (x, y, z):")
print(vector_wave1)

print("\nVector representation of wave 2 (x, y, z):")
print(vector_wave2)