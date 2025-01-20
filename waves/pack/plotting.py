import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging

# Function to plot velocity data
def plot_velocity_data(data_list_u, labels_u, component_to_plot, custom_colors):
    component_label = f"Velocity_{component_to_plot.upper()}"

    for i, data in enumerate(data_list_u):
        plt.plot(
            data["Time"], data[component_label],
            label=f"OF Inlet gust: {labels_u[i]}",
            linewidth=1.5,
            color=custom_colors[i % len(custom_colors)],
            marker="o",
            markersize=1,
            markerfacecolor="none",
            markeredgewidth=1.5,
            markeredgecolor=custom_colors[i % len(custom_colors)],
            alpha=0.2
        )


# Function to plot CSV data
def plot_csv_data(data_list_csv, labels_csv, custom_colors):
    for i, data in enumerate(data_list_csv):
        plt.plot(
            data['Time'], data['Amplitude'],
            label=f"CSV Data: {labels_csv[i]}",
            linestyle=":",
            linewidth=1.5,
            marker="o",
            markersize=6,
            markerfacecolor="none",
            markeredgewidth=1.5,
            color=custom_colors[i % len(custom_colors)],
            markeredgecolor=custom_colors[i % len(custom_colors)]
        )


# Function to plot generated wave
def plot_generated_wave(t_norm, sin_wave, original_sin_wave):
    plt.plot(t_norm, sin_wave, label="Reconstructed ($A\\sin(\\omega t + 0.128559) - 0.25$)", linestyle="-", linewidth=2, color="red", alpha=0.5)
    plt.plot(t_norm, original_sin_wave, label="$A\\sin(\\omega t)$", linestyle="-", linewidth=2, color="k", alpha=0.5)


# Function to finalize the plot (title, labels, grid, etc.)
def finalize_plot(figtitle, component_to_plot, grid, positive_peak, negative_peak):
    plt.title(figtitle)
    plt.xlabel("$t/T$")
    plt.ylabel(f"$v/U$ for {component_to_plot.upper()}-direction")
    plt.grid(grid)
    plt.axhline(positive_peak, color="grey", linestyle="--", label="Positive Peak")
    plt.axhline(negative_peak, color="grey", linestyle="-.", label="Negative Peak")
    plt.legend()
    plt.show()



