"""
    This module contains functions to generate simulation parameters.

"""

import numpy as np
from numpy import sqrt
import math

def random_position_uav(number_UAV, radius_UAV, uav_height):
    """Returns a random UAV position based on 3D Cartesian coordinates.

            x_r: x-axis | y_r: y-axis | z_r: height

    `theta_r:` randomly generates an angle

    `rho_r:` radius in meter of flight trajectory UAV

    `rho_u:` radius in meter of the area where users are distributed

    Arguments:

        number_UAV -- number of UAV.

        radius_UAV -- flight trajectory of the UAV in meters.

        uav_height -- average flight height

    Return:

        x_r, y_r, z_r -- position in the x-axis, y-axis and height of the UAV.
    """
    theta_r = np.random.rand(number_UAV, 1) * (math.pi * 2)
    rho_r = radius_UAV
    x_r = rho_r * np.cos(theta_r)
    y_r = rho_r * np.sin(theta_r)
    z_r = np.random.uniform(uav_height - 5.0, uav_height + 5.0)
    return x_r, y_r, z_r


def random_position_users(number_users, radiusUser):
    """Returns a random ground users position based on 2D Cartesian coordinates.

            x_u: x-axis |  y_u: y-axis | height is not considered

    `theta_u:` randomly generates an angle

    `rho_u:` radius in meter of the area where users are distributed

    Arguments:

        number_users -- number of users.

        radiusUser -- distribution radius of users in the cell in meters.

    Return:

        x_u, y_u -- position in the x-axis and y-axis of the n-th user.

    """
    theta_u = (np.random.rand(number_users, 1)) * (math.pi * 2)
    rho_u = np.sqrt(np.random.rand(number_users, 1)) * radiusUser
    x_u = rho_u * np.cos(theta_u)
    y_u = rho_u * np.sin(theta_u)
    return x_u, y_u


def fading_rician(K, P_los):
    """Returns the mean and standard deviation to model fading from the Rician distribution.

    Arguments:

        K -- Rician factor.

        P_los -- power of line-of-sight path and scattered paths.

    Return:
        s, sigma -- mean and standard deviation to model fading from the Rician distribution.
    """
    # Fading modeled by Rician distribution
    s = np.sqrt(K / (K + 1) * P_los)  # Non-Centrality Parameter (mean)
    sigma = P_los / np.sqrt(2 * (K + 1))  # Standard deviation
    return s, sigma


def generate_channel(
    s, sigma, number_user, user_X, user_Y, uav_X, uav_Y, uav_Z, path_loss
):
    """Returns the channel gains of the users over Rician Fading. The channel gains are sorted to identify
    the primary user and secondary user.

    `small_scale_fading:` calculating  Rician fading channel gains with complex Gaussian random variables with mean=s and variance=sigma.

    `large_scale_fading:`  large-scale fading

    `distance:` calculating distance between UAV and users.

    `h_n:` calculates channel coefficients based on the distance.

    `channelGain:` calculates the channel gains and sorting in descending order.

        Primary user:  channelGain[0]   -> min value

        Secondary user:  channelGain[1] -> max value

    Arguments:

        s -- non-Centrality Parameter (mean).

        sigma -- standard deviation.

        number_user -- number of user.

        user_X -- position axis x of n-th user.

        user_Y -- position axis y of n-th user.

        uav_X -- position axis x of UAV.

        uav_Y -- position axis y of UAV.

        uav_z -- UAV height.

        path_loss -- path loss exponent.

    Return:

        channel_primary --  channel gain of the primary user.

        channel_secondary --  channel gain of the secondary user.

    """
    # Initializing auxiliary arrays to store channel coefficients and distance between UAV and users, respectively:
    h_n = np.zeros(number_user)
    distance = np.zeros(number_user)

    for uu in range(number_user):

        # Generate small scale fading according to Rician Distribution
        small_scale_fading = np.sqrt(
            (np.random.normal(s, sigma) ** 2)
            + 1j * (np.random.normal(0, sigma) ** 2)
        )
        # Normalized distance
        distance[uu] = np.sqrt(
            (user_X[uu] - uav_X) ** 2 + (user_Y[uu] - uav_Y) ** 2 + uav_Z ** 2
        )
        # Generate path loss atenuation
        large_scale_fading = sqrt( (distance[uu])**( path_loss))

        # Generate channel coefficients
        h_n[uu] = (
            np.abs(small_scale_fading / large_scale_fading )
            ** 2
        )

    channel_primary = np.min(h_n)
    channel_secondary = np.max(h_n)

    return channel_primary, channel_secondary