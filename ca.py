import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Airfoil data (x, y coordinates)
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

# Split the data into upper and lower surfaces
upper_surface = airfoil_data[:25]
lower_surface = airfoil_data[25:]

# Extract x and y values for upper and lower surfaces
x_upper = upper_surface[:, 0]
y_upper = upper_surface[:, 1]
x_lower = lower_surface[:, 0]
y_lower = lower_surface[:, 1]

# Normalize x to be between 0 and 1 (as percentage of chord) for both surfaces
x_upper_normalized = x_upper / x_upper[-1]  # Normalize by the last x-value of the upper surface
x_lower_normalized = x_lower / x_lower[-1]  # Normalize by the last x-value of the lower surface

# Interpolate y-values for a finer grid of x (as percentage) for both surfaces
interp_upper = interp1d(x_upper_normalized, y_upper, kind='cubic', fill_value='extrapolate')
interp_lower = interp1d(x_lower_normalized, y_lower, kind='cubic', fill_value='extrapolate')

x_fine_upper = np.linspace(0, 1, 500)  # A finer grid for the upper surface (0 to 1)
x_fine_lower = np.linspace(0, 1, 500)  # A finer grid for the lower surface (0 to 1)

y_fine_upper = interp_upper(x_fine_upper)
y_fine_lower = interp_lower(x_fine_lower)

# Calculate the slope (dy/dx) using numerical differentiation for both surfaces
slopes_upper = np.diff(y_fine_upper) / np.diff(x_fine_upper)
slopes_lower = np.diff(y_fine_lower) / np.diff(x_fine_lower)

# To match the length of the original data (since np.diff reduces the array size by 1)
# Add NaN at the end to align with the original x and y arrays
slopes_upper = np.concatenate(([np.nan], slopes_upper))
slopes_lower = np.concatenate(([np.nan], slopes_lower))

# Print the slopes for both surfaces
print("Slopes of the upper surface (dy/dx):")
print(slopes_upper)

print("Slopes of the lower surface (dy/dx):")
print(slopes_lower)

# Plot the results
plt.figure(figsize=(10, 8))

# Plot the airfoil data for both surfaces
plt.subplot(2, 1, 1)
plt.plot(x_upper_normalized, y_upper, label='Upper Surface (Original)', color='b')
plt.plot(x_lower_normalized, y_lower, label='Lower Surface (Original)', color='r')
plt.plot(x_fine_upper, y_fine_upper, label='Upper Surface (Interpolated)', color='g', linestyle='--')
plt.plot(x_fine_lower, y_fine_lower, label='Lower Surface (Interpolated)', color='orange', linestyle='--')
plt.title('Airfoil Shape (Upper and Lower Surfaces)')
plt.xlabel('x (Chord Position as Percentage)')
plt.ylabel('y (Surface Height)')
plt.grid(True)
plt.legend()

# Plot the slopes (dy/dx) for both surfaces
plt.subplot(2, 1, 2)
plt.plot(x_fine_upper, slopes_upper, label='Slopes (Upper Surface)', color='b')
plt.plot(x_fine_lower, slopes_lower, label='Slopes (Lower Surface)', color='r')
plt.title('Slopes of the Airfoil (dy/dx)')
plt.xlabel('x (Chord Position as Percentage)')
plt.ylabel('Slope (dy/dx)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()