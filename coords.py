import numpy as np
from scipy.interpolate import CubicSpline


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
