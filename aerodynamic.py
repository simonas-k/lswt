import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from pressurecoefficient import load_data, load_chordwise_positions, calculate_cp, plot_cp_profile
from scipy.interpolate import CubicSpline
from coords import process_airfoil, get_slope

FILE_PATH = "raw_raw_2D_retest2.txt"
CHORDWISE_POSITIONS_FILE = "positions p.txt"  # New text file with x positions
WAKE_POS_FILE = "positions wake.txt"

airfoil_data = np.array([
    [0, 0], [0.35626, 0.77154], [1.33331, 1.60115], [3.66108, 2.87759], [7.2922, 4.15707],
    [11.35604, 5.13022], [15.59135, 5.85007], [19.91328, 6.3748], [24.28443, 6.74148], [28.68627, 6.9748],
    [33.10518, 7.09219], [37.53128, 7.10225], [41.95991, 7.00937], [46.38793, 6.81628], [50.8156, 6.52532],
    [55.2486, 6.14225], [59.69223, 5.68254], [64.13685, 5.16453], [68.579, 4.59453], [73.02401, 3.97658],
    [77.47357, 3.32133], [81.93114, 2.63941], [86.38589, 1.94846], [90.8108, 1.27669], [100, 0],
    [0, 0], [0.43123, -0.57176], [1.47147, -1.09275], [3.92479, -1.77203], [7.79506, -2.3727],
    [12.0143, -2.76684], [16.32276, -3.02746], [20.67013, -3.19868], [25.03792, -3.30615], [29.41554, -3.36298],
    [33.79772, -3.37697], [38.18675, -3.35304], [42.57527, -3.29378], [46.96278, -3.20029], [51.35062, -3.07206],
    [55.73662, -2.9106], [60.12075, -2.71424], [64.50502, -2.48323], [68.8901, -2.21935], [73.28011, -1.92575],
    [77.67783, -1.61034], [82.07965, -1.28273], [86.47978, -0.94874], [100, 0]
])

Vinf = 19.515
Pinf = 906.11
aoa = 15

aoa_values = np.arange(10, 50, 1)

alpha_values = []
cl_values = []
cd_values = []
for aoa in aoa_values:

    # Process the airfoil data
    interpolations = process_airfoil(airfoil_data)

    data = load_data(FILE_PATH)
    # print(data)
    positions = load_chordwise_positions(CHORDWISE_POSITIONS_FILE)
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
    cn_integrand = Cpl_new - Cpu_new
    cn = cumulative_trapezoid(cn_integrand, x_data, initial=0)
    cn_final = cn[-1]

    # Compute slopes
    upper_slopes = get_slope(interpolations, x_data, surface="upper")
    lower_slopes = get_slope(interpolations, x_data, surface="lower")

    ca_integrand = Cpu_new*upper_slopes - Cpl_new*lower_slopes
    ca = cumulative_trapezoid(ca_integrand, x_data, initial=0)
    ca_final = ca[-1]

    # Calculate cl and cd
    cl = cn_final * np.cos(np.radians(alpha)) - ca_final * np.sin(np.radians(alpha))
    cd = ca_final * np.cos(np.radians(alpha)) + cn_final * np.sin(np.radians(alpha))
    # print("Lift Coefficient =", cl)
    # print("Drag Coefficient =", cd)

    np.append(alpha_values,alpha)
    np.append(cl_values,cl)
    np.append(cd_values,cd)

