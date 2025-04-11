import matplotlib.pyplot as plt

def plot_results(results, motor_burn_time=None):
    time = results['time']
    alt = results['y']

    impact_time = time[-1]
    burnout_time = motor_burn_time if motor_burn_time is not None else 0

    def draw_event_lines(ax):
        if burnout_time:
            ax.axvline(x=burnout_time, color='orange', linestyle='--', label='Burnout')
        ax.axvline(x=impact_time, color='red', linestyle='--', label='Impact')
        ax.legend()

    plt.figure(figsize=(14, 10))

    for i, (title, ylabel, data) in enumerate([
        ('Altitude vs Time', 'Altitude (m)', alt),
        ('Vertical Velocity vs Time', 'Vertical Velocity (m/s)', results['vertical_velocity']),
        ('Drag vs Time', 'Drag (N)', results['drag']),
        ('Mass vs Time', 'Mass (kg)', results['mass']),
        ('Dynamic Pressure vs Time', 'Dynamic Pressure (Pa)', results['dynamic_pressure']),
        ('Mach Number vs Time', 'Mach Number', results['mach']),
        ('Vertical Acceleration vs Time', 'Vertical Acceleration (m/s²)', results['acceleration'])
    ]):
        plt.subplot(3, 3, i + 1)
        plt.plot(time, data)
        plt.xlabel('Time (s)')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        draw_event_lines(plt.gca())

    plt.subplot(3, 3, 8)
    plt.plot(time, results['ke'], label='Kinetic Energy')
    plt.plot(time, results['pe'], label='Potential Energy')
    plt.plot(time, results['total_energy'], label='Total Energy')
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.title('Energy vs Time')
    plt.legend()
    plt.grid(True)
    draw_event_lines(plt.gca())

    plt.subplot(3, 3, 9)
    plt.plot(time, results['stag_temp'])
    plt.xlabel('Time (s)')
    plt.ylabel('Stag Temp (K)')
    plt.title('Stagnation Temperature vs Time')
    plt.grid(True)
    draw_event_lines(plt.gca())

    plt.tight_layout()
    plt.show()