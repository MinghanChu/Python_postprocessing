import pyvista as pv
import imageio
import numpy as np
import glob
import os

# Choose which field to plot: "U" or "p"
plot_field = "U"

base_path = "/Users/minghan/Downloads/pitch_heave/heaving/postProcessing/midPlaneXZ"
vtk_files = sorted(
    glob.glob(os.path.join(base_path, "*/midPlaneXZ.vtp")),
    key=lambda x: float(os.path.basename(os.path.dirname(x)))
)

print(f"Found {len(vtk_files)} VTK files.")

plotter = pv.Plotter(off_screen=True, window_size=(1920, 1080))  # HD
frames = []

# Optional: consistent scalar range across frames
scalar_range = None  # e.g., (0, 20) if you want to lock it

for i, file in enumerate(vtk_files):
    print(f"[{i+1}/{len(vtk_files)}] Processing: {file}")
    mesh = pv.read(file)

    # Compute U magnitude if not already in the file
    if plot_field == "U" and "U" in mesh.array_names:
        if "U_Magnitude" not in mesh.array_names:
            mesh["U_Magnitude"] = np.linalg.norm(mesh["U"], axis=1)
        scalar_field = "U_Magnitude"
    elif plot_field == "p" and "p" in mesh.array_names:
        scalar_field = "p"
    else:
        print(f"No usable field '{plot_field}' found in:", file)
        continue

    plotter.clear()

    plotter.add_mesh(
        mesh,
        scalars=scalar_field,
        cmap="jet",
        show_scalar_bar=True,
        show_edges=True,
        edge_color='black',
        opacity=0.85,
        scalar_bar_args={
            "title": f"{plot_field}",
            "title_font_size": 30,
            "label_font_size": 24,
            "n_labels": 4,               # Number of ticks
            "vertical": True,            # Orientation
            "position_x": 0.2,          # X position
            "position_y": 0.25,          # Y position
            "width": 0.04,               # Colorbar width
            "height": 0.5,               # Colorbar height
            "color": "white",            # Colorbar color
        },
    )

    # Camera position
    plotter.set_focus((0, 0, 0))
    plotter.camera_position = [(0, -2, 0), (0, 0, 0), (0, 0, 1)]
    plotter.reset_camera_clipping_range()

    img = plotter.screenshot(return_img=True)
    frames.append(img)

if frames:
    imageio.mimsave("velocity_animation.gif", frames, fps=10)
    print("Animation saved as velocity_animation.gif")
else:
    print(" No frames collected. Check VTK contents.")