import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid

# Path to the data file
FILE_PATH = "raw_raw_2D_retest2.txt"
POSITIONS_FILE = "wake rake locations.txt"  # New text file with x positions

Vinf = 19.515  # Freestream velocity (m/s)
x_data = np.linspace(0, 1, 100)

pt_positions = np.array([0, 12, 21, 27, 33, 39, 45, 51, 57, 63, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99,
                         102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147,
                         150, 156, 162, 168, 174, 180, 186, 195, 207, 219])
ps_positions = np.array([43.5, 55.5, 67.5, 79.5, 91.5, 103.5, 115.5, 127.5, 139.5, 151.5, 163.5, 175.5])


def load_data(file_path):
    """Load the data from the text file and parse it into lists."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Skip the header (first two lines) and read data
    data_lines = lines[2:]
    data = []

    for line in data_lines:
        # Split the line by whitespace and convert to appropriate types
        parts = line.split()
        run_nr = int(parts[0])
        alpha = float(parts[2])
        rho = float(parts[7])
        Pinf = float(parts[97])
        pressures = [float(p) for p in parts[57:104]]
        static_pressures = [float(p) for p in parts[105:117]]
        data.append((run_nr, alpha, rho, Pinf, pressures, static_pressures))
    return data

def load_positions(file_path):
    """Load wake positions from the text file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Convert each line to a float representing percentage of the chord
    positions = [float(line.strip()) for line in lines]
    
    return positions

def calculate_velocity(data, selected_run_nr):
    """Calculate the wake velocity profile for a specific run number."""
    for run_nr, alpha, rho, Pinf, pressures, static_pressures in data:
        if run_nr == selected_run_nr:
            print(static_pressures)
            # print(pressures)
            # print(len(pressures))
            # print(len(static_pressures))
            # print(len(pt_positions))
            # print(len(ps_positions))
            # Calculate velocity using Bernoulli's equation with a check for non-negative values
            velocities = []
            for p in pressures:
                delta_p = Pinf - p
                if Vinf**2 + (2 * delta_p) / rho >= 0:
                    velocities.append(math.sqrt(Vinf**2 + (2 * delta_p) / rho))
                else:
                    velocities.append(0)  # Set velocity to 0 if expression inside sqrt is negative

            return velocities, alpha, static_pressures

    print(f"No data found for Run_nr {selected_run_nr}")
    return None, None, None

def plot_velocity_profile(positions, velocities, alpha):
    """Plot the velocity distribution as a single line over the wake profile."""
    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot the velocities over the chordwise positions as a single line
    plt.plot(positions, velocities, marker='o', linestyle='-', color='blue', label='Velocity Distribution')

    # Add labels, title, grid, and legend
    plt.xlabel('Total wake rake probe locations (mm)')
    plt.ylabel('Velocity (m/s)')
    plt.title(f'Velocity Distribution for α = {alpha}°')
    plt.grid(True)
    plt.legend()

    # Display the plot
    plt.show()

def main():
    alpha_values = []
    cd_values = []
    aoa_values = np.arange(3, 52, 1)
    # Load the data
    data = load_data(FILE_PATH)

    # Load the chordwise positions
    positions = load_positions(POSITIONS_FILE)

    # Select the run number (change this to analyze different angles)
    selected_run_nr = 5  # Example run number

    # Calculate velocity profile
    for aoa in aoa_values:
        velocities, alpha, static = calculate_velocity(data, aoa)

        velocities = np.array(velocities)
        velocities = np.interp(x_data*219, positions, velocities)
        drag = (Vinf - velocities) * velocities
        D = cumulative_trapezoid(drag, x_data, initial=0)
        static_interpolate = np.interp(x_data*220, ps_positions, static)
        print(static_interpolate)
        drag_2 = cumulative_trapezoid(-static_interpolate, x_data, initial=0)
        Drag = -(D[-1]+drag_2[-1])/(1/2*1.2047*Vinf**2)

        alpha_values.append(alpha)
        cd_values.append(Drag)

        # if velocities is not None:
        #     # Plot the velocity profile
        #     plot_velocity_profile(alpha_values, cd_values, alpha)
    print(alpha_values)
    print(cd_values)

    plt.figure(figsize=(10, 6))
    plt.plot(alpha_values, cd_values, marker='o', linestyle='-', color='blue', label='Drag Coefficient vs. AoA')
    plt.xlabel('Angle of Attack ($\\alpha$, in °)')
    plt.ylabel('Drag Coefficient ($C_d$)')
    plt.title('Drag Coefficient vs. Angle of Attack')
    plt.grid(True)
    plt.savefig("wake_rake.pdf")
    # plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

