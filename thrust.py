import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import glob

motors = {}

motor_files = glob.glob("motors/*.csv")
for file in motor_files:
    try:
        # Normalize motor name (remove .csv and any path info/extra spaces)
        name = file.split("/")[-1].replace(".csv", "").strip()

        # Read and clean column headers
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]  # clean header names

        # Assume the first two columns are time and thrust
        time_col = df.columns[0]
        thrust_col = df.columns[1]

        t = df[time_col].values
        thrust = df[thrust_col].values

        interp = interp1d(t, thrust, fill_value=0, bounds_error=False)

        motors[name] = {
            'thrust_time': t,
            'thrust_values': thrust,
            'thrust_func': interp,
            'burn_time': t[-1],
            'Isp': 250
        }

        # Uncomment to check if motors are loaded correctly
        # print(f"[thrust.py] Loaded motor: {name} from {file}")

    except Exception as e:
        print(f"[thrust.py] Error loading {file}: {e}")