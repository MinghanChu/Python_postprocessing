import os
import glob
import pandas as pd

def load_u_files(data_U_folder, freestream_velocity, time_normalization):
    u_files = glob.glob(os.path.join(data_U_folder, "U*"))
    if not u_files:
        raise FileNotFoundError(f"No U files found in {data_U_folder}")

    data_list_u = []
    labels_u = []

    for u_file in u_files:
        file_base = os.path.splitext(os.path.basename(u_file))[0]
        time, velocity_x, velocity_y, velocity_z = [], [], [], []

        with open(u_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("Time"):
                    parts = line.split(maxsplit=1)
                    try:
                        time_val = float(parts[0]) / time_normalization  # Normalize time
                        velocity_tuple = parts[1].strip("()\n").split()
                        velocity_x.append(float(velocity_tuple[0]) / freestream_velocity)
                        velocity_y.append(float(velocity_tuple[1]) / freestream_velocity)
                        velocity_z.append(float(velocity_tuple[2]) / freestream_velocity)
                        time.append(time_val)
                    except (ValueError, IndexError):
                        continue

        data = pd.DataFrame({
            'Time': time,
            'Velocity_X': velocity_x,
            'Velocity_Y': velocity_y,
            'Velocity_Z': velocity_z,
        })
        data_list_u.append(data)
        labels_u.append(file_base)

    return data_list_u, labels_u


def load_csv_files(data_csv_folder):
    csv_files = [f for f in os.listdir(data_csv_folder) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_csv_folder}")

    data_list_csv = []
    labels_csv = []
    sinwave_exp_2_5c = None
    sinwave_exp_0_5c = None

    for csv_file in csv_files:
        file_path = os.path.join(data_csv_folder, csv_file)
        data = pd.read_csv(file_path)
        if 'Time' in data.columns and 'Amplitude' in data.columns:
            data_list_csv.append(data)
            labels_csv.append(os.path.splitext(csv_file)[0])

            # Identify specific files for filling
            if 'sinwave_exp_2.5c' in csv_file:
                sinwave_exp_2_5c = (data['Time'].values, data['Amplitude'].values)
            elif 'sinwave_exp_0.5c' in csv_file:
                sinwave_exp_0_5c = (data['Time'].values, data['Amplitude'].values)

    return data_list_csv, labels_csv, sinwave_exp_2_5c, sinwave_exp_0_5c