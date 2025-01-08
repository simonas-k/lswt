import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
rho = 1.21  # [kg/m^3]
u_inf = 19.5  # [m/s]
p_inf = 101570  # [Pa]

# Load data
file_path = "raw_raw_2D_retest2.txt"  # Update with the correct file path
data = pd.read_csv(file_path, sep=r'\s+')  # Use raw string for valid escape sequence

# Convert relevant columns to numeric
pt_columns = [f'P{50+i:03}' for i in range(48)]  # P050 to P097
ps_columns = [f'P{98+i:03}' for i in range(12)]  # P098 to P109

# Ensure numeric data
data[pt_columns] = data[pt_columns].apply(pd.to_numeric, errors='coerce')
data[ps_columns] = data[ps_columns].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values if necessary
data.dropna(subset=pt_columns + ps_columns, inplace=True)

# Define positions in mm for pt and ps
pt_positions = np.array([0, 12, 21, 27, 33, 39, 45, 51, 57, 63, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99,
                         102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147,
                         150, 156, 162, 168, 174, 180, 186, 195, 207, 219])
ps_positions = np.array([43.5, 55.5, 67.5, 79.5, 91.5, 103.5, 115.5, 127.5, 139.5, 151.5, 163.5, 175.5])

pt_positions = pt_positions / 1000  # Convert to meters
ps_positions = ps_positions / 1000  # Convert to meters


# Ensure pt_positions matches the number of pt_values columns
if len(pt_positions) != len(pt_columns):
    pt_positions = np.linspace(pt_positions[0], pt_positions[-1], len(pt_columns))  # Interpolate positions

# Extract pt and ps values
pt_values = data[pt_columns].to_numpy()
ps_values = data[ps_columns].to_numpy()

# Interpolate static pressure (ps) to match total pressure (pt) positions
interpolated_ps = np.interp(pt_positions, ps_positions, ps_values.mean(axis=0))  # Mean ps values across runs

# Calculate velocity using Bernoulli's equation
velocity = np.sqrt(2 * (pt_values.mean(axis=0) - interpolated_ps) / rho)

# Calculate drag components
momentum_drag = rho * np.trapz((u_inf - velocity) * velocity, x=pt_positions)
pressure_drag = np.trapz(p_inf - interpolated_ps, x=pt_positions)
total_drag = momentum_drag + pressure_drag

# Output results
print(f"Momentum Drag: {momentum_drag:.3f} N/m")
print(f"Pressure Drag: {pressure_drag:.3f} N/m")
print(f"Total Drag: {total_drag:.3f} N/m")