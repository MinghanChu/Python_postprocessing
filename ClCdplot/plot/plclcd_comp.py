import matplotlib.pyplot as plt

def plot_coefficients_comparison(
    data_list,
    labels,
    filename,
    figtitle,
    figsize,
    xrange,
    yrange,
    line_styles,
    line_colors,
    line_alphas,
    grid,
    exp_marker=None,  # New parameter to accept marker settings for experimental data
    plot_lines=True,  # Flag to control line plotting
    plot_markers=True  # Flag to control marker plotting
):
    """
    Plot a comparison of coefficients (Cl or Cd) from multiple datasets with customizable line styles, colors, and transparency.

    Parameters:
        data_list (list): A list of Pandas DataFrames containing the data.
        labels (list): A list of strings to use as labels for each dataset.
        filename (str): The column name to plot (e.g., "Cl" or "Cd").
        figtitle (str): Title of the figure.
        figsize (tuple): Figure size (width, height).
        xrange (list): X-axis range [min, max].
        yrange (list): Y-axis range [min, max].
        line_styles (list): List of line styles for each dataset (e.g., ['-', '--', '-.']).
        line_colors (list): List of line colors for each dataset (e.g., ['blue', 'green', 'red']).
        line_alphas (list): List of transparency values (0.0 to 1.0) for each dataset.
        grid (bool): Whether to show the grid.
        exp_marker (dict, optional): Dictionary with marker customization for experimental data.
        plot_lines (bool): Whether to plot lines for experimental data (default True).
        plot_markers (bool): Whether to plot markers for experimental data (default True).
    """
    # Convert filename to LaTeX format for axis label
    latex_labels = {"Cl": r"$C_l$", "Cd": r"$C_d$"}
    
    # If filename matches "Cl" or "Cd", the y-axis label is set in LaTeX format. Otherwise, it defaults to the original filename.
    y_label = latex_labels.get(filename, filename)  # Default to filename if not Cl or Cd

    # Create the plot
    plt.figure(figsize=figsize)
    plt.title(figtitle, fontsize=16)

    # Plot each dataset with specific style, color, and transparency
    for data, label, style, color, alpha in zip(data_list, labels, line_styles, line_colors, line_alphas):
        if label == "Experimental Data" and exp_marker is not None:
            # Plot experimental data with customizable markers and lines (if desired)
            if plot_lines:
                # Plot line if plot_lines is True
                plt.plot(
                    data["Time"],
                    data[filename],
                    label=label,
                    linestyle=style,  # Solid line
                    color=color,
                    alpha=alpha,  # Set transparency
                    linewidth=2
                )
            
            if plot_markers:
                # Plot markers if plot_markers is True
                plt.plot(
                    data["Time"],
                    data[filename],
                    label=label,
                    linestyle="None",  # No line, just markers
                    color=exp_marker.get("markeredgecolor", color),
                    alpha=alpha,
                    marker=exp_marker["marker"],  # Use the specified marker
                    markerfacecolor=exp_marker["markerfacecolor"],
                    markeredgecolor=exp_marker["markeredgecolor"],
                    markeredgewidth=exp_marker["markeredgewidth"],
                    markersize=exp_marker.get("markersize", 6),  # Default size of marker
                    linewidth=0,  # No line for experimental data
                )
        else:
            # For other datasets, use the specified line styles and colors
            plt.plot(
                data["Time"],
                data[filename],
                label=label,
                linestyle=style,
                color=color,
                alpha=alpha,  # Set transparency
                linewidth=2
            )

    # Set plot limits
    if xrange:
        plt.xlim(xrange)
    if yrange:
        plt.ylim(yrange)

    # Set plot grid
    if grid:
        plt.grid(color='gray', linestyle='--', linewidth=0.5)

    # Label axes
    plt.xlabel("Time", fontsize=14)
    plt.ylabel(y_label, fontsize=14)  # Use LaTeX format for the y-axis label

    # Add legend
    plt.legend(loc="best", fontsize=12)

    # Save the plot with the provided filename
    plt.savefig(f"./results/{filename}.pdf", bbox_inches='tight', format='pdf')

    # Show the plot
    plt.tight_layout()
    plt.show()