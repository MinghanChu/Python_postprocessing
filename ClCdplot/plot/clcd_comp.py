import plclcd_comp
import pandas as pd
import matplotlib.pyplot as plt
import glob
import logging
import os

# Enable LaTeX rendering for text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],  # Use LaTeX's default font
})

# Configure logging to write to a file
logging.basicConfig(
    filename="plot_log.txt",
    level=logging.INFO,  # Set log level to INFO
    format="%(asctime)s - %(message)s",
    filemode="w",  # Overwrite the log file each run
)

# Configuration
filename = "Cl"  # Choose "Cl" or "Cd"
figsize = (16, 9)
figtitle = "Comparison of Coefficients"



# Set yrange dynamically based on the chosen quantity
match filename:
    case "Cl":
        yrange = [0.25, 1.2]
    case "Cd":
        yrange = [-1, 1]

grid = True

# Specify manual overrides for specific filenames (base filenames without paths)
manual_overrides = {
    "omega304": {"style": "-", "color": "red", "alpha": 1},
    "omega100": {"style": "-", "color": "green", "alpha": 1},
    "omega50": {"style": "-", "color": "blue", "alpha": 1},
}

# Specify filenames to skip (base filenames without paths)
skip_files = {"omega15", "file4"}  # Filenames without ".dat" extension

# Robustness check: Remove any conflicts between pinned files and skipped files
conflicting_files = set(manual_overrides.keys()).intersection(skip_files)
if conflicting_files:
    logging.warning(
        "Conflicting files detected between manual overrides and skip list: %s. "
        "These files will be excluded from the skip list to prioritize manual overrides.",
        conflicting_files,
    )
    # Remove conflicting files from the skip list
    skip_files -= conflicting_files

# Glob pattern to find all .dat files in the directory
dat_files = glob.glob("./data/*.dat")
if not dat_files:
    print("No .dat files found in the current directory.")
    exit()

# Generate dynamic styles, colors, and transparency
num_files = len(dat_files)
default_styles = ["--", "-.", ":"]
default_colors = ["cornflowerblue", "lightsteelblue", "slategrey", "darkviolet", "orange"]
default_alphas = [0.5, 0.5, 0.5, 0.5, 0.5]

line_styles = []
line_colors = []
line_alphas = []
data_list = []
labels = []

# Assign styles, colors, and alphas
for i, dat_file in enumerate(dat_files):
    # Extract base filename without directory and extension
    # Used os.path.basename(dat_file) to get the filename from the path
    # Used os.path.splitext() to remove the .dat extension.
    file_base = os.path.splitext(os.path.basename(dat_file))[0]
    
    # Skip files that are in the skip list
    if file_base in skip_files:
        print(f"Skipping file: {dat_file}")
        logging.info(f"Skipping file: {dat_file}")
        continue

    # Load data from the current .dat file
    data = pd.read_csv(dat_file, sep=r'\s+')
    data_list.append(data)
    labels.append(file_base)  # Use the base filename as the label for the plot

    # Check for manual overrides
    if file_base in manual_overrides:
        override = manual_overrides[file_base]
        line_styles.append(override["style"])
        line_colors.append(override["color"])
        line_alphas.append(override["alpha"])
    else:
        # Use default cyclic styles, colors, and alphas
        line_styles.append(default_styles[i % len(default_styles)])
        line_colors.append(default_colors[i % len(default_colors)])
        line_alphas.append(default_alphas[i % len(default_alphas)])

# xrange = [0, 0.3]  # Set the x-axis range
# Dynamically set xrange based on the maximum "Time" value
if data_list:
    max_time = max(data["Time"].max() for data in data_list)
    xrange = [0, max_time]

# Log the dynamically calculated xrange
logging.info("Dynamically calculated xrange: %s", xrange)

# Log the generated variables into the log file
logging.info("Generated line styles: %s", line_styles)
logging.info("Generated line colors: %s", line_colors)
logging.info("Generated line alphas: %s", line_alphas)

# Call the plotting function to overlay all lines
plclcd_comp.plot_coefficients_comparison(
    data_list=data_list,
    labels=labels,
    filename=filename,
    figtitle=figtitle,
    figsize=figsize,
    xrange=xrange,
    yrange=yrange,
    line_styles=line_styles,
    line_colors=line_colors,
    line_alphas=line_alphas,
    grid=grid
)