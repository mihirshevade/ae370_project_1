import numpy as np
from atmosphere import atmosphere_properties
from dynamics import dynamics, rk4_step

g = 9.80665

def run_simulation(motor, rocket_params, sim_params, dt=0.01):

    initial_mass = rocket_params['dry_mass'] + rocket_params['propellant_mass']
    state = np.array([0.0, 0.0, rocket_params['v0_x'], rocket_params['v0_y'], initial_mass])

    results = {
        'time': [], 'x': [], 'y': [], 'vx': [], 'vy': [], 'mass': [],
        'drag': [], 'dynamic_pressure': [], 'mach': [], 'vertical_velocity': [],
        'acceleration': [], 'temperature': [], 'speed_of_sound': [],
        'ke': [], 'pe': [], 'total_energy': [], 'stag_temp': []
    }

    t = 0
    while True:
        x, y, vx, vy, m = state

        results['time'].append(t)
        results['x'].append(x)
        results['y'].append(max(y, 0))
        results['vx'].append(vx)
        results['vy'].append(vy)
        results['mass'].append(m)
        results['vertical_velocity'].append(vy)

        dens, temp, a_sound = atmosphere_properties(max(y, 0))
        results['temperature'].append(temp)
        results['speed_of_sound'].append(a_sound)

        v_rel = np.array([vx - sim_params['wind'], vy])
        v_rel_mag = np.linalg.norm(v_rel)

        A = np.pi * (rocket_params['diameter'] / 2)**2
        drag = 0.5 * dens * rocket_params['Cd'] * A * v_rel_mag**2
        results['drag'].append(drag)

        q = 0.5 * dens * v_rel_mag**2
        results['dynamic_pressure'].append(q)

        mach = v_rel_mag / a_sound if a_sound > 0 else 0
        results['mach'].append(mach)

        ke = 0.5 * m * (vx**2 + vy**2)
        pe = m * g * y
        results['ke'].append(ke)
        results['pe'].append(pe)
        results['total_energy'].append(ke + pe)

        stag_temp = temp * (1 + 0.2 * mach**2)
        results['stag_temp'].append(stag_temp)

        deriv = dynamics(t, state, motor, rocket_params, sim_params)
        acc = deriv[3]
        results['acceleration'].append(acc)

        if y <= 0 and vy <= 0 and t > 0.25:
            break

        state = rk4_step(dynamics, t, state, dt, motor, rocket_params, sim_params)
        t += dt

        # debugging motor selection issues
        # if t < 0.1:  # just for the first few steps
        #     print(f"[t={t:.3f}] y={y:.3f}, vy={vy:.3f}, thrust={motor['thrust_func'](t):.2f}")

    for key in results:
        results[key] = np.array(results[key])

    print("\n--- Flight Statistics ---")
    apogee = np.max(results['y'])
    time_to_apogee = results['time'][np.argmax(results['y'])]
    max_q = np.max(results['dynamic_pressure'])
    max_speed = np.max(np.sqrt(results['vx']**2 + results['vy']**2))
    max_mach = np.max(results['mach'])
    max_accel = np.max(results['acceleration'])
    max_stag_temp = np.max(results['stag_temp'])

    print(f"Apogee: {apogee:.2f} m")
    print(f"Time to Apogee: {time_to_apogee:.2f} s")
    print(f"Impact Time: {results['time'][-1]:.2f} s")
    print(f"Max Acceleration: {max_accel:.2f} m/s²")
    print(f"Max Q (dynamic pressure): {max_q:.2f} Pa")
    print(f"Max Speed: {max_speed:.2f} m/s")
    print(f"Max Mach Number: {max_mach:.2f}")
    print(f"Max Stage Temperature: {max_stag_temp:.2f} K")

    return results