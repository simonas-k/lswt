import math
import matplotlib.pyplot as plt

# pbar-p097 = pref

# Path to the data file
FILE_PATH = "raw_raw_2D_retest2.txt"
CHORDWISE_POSITIONS_FILE = "positions p.txt"  # New text file with x positions
WAKE_POS_FILE = "positions wake.txt"

Vinf = 19.515
Pinf = 906.11

def load_data(file_path):
    """Load the data from the text file and parse it into lists."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Skip the header (first two lines) and read data
    data_lines = lines[2:]
    data = []
    p097_values = []

    for line in data_lines:
        # Split the line by whitespace and convert to appropriate types
        parts = line.split()
        run_nr = int(parts[0])
        alpha = float(parts[2])         # Angle of attack  
        rho = float(parts[7])           # Air density
        pressures = [float(p) for p in parts[8:57]]
        p097 = float(parts[104+13])
        wake_pressures = [float(p) for p in parts[57:104]]
        data.append((run_nr, alpha, rho, pressures, p097, wake_pressures))

    return data

def load_chordwise_positions(file_path):
    """Load chordwise x positions from the text file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Convert each line to a float representing percentage of the chord
    positions = [float(line.strip()) for line in lines]
    
    return positions

def load_wake_positions(wake_path):
    with open(wake_path, 'r') as f:
        lines = f.readlines()

    # Convert each line to a float representing percentage of the chord
    positions = [float(line.strip()) for line in lines]

    return positions

def calculate_cp(data, selected_run_nr):

    """Calculate the pressure coefficient for a specific run number."""
    for run_nr, alpha, rho, pressures, p097, wake_pressures in data:
        if run_nr == selected_run_nr:
            # Calculate pressure coefficient C_p
            C_p = [(p - p097) / (0.5 * rho * (Vinf**2)) for p in pressures]
            C_pt_wake = [(p - p097) / (0.5 * rho * (Vinf**2)) for p in wake_pressures]
            return C_p, alpha, C_pt_wake

    # print(f"No data found for Run_nr {selected_run_nr}")
    return None, None

def plot_cp_profile(positions, C_p, alpha):
    """Plot the pressure coefficient profile with no diagonal line."""
    # Determine the midpoint to split upper and lower surfaces
    midpoint = len(positions) // 2

    # Split the positions and Cp data into upper and lower surfaces
    positions_upper = positions[:midpoint+1]
    C_p_upper = C_p[:midpoint+1]

    positions_lower = positions[midpoint+1:]
    C_p_lower = C_p[midpoint+1:]

    # Reverse lower surface data to plot leading to trailing edge
    positions_lower = positions_lower[::-1]
    C_p_lower = C_p_lower[::-1]

    # Create the plot
    # plt.figure(figsize=(10, 6))
    #
    # # Plot the upper surface (blue line)
    # plt.plot(positions_upper, C_p_upper, marker='o', linestyle='-', color='blue', label='Upper Surface')
    #
    # # Plot the lower surface (red line)
    # plt.plot(positions_lower, C_p_lower, marker='o', linestyle='-', color='red', label='Lower Surface')

    # # Ensure the y-axis is inverted for aerodynamic convention
    # plt.gca().invert_yaxis()
    #
    # # Add labels, title, grid, and legend
    # plt.xlabel('Chordwise Position (%)')
    # plt.ylabel('Pressure Coefficient (Cp)')
    # plt.title(f'Pressure Coefficient Profile for α = {alpha}°')
    # plt.grid(True)
    # plt.legend()
    # plt.show()

    return C_p_upper, positions_upper, C_p_lower, positions_lower

def plot_wake_profile(positions, C_pt_wake, alpha):
    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot
    plt.plot(positions, C_pt_wake, marker='o', linestyle='-', color='black')

    # Add labels, title, grid, and legend
    plt.xlabel('Chordwise Position (mm)')
    plt.ylabel('Pressure Coefficient (Cp)')
    plt.title(f'Pressure Coefficient Profile for α = {alpha}°')
    plt.grid(True)
    plt.show()

# def main():
#     # Load the data
#     data = load_data(FILE_PATH)
#
#     # Load the chordwise positions from the text file
#     chordwise_positions = load_chordwise_positions(CHORDWISE_POSITIONS_FILE)
#     wake_positions = load_wake_positions(WAKE_POS_FILE)
#
#     # Select run numbers to analyze (change these as needed for different α)
#     selected_run_nr = 30  # to change alpha
#
#     # Calculate Cp
#     C_p, alpha, C_pt_wake = calculate_cp(data, selected_run_nr)
#
#     if C_p is not None:
#         # Plot the Cp profile using chordwise positions
#         plot_cp_profile(chordwise_positions, C_p, alpha)
#
#     if C_p is not None:
#         plot_wake_profile(wake_positions, C_pt_wake, alpha)

# if __name__ == "__main__":
#     main()
