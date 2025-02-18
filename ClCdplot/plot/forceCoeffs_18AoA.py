import os
import glob
import plclcd
import pandas as pd
import matplotlib.pyplot as plt

# Enable LaTeX rendering for text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],
})

# Directory containing the .txt files
data_folder = "./data_averageCl"

# Find all .txt files in the data folder
data_files = glob.glob(os.path.join(data_folder, "*.dat"))

if not data_files:
    print(f"No .txt files found in {data_folder}.")
    exit()

# Specify time range for filtering
time_min, time_max = 0.47, 0.96

# Quantities to process
quantities = ['Cl', 'Cd']  # Add more column names as needed

# Initialize a dictionary to store results
results = {}

# Process each data file
for file_path in data_files:
    file_name = os.path.basename(file_path)  # Extract the file name for reference
    
    # Load data from the file
    data = pd.read_csv(file_path, delim_whitespace=True)

    # Filter the DataFrame based on the time range
    filtered_data = data[(data['Time'] >= time_min) & (data['Time'] <= time_max)]

    # Process each quantity dynamically
    for quantity in quantities:
        if quantity in filtered_data.columns:
            # Extract time and quantity values
            time_points = filtered_data['Time'].values
            quantity_values = filtered_data[quantity].values
            
            # Calculate time intervals (assuming non-uniform spacing)
            time_intervals = time_points[1:] - time_points[:-1]

            # Calculate weighted average
            average = sum((quantity_values[:-1] + quantity_values[1:]) / 2 * time_intervals) / (time_points[-1] - time_points[0])
            
            # Store results
            count = len(quantity_values)
            results[(file_name, quantity)] = {'average': average, 'count': count}

# Write results to an output file
output_file = "output_info.txt"
with open(output_file, "w") as f:
    for (file_name, quantity), result in results.items():
        f.write(f"File: {file_name}, {quantity}:\n")
        f.write(f"  Average: {result['average']}\n")
        f.write(f"  Count: {result['count']}\n\n")

# Print results to console for verification
for (file_name, quantity), stats in results.items():
    print(f"File: {file_name}, Average {quantity}: {stats['average']}")
    print(f"File: {file_name}, Number of Rows ({quantity}): {stats['count']}")

print(f"The information has been saved to {output_file}.")

# Plotting Configuration
filename = "Cl"
figsize = (16, 9)
figtitle = "$18^{\circ}$ AoA"

# Set x-range dynamically based on max time value
xrange = [0, max(data["Time"])]

match filename:
    case "Cl":
        yrange = [0, 1.25]
    case "Cd":
        yrange = [0.15, 1]

linecolor = 'cornflowerblue'
grid = True

# CFL and t values for vertical lines
indicator_lines = [
    (1500, 0.0585484),
    (2000, 0.585309),
    (2500, 0.821048),
    (1500, 1.48408)
]

# Call the plotting function with indicators
plclcd.plot_coefficients(
    data=data,
    filename=filename,
    figtitle=figtitle,
    figsize=figsize,
    xrange=xrange,
    yrange=yrange,
    linecolor=linecolor,
    grid=grid,
    indicator_lines=indicator_lines,
    ytick_remove=0,  
    text_yoffset=0.055,  
    text_xoffset=0.01,
    show_indicators=False  
)