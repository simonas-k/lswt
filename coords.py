import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Airfoil coordinates
data = np.array([
    [0, 0],
    [0.35626, 0.77154],
    [1.33331, 1.60115],
    [3.66108, 2.87759],
    [7.2922, 4.15707],
    [11.35604, 5.13022],
    [15.59135, 5.85007],
    [19.91328, 6.3748],
    [24.28443, 6.74148],
    [28.68627, 6.9748],
    [33.10518, 7.09219],
    [37.53128, 7.10225],
    [41.95991, 7.00937],
    [46.38793, 6.81628],
    [50.8156, 6.52532],
    [55.2486, 6.14225],
    [59.69223, 5.68254],
    [64.13685, 5.16453],
    [68.579, 4.59453],
    [73.02401, 3.97658],
    [77.47357, 3.32133],
    [81.93114, 2.63941],
    [86.38589, 1.94846],
    [90.8108, 1.27669],
    [100, 0],
    [0, 0],
    [0.43123, -0.57176],
    [1.47147, -1.09275],
    [3.92479, -1.77203],
    [7.79506, -2.3727],
    [12.0143, -2.76684],
    [16.32276, -3.02746],
    [20.67013, -3.19868],
    [25.03792, -3.30615],
    [29.41554, -3.36298],
    [33.79772, -3.37697],
    [38.18675, -3.35304],
    [42.57527, -3.29378],
    [46.96278, -3.20029],
    [51.35062, -3.07206],
    [55.73662, -2.9106],
    [60.12075, -2.71424],
    [64.50502, -2.48323],
    [68.8901, -2.21935],
    [73.28011, -1.92575],
    [77.67783, -1.61034],
    [82.07965, -1.28273],
    [86.47978, -0.94874],
    [100, 0]
])

# Separate into upper and lower surfaces
upper_surface = data[:25]
lower_surface = data[25:]

# Multiply x-coordinates by 1.6
data[:, 0] *= 1.6

# Remove duplicate (0, 0) from lower surface
lower_surface = lower_surface[1:]

# Process upper surface
x_upper = upper_surface[:, 0]
y_upper = upper_surface[:, 1]

# Ensure strictly increasing x
x_upper_sorted_idx = np.argsort(x_upper)
x_upper = x_upper[x_upper_sorted_idx]
y_upper = y_upper[x_upper_sorted_idx]

# Process lower surface
x_lower = lower_surface[:, 0]
y_lower = lower_surface[:, 1]

# Ensure strictly increasing x
x_lower_sorted_idx = np.argsort(x_lower)
x_lower = x_lower[x_lower_sorted_idx]
y_lower = y_lower[x_lower_sorted_idx]

# Interpolation for upper surface
cubic_interp_upper = CubicSpline(x_upper, y_upper)

# Interpolation for lower surface
cubic_interp_lower = CubicSpline(x_lower, y_lower)

# Generate finer x-coordinates for interpolation
x_fine = np.linspace(0, 160, 500)
y_fine_upper = cubic_interp_upper(x_fine)
y_fine_lower = cubic_interp_lower(x_fine)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(x_upper, y_upper, 'o', label='Upper Surface Data')
plt.plot(x_lower, y_lower, 'o', label='Lower Surface Data')
plt.plot(x_fine, y_fine_upper, '--', label='Upper Surface Interpolation')
plt.plot(x_fine, y_fine_lower, '--', label='Lower Surface Interpolation')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Airfoil Interpolation (Upper and Lower Surfaces)')
plt.legend()
plt.grid()
plt.show()
