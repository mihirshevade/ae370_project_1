# AE 370 Rocket Trajectory Simulator

This project is a 2DOF physics-based rocket simulator built in Python, developed for the AE 370 course. It models the vertical flight of a rocket using time-dependent thrust curves, atmospheric effects, and aerodynamic drag, with numerical integration performed via the 4th-order Runge-Kutta (RK4) method.

## Features

- Interactive launch interface with `ipywidgets`
- Real motor thrust curve support via CSV import
- RK4-based trajectory integration with mass depletion and drag
- Output includes velocity, altitude, dynamic pressure, Mach number, energy, and more
- Built-in plotting for all key flight parameters
- Convergence and stability analysis tools to validate numerical accuracy

## How It Works

1. The user selects a motor and inputs rocket parameters through a Jupyter interface.
2. Thrust data is interpolated from `.csv` files in the `motors/` folder.
3. The simulation calculates forces and updates rocket state via RK4.
4. Plots are generated to visualize time evolution of physical quantities.

## File Overview

| File              | Purpose |
|-------------------|---------|
| `main.ipynb`      | Launches the simulation UI (Jupyter notebook) |
| `interface.py`    | Interactive config interface using `ipywidgets` |
| `simulation.py`   | Core RK4 simulation logic |
| `dynamics.py`     | Defines equations of motion and RK4 step |
| `plotter.py`      | Flight data visualization |
| `thrust.py`       | Loads and interpolates motor thrust data |
| `motors/`         | CSV files containing thrust curves |
| `convergence_study.py` | RK4 error analysis across dt values |
| `stability_plot.py`    | Optional: Empirical stability region plot |

## 📊 Requirements

- Python 3.8+
- `numpy`
- `matplotlib`
- `scipy`
- `pandas`
- `ipywidgets`
- `pyatmos`
