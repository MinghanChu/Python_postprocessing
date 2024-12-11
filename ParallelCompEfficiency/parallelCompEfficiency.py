import matplotlib.pyplot as plt

# Enable LaTeX rendering for text （uncomment for English labels/captions）
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],  # Use LaTeX's default font
})

# Configure the font and enable Chinese character support
#plt.rcParams.update({
#    "font.family": "sans-serif",
#    "font.sans-serif": ["PingFang HK"],  # SimHei is a common Chinese font; adjust as needed
#    "axes.unicode_minus": False  # Ensure minus signs are rendered correctly
#})

# Enable LaTeX rendering for text for English
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],  # Use LaTeX's default font
})

# Data: Replace with your simulation results
processors = [1, 300, 600, 900, 1200]  # Number of CPUs
execution_time = [102951, 552, 329, 273, 232]  # Time in seconds
speedup = [execution_time[0] / t for t in execution_time]  # Speedup calculation
efficiency = [s / p for s, p in zip(speedup, processors)]  # Efficiency calculation

# Create a figure with two subplots
#fig, axs = plt.subplots(1, 2, figsize=(15, 5))  # 1 row, 2 columns
# Create a figure with two subplots arranged vertically
fig, axs = plt.subplots(2, 1, figsize=(8, 10))  # 2 rows, 1 column

"""# Subplot 1: Speedup vs. CPUs
axs[0].plot(processors, speedup, marker='o', label='加速比（SpeedUp）')
axs[0].plot(processors, processors, '--', label='理想加速比 (S=n)')
axs[0].set_xlabel('CPU数量 （n）')
axs[0].set_ylabel('加速比（S）')
axs[0].set_title('加速比 vs. CPU 数量')
axs[0].legend()
axs[0].grid()

# Subplot 2: Efficiency vs. CPUs
axs[1].plot(processors, efficiency, marker='o', label='并行效率（Paralle Efficiency）')
axs[1].axhline(1.0, color='r', linestyle='--', label='100% 并行效率')
axs[1].set_xlabel('CPU 数量 （n）')
axs[1].set_ylabel('并行效率 (%)')
axs[1].set_title('并行效率 vs. CPU 数量')
axs[1].legend()
axs[1].grid()
"""

#English version
# Subplot 1: Speedup vs. CPUs
axs[0].plot(processors, speedup, marker='o', label='Measured Speedup')
axs[0].plot(processors, processors, '--', label='Ideal Speedup (S=n)')
axs[0].set_xlabel('Number of CPUs')
axs[0].set_ylabel('Speedup')
axs[0].set_title('Speedup vs. Number of CPUs')
axs[0].legend()
axs[0].grid()

# Subplot 2: Efficiency vs. CPUs
axs[1].plot(processors, efficiency, marker='o', label='Parallel Efficiency')
axs[1].axhline(1.0, color='r', linestyle='--', label='100% Efficiency')
axs[1].set_xlabel('Number of CPUs')
axs[1].set_ylabel('Efficiency (%)')
axs[1].set_title('Parallel Efficiency vs. Number of CPUs')
axs[1].legend()
axs[1].grid()



# Adjust layout for better spacing
plt.tight_layout()

# Save the combined figure as a PDF
plt.savefig("parallel_performance.pdf", format='pdf', bbox_inches='tight')
plt.show()