import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

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

def process_airfoil(data, scale_factor=1.6):
    """
    Process airfoil data, scale x-coordinates, and prepare interpolations for upper and lower surfaces.

    Parameters:
        data (numpy.ndarray): Airfoil data as a 2D array (x, y).
        scale_factor (float): Scaling factor for x-coordinates.

    Returns:
        dict: A dictionary containing interpolation objects for upper and lower surfaces.
    """
    # Scale x-coordinates
    data[:, 0] *= scale_factor

    # Separate into upper and lower surfaces
    upper_surface = data[:25]
    lower_surface = data[25:]

    # Remove duplicate (0, 0) from lower surface
    lower_surface = lower_surface[1:]

    # Create cubic interpolations for both surfaces
    upper_interp = CubicSpline(upper_surface[:, 0], upper_surface[:, 1])
    lower_interp = CubicSpline(lower_surface[:, 0], lower_surface[:, 1])

    return {"upper": upper_interp, "lower": lower_interp}


def get_slope(interpolations, x, surface="upper"):
    """
    Calculate the slope of the airfoil at a given x-coordinate.

    Parameters:
        interpolations (dict): Dictionary containing interpolation objects for "upper" and "lower" surfaces.
        x (float): x-coordinate to calculate the slope.
        surface (str): Specify "upper" or "lower" to choose the surface.

    Returns:
        float: The slope at the given x-coordinate on the specified surface.
    """
    if surface not in interpolations:
        raise ValueError("Invalid surface. Choose 'upper' or 'lower'.")

    # Get the derivative (slope) of the cubic spline at x
    slope = interpolations[surface].derivative()(x)
    return slope


# Process airfoil data
scale_factor = 1.6
interpolations = process_airfoil(airfoil_data, scale_factor)

# Generate x-coordinates for plotting
x_values = np.linspace(0, 100 * scale_factor, 500)

# Calculate y-values for airfoil and slopes
upper_y = interpolations["upper"](x_values)
lower_y = interpolations["lower"](x_values)

upper_slope = interpolations["upper"].derivative()(x_values)
lower_slope = interpolations["lower"].derivative()(x_values)

# Plot airfoil geometry
plt.figure(figsize=(14, 6))

# Plot upper and lower surfaces
plt.subplot(1, 2, 1)
plt.plot(x_values, upper_y, label="Upper Surface", color="blue")
plt.plot(x_values, lower_y, label="Lower Surface", color="red")
plt.scatter(airfoil_data[:25, 0], airfoil_data[:25, 1], color="blue", s=10, label="Upper Points")
plt.scatter(airfoil_data[26:, 0], airfoil_data[26:, 1], color="red", s=10, label="Lower Points")
plt.title("Airfoil Geometry")
plt.xlabel("x-coordinate (scaled)")
plt.ylabel("y-coordinate")
plt.legend()
plt.grid(True)

# Plot slopes
plt.subplot(1, 2, 2)
plt.plot(x_values, upper_slope, label="Upper Slope", color="blue")
plt.plot(x_values, lower_slope, label="Lower Slope", color="red")
plt.title("Airfoil Slopes")
plt.xlabel("x-coordinate (scaled)")
plt.ylabel("Slope (dy/dx)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
