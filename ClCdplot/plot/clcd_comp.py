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
        yrange = [0.4, 1.2]
    case "Cd":
        yrange = [-1, 1]

grid = True

# Specify manual overrides for specific filenames (base filenames without paths)
manual_overrides = {
    "": {"style": "-", "color": "red", "alpha": 0.1},
    "omega404_CFL400": {"style": "-", "color": "green", "alpha": 1},
    "comega304": {"style": "-", "color": "green", "alpha": 1},
    "omega404_continue": {"style": "-", "color": "red", "alpha": 0.1},
    "coefficient": {"style": "-", "color": "red", "alpha": 1},
}

# Specify filenames to skip (base filenames without paths)
skip_files = {"omega15_gust_time(0.15)", "omega2_gust_time(0.3)_CFL400", "omega15", "omega100", "omega50"}
conflicting_files = set(manual_overrides.keys()).intersection(skip_files)
if conflicting_files:
    logging.warning(
        "Conflicting files detected between manual overrides and skip list: %s. "
        "These files will be excluded from the skip list to prioritize manual overrides.",
        conflicting_files,
    )
    skip_files -= conflicting_files

# Load .dat files from ./data/
dat_files = glob.glob("./data/*.dat")
if not dat_files:
    print("No .dat files found in ./data/ directory.")
    exit()

# Load experimental data from exp_data/ directory
exp_data_file = "./exp_data/exp_data.csv"
try:
    exp_data = pd.read_csv(exp_data_file)
    # Rename columns if necessary
    if set(exp_data.columns) != {"Time", "Cl"}:
        exp_data.rename(columns={exp_data.columns[0]: "Time", exp_data.columns[1]: "Cl"}, inplace=True)
    print("Experimental data loaded successfully.")
    logging.info(f"Experimental data loaded from {exp_data_file}")

    # Apply a horizontal shift to the "Time" column
    T_gust = 0.5
    time_shift = 0.12  # Modify this value as needed
    exp_data["Time"] = exp_data["Time"] * T_gust + time_shift
    logging.info(f"Experimental data 'Time' column shifted by {time_shift}")
except FileNotFoundError:
    print(f"Error: Experimental data file '{exp_data_file}' not found.")
    logging.error(f"FileNotFoundError: Experimental data file '{exp_data_file}' not found.")
    exp_data = None  # Set to None if the file is not found
except Exception as e:
    print(f"Error loading experimental data: {e}")
    logging.error(f"Error loading experimental data: {e}")
    exp_data = None

# Process .dat files
num_files = len(dat_files)
default_styles = ["--", "-.", ":"]
default_colors = ["red", "cornflowerblue", "lightsteelblue", "slategrey", "darkviolet", "orange", "magenta"]
default_alphas = [0.5, 0.5, 0.5, 0.5, 0.5]

line_styles = []
line_colors = []
line_alphas = []
data_list = []
labels = []

for i, dat_file in enumerate(dat_files):
    file_base = os.path.splitext(os.path.basename(dat_file))[0]
    if file_base in skip_files:
        print(f"Skipping file: {dat_file}")
        logging.info(f"Skipping file: {dat_file}")
        continue

    data = pd.read_csv(dat_file, sep=r'\s+')
    data_list.append(data)
    labels.append(file_base)

    if file_base in manual_overrides:
        override = manual_overrides[file_base]
        line_styles.append(override["style"])
        line_colors.append(override["color"])
        line_alphas.append(override["alpha"])
    else:
        line_styles.append(default_styles[i % len(default_styles)])
        line_colors.append(default_colors[i % len(default_colors)])
        line_alphas.append(default_alphas[i % len(default_alphas)])

# Determine xrange based on data
if data_list:
    max_time = max(data["Time"].max() for data in data_list)
    xrange = [0, max_time]
else:
    xrange = [0, 0.3]  # Default range if no data is loaded

logging.info("Dynamically calculated xrange: %s", xrange)

# Include experimental data in plotting if available
# Include experimental data in plotting if available
# Configuration flags for plotting
plot_lines = True   # Set to True to plot lines
plot_markers = True  # Set to True to plot markers

if exp_data is not None:
    data_list.append(exp_data)
    labels.append("Experimental Data")
    line_styles.append(":")  # Default line style (solid line)
    line_colors.append("black")  # Line color
    line_alphas.append(1.0)  # Line transparency

    # Marker settings for experimental data
    exp_marker = {
        "marker": "^",  # Circle marker
        "markerfacecolor": "none",  # Open marker (no fill)
        "markeredgecolor": "blue",  # Marker edge color
        "markeredgewidth": 1.5,  # Marker edge thickness
    }
# Call the plotting function
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
    grid=grid,
    exp_marker=exp_marker,
    plot_lines=plot_lines,
    plot_markers=plot_markers,
)