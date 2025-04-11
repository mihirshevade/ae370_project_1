import ipywidgets as widgets
from IPython.display import display
from ipywidgets import HBox, VBox
import numpy as np
from dynamics import rk4_step, dynamics
from simulation import run_simulation
from plotter import plot_results
from thrust import motors


def run_interface():
    motor_dropdown = widgets.Dropdown(
        options=list(motors.keys()),
        value=list(motors.keys())[0] if motors else None,
        description='Motor:'
    )
    rail_length_text = widgets.FloatText(value=1.5, description='Rail Length (m):')
    wind_text = widgets.FloatText(value=0.0, description='Wind (m/s):')
    diameter_text = widgets.FloatText(value=98, description='Diameter (mm):')
    Cd_text = widgets.FloatText(value=0.75, description='Cd:')
    dry_mass_text = widgets.FloatText(value=10.0, description='Dry Mass (kg):')
    propellant_mass_text = widgets.FloatText(value=5.0, description='Propellant Mass (kg):')
    run_button = widgets.Button(description='Run Simulation')
    out = widgets.Output()

    def on_run_button_clicked(b):
        with out:
            out.clear_output()
            selected_motor = motors[motor_dropdown.value]
            selected_motor = motors.get(motor_dropdown.value)

            rocket_params = {
                'diameter': diameter_text.value / 1000,
                'Cd': Cd_text.value,
                'dry_mass': dry_mass_text.value,
                'propellant_mass': propellant_mass_text.value
            }
            sim_params = {'wind': wind_text.value}

            print(f"Running simulation with {motor_dropdown.value}...")

            # Pre-rail simulation
            state = np.array([0.0, 0.0, 0.0, 0.0, rocket_params['dry_mass'] + rocket_params['propellant_mass']])
            t = 0
            rocket_params['launch_angle'] = 0
            rocket_params['v0_x'] = 0
            rocket_params['v0_y'] = 0

            results = run_simulation(selected_motor, rocket_params, sim_params, dt=0.01)
            plot_results(results, motor_burn_time=selected_motor['burn_time'])

    run_button.on_click(on_run_button_clicked)

    ui = VBox([
        HBox([motor_dropdown, rail_length_text, wind_text]),
        HBox([diameter_text, Cd_text, dry_mass_text, propellant_mass_text]),
        run_button,
        out
    ])

    display(ui)