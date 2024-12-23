import pandas as pd
import matplotlib.pyplot as plt
import re
import os

# Configure the font and enable Chinese character support
#plt.rcParams.update({
#    "font.family": "sans-serif",
#    "font.sans-serif": ["PingFang HK"],  # SimHei is a common Chinese font; adjust as needed
#    "axes.unicode_minus": False  # Ensure minus signs are rendered correctly
#})

# Enable LaTeX rendering for text
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern"],  # Use LaTeX's default font
})

# List of Excel file names
xlsx_files = ["./data/Beihang.xlsx", "./data/Changhang.xlsx", "./data/Lixuesuo.xlsx"]
line_styles = ['-o', '-s', '-^']  # Line styles for variety

# Plotting setup
plt.figure(figsize=(10, 6))
reference_data = None  # Will hold the reference dataset (e.g., "Beihang.xlsx")

for i, file in enumerate(xlsx_files, 1):
    try:
        # Try reading each Excel file
        print(f"Reading {file}...")
        data = pd.read_excel(file)

        # Clean up column names by removing any non-alphanumeric characters
        data.columns = [re.sub(r'\W+', '', col) for col in data.columns]
        
        # Print cleaned column names for verification
        print(f"Cleaned columns in {file}:", data.columns.tolist())
        
        # Check if the cleaned columns contain "AoA" and "Cl"
        if 'AoA' in data.columns and 'Cl' in data.columns:
            print(f"Plotting {file}")
            # Extract the filename without extension
            base_name = os.path.splitext(os.path.basename(file))[0]  # Get filename without extension
            #base_name = os.path.splitext(file)[0]
            
            # Store the reference data (e.g., "bei'hang.xlsx") when first encountered
            if reference_data is None:
                reference_data = data

            # Plot the data
            plt.plot(data['AoA'], data['Cl'], line_styles[i % len(line_styles)], label=base_name, fillstyle='none')
            
            # Calculate percentage difference from reference data (Beihang)
            if reference_data is not None and file != "./data/Beihang.xlsx":  # Skip the reference dataset itself (hard-coded!)
                # Ensure both datasets have the same AoA values
                common_AoA = data['AoA'].isin(reference_data['AoA'])  # Find common AoA values
                diff = data.loc[common_AoA, 'Cl'] - reference_data.loc[common_AoA, 'Cl']
                percentage_diff = (diff / reference_data.loc[common_AoA, 'Cl']) * 100
                
                # Add percentage difference texts on the plot
                #for j, percent in enumerate(percentage_diff):
                #    x_offset = 0.1  # Adjust text offset to avoid overlap
                #    y_offset = 0.05
                #    plt.text(data['AoA'].iloc[j] + x_offset, data['Cl'].iloc[j] + y_offset, 
                #             f"{percent:.1f}%", fontsize=10, color='blue')  # You can change the color as needed
                for j, percent in enumerate(percentage_diff):
                    x_offset = 0.1  # Adjust text offset to avoid overlap
                    y_offset = 0.05
                    if percent > 10:  # If the percentage difference is greater than 10%
                        color = 'red'
                    else:
                        color = 'green'
                    plt.text(data['AoA'].iloc[j] + x_offset, data['Cl'].iloc[j] + y_offset, 
                             f"{percent:.1f}%", fontsize=10, color=color)  # You can change the color as needed
                #for j, percent in enumerate(percentage_diff):
                #    plt.text(data['AoA'].iloc[j], data['Cl'].iloc[j], 
                #        f"{percent:.1f}%", fontsize=10, color=color)

        else:
            print(f"Columns 'AoA' and 'Cl' not found in {file}")

    except Exception as e:
        print(f"Error reading {file}: {e}")
        # You can print more information if needed
        # Example: print(f"Error details for {file}: {e}")
        
# Customize the plot
plt.xlabel("AoA")
plt.ylabel("$C_l$")
plt.title("Lift Coefficient ($C_l$) vs Angle of Attack (AoA)")
plt.xlim(0, 20)
plt.ylim(0, 1.5)
plt.legend()
plt.grid(True)

# Save the plot as a PDF with LaTeX formatting
#plt.savefig(r'Cl_comp', format='pdf')
plt.savefig(f"results/Cl_percentDiff.pdf", bbox_inches='tight', format='pdf')

# Show the plot
plt.show()