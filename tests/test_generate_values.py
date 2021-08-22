import pytest
import numpy as np
from uavnoma.generate_values import *


# Valid and invalid parameters for testing the generate_values of uavnoma package
data_parameter_position_user = [
    (2, 10), # Valid # number_user, radius_user 
    (4, 6),  # Invalid
    (2, 18), # Valid
    (2, -1), # Invalid
]

data_parameter_position_uav = [
    (1, 2, 20), # Valid # number_uav, radius_uav, height_uav
    (1, 6, -2), # Invalid
    (1, 4, 25), # Valid
    (1, -1, 80),# Invalid  
]

data_parameter_rician_fading = [
    (15, 1),  # Valid # rician_factor, power_los
    (18, 2),  # Valid
    (-2, 15), # Invalid
    (26, -1),  # Invalid
]

""" data_parameter_generate_channel = [
    (2, 10.0, 6.0, 2.0, 4.0, 35.0, 2.0, 15.0, 1.0) # Valid # number_user, axis x user position, axis y user position, axis x uav position, axis y uav position, uav mean height, path_loss, rician_factor, power_los
    (4, 2.0, 15.0, 4.0, 2.0, 20.0, 2.2, 18.0, 2.0), # Invalid
    (2, 10.0, 10.0, 2.0, 3.0, 40.0, 2.0, 16.0, 2.0),  # Valid
    (4, 8.0, 15.0, 2.0, 3.0, 40.0, 8.0, 3.0, 4.0),   # Invalid
] """

# Test user position
@pytest.mark.parametrize("number_users, radius_user", data_parameter_position_user)
def test_position_user(number_users, radius_user): 
    assert number_users == 2
    x_u, y_u = random_position_users(number_users, radius_user)
    assert x_u.all() <= radius_user
    assert y_u.all() <= radius_user



# Test uav position
@pytest.mark.parametrize("number_uav, radius_uav, height_uav", data_parameter_position_uav)
def test_position_uav(number_uav, radius_uav, height_uav):
    assert number_uav == 1
    x_u, y_u, z_u = random_position_uav(number_uav, radius_uav, height_uav)
    assert x_u <= radius_uav
    assert y_u <= radius_uav
    assert (
        height_uav - 5 <= z_u <= height_uav + 5
    )


# Test rician fading
@pytest.mark.parametrize("rician_factor, power_los", data_parameter_rician_fading)
def test_rician_parameters(rician_factor, power_los):
    # Fading modeled by Rician distribution
        s, sigma = fading_rician(rician_factor, power_los)
        assert s > 0 and s < 2  # Non-negative
        assert sigma > 0 and sigma <= 1.5  # Non-negative


# Test generate channel
""" @pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, rician_factor, power_los", data_parameter_generate_channel)
def test_channel_gain(fading_rician,number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, rician_factor, power_los):
    s = np.sqrt(rician_factor / (rician_factor + 1) * power_los)  # Non-Centrality Parameter (mean)
    sigma = power_los / np.sqrt(2 * (rician_factor + 1))  # Standard deviation   
    channel_gain_primary, channel_gain_secondary = generate_channel(
        s, sigma, number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss
    )
    assert channel_gain_primary >= 0  # Non-negative
    assert channel_gain_secondary >= 0  # Non-negative
    assert channel_gain_primary <= channel_gain_secondary """
