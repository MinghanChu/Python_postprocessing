import matplotlib.pyplot as plt

# Configuration
figsize = (16, 9)
grid = True

# Directory paths
data_U_folder = "./data_U"
data_csv_folder = "./data"

# Freestream velocity and normalization factors
freestream_velocity = 20  # Normalization factor for velocity
time_normalization = 0.5  # Period for time normalization

# Matplotlib settings
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],
})