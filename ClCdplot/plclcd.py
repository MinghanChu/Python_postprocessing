def plot_coefficients(data, filename, figtitle, figsize, xrange, yrange, linecolor, grid, indicator_lines=None, 
                      ytick_remove=-0.01, text_yoffset=0.1, text_xoffset = 0.1, show_indicators=True):
    """
    Function to plot Cl or Cd based on user input.
    Args:
        filename (str): The filename to save the plot as.
        figsize (tuple): The figure size for the plot.
        xrange (tuple): The x range for the plot.
        yrange (tuple): The y range for the plot.
        figtitle (str): The title for the plot.
        linecolor (str): The color of the line for the plot.
        grid (bool): A flag to enable or disable the grid on the plot.
        indicator_lines (list of tuples): List of (CFL, Time) pairs for vertical lines.
        ytick_remove(float): In case x and y ticks overlap at the corner of the graph.
        text_offset (float): The vertical offset for indicator labels relative to yrange[1].
        show_indicators (bool): A flag to enable or disable drawing the indicators.
    """
    import matplotlib.pyplot as plt

    # User input for the case
    input_string = input("Enter your case (Cd or Cl): ")

    # Create the plot with the specified figure size
    plt.figure(figsize=figsize)

    # Match-case to handle user input
    match input_string:
        case "Cd":
            print("*** You are plotting Cd. ***")
            plt.plot(data["Time"], data["Cd"], label=r'$C_d$', color=linecolor, linewidth=2)
            caption = "Drag coefficient"
        case "Cl":
            print("*** You are plotting Cl. ***")
            plt.plot(data["Time"], data["Cl"], label=r'$C_l$', color=linecolor, linewidth=2)
            caption = "Lift coefficient"
        case _:
            print("Unknown case. Please enter a valid case.")
            return  # Exit the function if the input is invalid

    # Set labels, title, and limits with LaTeX formatting
    plt.xlabel(r'Time (Seconds)', fontsize=22)
    plt.ylabel(caption, fontsize=22)
    plt.title(figtitle, fontsize=24)
    plt.xlim(xrange)  # Dynamic x-axis limits
    plt.ylim(yrange)

    # Add legend
    plt.legend(loc='upper right', fontsize=14)

    # Customize ticks
    ax = plt.gca()
    ax.tick_params(axis='both', labelsize=16, direction='in', length=6, width=2)
    # Remove 0.0 from y-axis ticks
    ticks = [tick for tick in ax.get_yticks() if tick != ytick_remove]
    ax.set_yticks(ticks)
    
    # Set grid based on user input
    if grid:
        plt.grid(grid, color='grey', linestyle=':')
    else:
        plt.grid(grid)

    # Draw vertical lines and add indicator labels if enabled
    if show_indicators and indicator_lines is not None:
        for cfl, x_coord in indicator_lines:
            # Draw vertical line
            plt.axvline(x=x_coord, color='red', linestyle='--', linewidth=1.2)

            # Add text beside the line
            plt.text(
                x_coord + text_xoffset, yrange[1] - text_yoffset, f"CFL={cfl}",
                rotation=90, color='red', fontsize=10, ha='left' #left, right, center
            )


    # Save the plot with the provided filename
    plt.savefig(f"{filename}.pdf", bbox_inches='tight', format='pdf')

    # Show the plot
    plt.show()