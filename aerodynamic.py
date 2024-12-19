import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from pressurecoefficient import load_data, load_chordwise_positions, calculate_cp, plot_cp_profile, load_wake_positions, plot_wake_profile

FILE_PATH = "raw_raw_2D_retest2.txt"
CHORDWISE_POSITIONS_FILE = "positions p.txt"  # New text file with x positions
WAKE_POS_FILE = "positions wake.txt"

Vinf = 19.515
Pinf = 906.11
aoa = 25

data = load_data(FILE_PATH)
# print(data)
positions = load_chordwise_positions(CHORDWISE_POSITIONS_FILE)
wake_positions = load_wake_positions(WAKE_POS_FILE)
wake_positions = np.array(wake_positions)
wake_positions = wake_positions / wake_positions[-1]
print("wake pos", wake_positions)
C_p, alpha, C_pt_wake = calculate_cp(data, aoa)
C_p_upper, positions_upper, C_p_lower, positions_lower = plot_cp_profile(positions, C_p, alpha)


C_p_lower = C_p_lower[::-1]
positions_lower = positions_lower[::-1]
positions_lower = np.array(positions_lower)
positions_lower = positions_lower / 100
positions_upper = np.array(positions_upper)
positions_upper = positions_upper / 100
# print(positions_lower)
x_data = np.linspace(0, 1, 100)  # x values (0 to 1)

Cpl_new = np.interp(x_data, positions_lower, C_p_lower)
Cpu_new = np.interp(x_data, positions_upper, C_p_upper)
# print(Cpl_new, Cpu_new)
Cp_diff = -Cpl_new + Cpu_new
cn = cumulative_trapezoid(Cp_diff, x_data, initial=0)
cn_final = cn[-1]
print("cn",cn_final)

#drag
C_pt_wake_new = np.interp(x_data, wake_positions, C_pt_wake)
print(C_pt_wake_new)
integrand = np.sqrt(C_pt_wake_new) * (1 - np.sqrt(C_pt_wake_new))
# print(integrand)
cd_calc = cumulative_trapezoid(integrand,x_data,initial=0)
cd = cd_calc[-1]
print("cd", cd)

cl = cn_final * (np.cos(np.radians(alpha))+(np.sin(np.radians(alpha)))**2 / np.cos(np.radians(alpha))-cd*np.tan(np.radians(alpha)))
print(cl)
print("lift to drag", cl/cd)