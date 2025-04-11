import numpy as np
from atmosphere import atmosphere_properties

g = 9.80665

def dynamics(t, state, motor, rocket_params, sim_params):
    x, y, vx, vy, m = state

    if t <= motor['burn_time']:
        T = motor['thrust_func'](t)
        dm_dt = -rocket_params['propellant_mass'] / motor['burn_time']
    else:
        T = 0
        dm_dt = 0

    theta_rad = np.deg2rad(rocket_params['launch_angle'])
    T_x = T * np.sin(theta_rad)
    T_y = T * np.cos(theta_rad)

    v_wx = sim_params['wind']
    v_rel = np.array([vx - v_wx, vy])
    v_rel_mag = np.linalg.norm(v_rel)

    if v_rel_mag == 0:
        D = np.array([0.0, 0.0])
    else:
        dens, temp, a_sound = atmosphere_properties(max(y, 0))
        A = np.pi * (rocket_params['diameter'] / 2)**2
        Cd = rocket_params['Cd']
        D = -0.5 * dens * Cd * A * v_rel_mag * v_rel

    ax = (T_x + D[0]) / m
    ay = (T_y + D[1]) / m - g

    return np.array([vx, vy, ax, ay, dm_dt])


def rk4_step(f, t, y, dt, *args):
    k1 = f(t, y, *args)
    k2 = f(t + dt/2, y + dt*k1/2, *args)
    k3 = f(t + dt/2, y + dt*k2/2, *args)
    k4 = f(t + dt, y + dt*k3, *args)
    return y + dt*(k1 + 2*k2 + 2*k3 + k4)/6