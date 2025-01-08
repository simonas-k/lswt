import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
import pandas as pd

FILE_PATH = "raw_raw_2D_retest2.txt"
CHORDWISE_POSITIONS_FILE = "positions p.txt"  # New text file with x positions
WAKE_POS_FILE = "positions wake.txt"

Vinf = 19.515
Pinf = 906.11
aoa = 15

# Compute slopes
x_data = np.linspace(0, 1, 100)

aoa_values = np.arange(1, 55, 1)

pt_positions = np.array([0, 12, 21, 27, 33, 39, 45, 51, 57, 63, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99,
                         102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147,
                         150, 156, 162, 168, 174, 180, 186, 195, 207, 219])
ps_positions = np.array([43.5, 55.5, 67.5, 79.5, 91.5, 103.5, 115.5, 127.5, 139.5, 151.5, 163.5, 175.5])
data = pd.read_csv(FILE_PATH, sep=r'\s+')  # Use raw string for valid escape sequence

# Convert relevant columns to numeric
pt_columns = [f'P{50+i:03}' for i in range(48)]  # P050 to P097
ps_columns = [f'P{98+i:03}' for i in range(12)]  # P098 to P109

# Ensure numeric data
data[pt_columns] = data[pt_columns].apply(pd.to_numeric, errors='coerce')
data[ps_columns] = data[ps_columns].apply(pd.to_numeric, errors='coerce')

for aoa in aoa_values:


    # Cpl_new = np.interp(x_data, positions_lower, C_p_lower)
    # Cpu_new = np.interp(x_data, positions_upper, C_p_upper)
    # cn_integrand = Cpl_new - Cpu_new
    # cn = cumulative_trapezoid(cn_integrand, x_data, initial=0)
    # cn_final =  cn[-1]
    #
    #
    # alpha_values.append(alpha)


# Plotting Cl and Cd
plt.figure(figsize=(12, 6))

# Plot 1: Cl vs Alpha
plt.figure()
plt.plot(alpha_values, cl_values, marker='o', color='b', label='Cl')
plt.xlabel("Angle of Attack ($\\alpha$)")
plt.ylabel("Lift Coefficient ($C_l$)")
plt.title("Airfoil Lift Coefficient vs Angle of Attack")
plt.grid(True)
plt.legend()
plt.savefig("Cl_vs_Alpha.pdf")
plt.close()
