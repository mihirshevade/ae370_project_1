import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import glob

motors = {}

motor_files = glob.glob("motors/*.csv")
for file in motor_files:
    try:
        name = file.split("/")[-1].replace(".csv", "").strip()

        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]

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