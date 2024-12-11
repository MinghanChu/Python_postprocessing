import plclcd
import pandas as pd
import matplotlib.pyplot as plt

# Enable LaTeX rendering for text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],  # Use LaTeX's default font
})

# Load data from file
data = pd.read_csv('coefficient.dat', delim_whitespace=True)

# Filter the DataFrame based on a condition for the "Time" column
time_min, time_max = 1.58, 2.33  # Specify the range for "Time"
filtered_data = data[(data['Time'] >= time_min) & (data['Time'] <= time_max)]

# Quantities to process
quantities = ['Cl', 'Cd']  # Add more column names here as needed

# Initialize a dictionary to store results
results = {}

# Process each quantity dynamically
for quantity in quantities:
    # Extract time and quantity values
    time_points = filtered_data['Time'].values
    quantity_values = filtered_data[quantity].values
    
    # Calculate time intervals (assuming non-uniform spacing)
    time_intervals = time_points[1:] - time_points[:-1]
    
    # Calculate the average as a weighted sum if time intervals are non-uniform
    # Slicing starts from the beginning of quantity_values and excludes the end index, the last element is omitted.
    # Note that you cannot factor 2*time_intervals outside the summation function because the time_intervals vary
    # across segments
    average = sum((quantity_values[:-1] + quantity_values[1:]) / 2 * time_intervals) / (time_points[-1] - time_points[0])
    
    # Store results
    count = len(quantity_values)
    results[quantity] = {'average': average, 'count': count}

# Write results to an output file
output_file = "output_info.txt"
with open(output_file, "w") as f:
    for quantity, result in results.items():
        f.write(f"{quantity}:\n")
        f.write(f"  Average: {result['average']}\n")
        f.write(f"  Count: {result['count']}\n")

# Print results to console for verification
for quantity, stats in results.items():
    print(f"Average {quantity}: {stats['average']}")
    print(f"Number of Rows ({quantity}): {stats['count']}")

print(f"The information has been saved to {output_file}.")

# Configuration: filename and figure size
filename = "Cd"
figsize = (16, 9)
figtitle = "$6^{\circ}$ AoA"
xrange = [0, max(data["Time"])]

match filename:
    case "Cl":
        yrange = [0, 1]
    case "Cd":
        yrange = [-0.01, 0.05]

linecolor = 'cornflowerblue'  # Options: lightsteelblue, slategrey, cornflowerblue
grid = True

# CFL and t values for vertical lines
indicator_lines = [
    #(100, 0),
    #(500, 0.000872681),
    #(1000, 0.0151339),
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
    indicator_lines=indicator_lines,  # Pass corrected indicator values
    ytick_remove=0,                   # -0.01 for Cd and none for Cl 
    text_yoffset=0.9,                 # Dynamic text offset for labels, e.g. text_yoffset = 0.9 for Cl and 0.055 for Cd
    text_xoffset=0.01,
    show_indicators=True              # Toggle indicators on/off
)