import pytest
import numpy as np
from uavnoma.generate_values import *

#
# Valid and invalid parameters for testing the generate_values module
#

data_parameter_position_user_valid = [
    # number_user, radius_user
    ([2, 10]), # Valid
    ([2, 18]), # Valid
]

data_parameter_position_user_invalid = [
    # number_user, radius_user
    ([4, 6]),  # Invalid
    ([2, -1]), # Invalid
]

data_parameter_position_uav_valid = [
    # number_uav, radius_uav, height_uav
    ([1, 2, 20]), # Valid
    ([1, 4, 25]), # Valid
]

data_parameter_position_uav_invalid = [
    # number_uav, radius_uav, height_uav
    ([1, 15, -2]), # Invalid
    ([1, 4, 25]), # Valid
]

data_parameter_rician_fading_valid = [
    # rician_factor, power_los
    ([15, 1]),  # Valid
    ([18 , 2]),  # Valid
]

data_parameter_rician_fading_invalid = [
    # rician_factor, power_los
    ([-2, 15]), # Invalid
    ([26, -1]), # Invalid
]

data_parameter_generate_channel_valid = [
    # number_user, array axis x user position, array axis y user position,  axis x uav position, axis y uav position, uav mean height, path_loss, mean rician distribution, standard deviation
    ([2, np.array([10.0, 6.0]), np.array([2.0, 8.0]), 2.0, 4.0, 35.0, 2.0, 0.5, 1.3]),  # Valid
    ([2, np.array([14.0, -2.0]), np.array([2.0, -12.0]), 1.0, 3.0, 40.0, 2.0, 0.1, 1.0]), # Valid
]

data_parameter_generate_channel_invalid = [
    # exception, number_user, array axis x user position, array axis y user position, axis x uav position, axis y uav position, uav mean height, path_loss, mean rician distribution, standard deviation

    # This will throw an IndexError due to incorrect number of users (function only supports 2 users for now)
    ([IndexError, 4, np.array([3.0, 10.0]), np.array([7.0, 15.0]), 2.0, 4.0, 40.0, 8.0, -0.5, 2.5]),
    # This will throw a ValueError due to negative standard deviation
    ([ValueError, 2, np.array([2.0, -15.0]), np.array([-2.0, 10.0]), 7.0, 3.0, 25.0, -1.0, -3.0, -4.0]),
]

#
# Tests for generate_values module
#

# Test user position (valid parameters)
@pytest.mark.parametrize("number_users, radius_user", data_parameter_position_user_valid)
def test_position_user_valid(number_users, radius_user):
    assert number_users == 2
    x_u, y_u = random_position_users(number_users, radius_user)
    assert x_u.all() <= radius_user
    assert y_u.all() <= radius_user

# Test user position (invalid parameters)
@pytest.mark.parametrize("number_users, radius_user", data_parameter_position_user_invalid)
def test_position_user_invalid(number_users, radius_user):
    # Although the parameters are invalid for the simulation as a whole, this
    # function will work its math without throwing exceptions
    random_position_users(number_users, radius_user)

# Test uav position (valid parameters)
@pytest.mark.parametrize("number_uav, radius_uav, height_uav", data_parameter_position_uav_valid)
def test_position_uav_valid(number_uav, radius_uav, height_uav):
    assert number_uav == 1
    x_u, y_u, z_u = random_position_uav(number_uav, radius_uav, height_uav)
    assert x_u <= radius_uav
    assert y_u <= radius_uav
    assert (
        height_uav - 5 <= z_u <= height_uav + 5
    )

# Test uav position (invalid parameters)
@pytest.mark.parametrize("number_uav, radius_uav, height_uav", data_parameter_position_uav_invalid)
def test_position_uav_invalid(number_uav, radius_uav, height_uav):
    # Although the parameters are invalid for the simulation as a whole, this
    # function will work its math without throwing exceptions
    random_position_uav(number_uav, radius_uav, height_uav)

# Test rician fading (valid parameters)
@pytest.mark.parametrize("rician_factor, power_los", data_parameter_rician_fading_valid)
def test_rician_parameters_valid(rician_factor, power_los):
    # Fading modeled by Rician distribution
    s, sigma = fading_rician(rician_factor, power_los)
    assert s > 0 and s <=1.5  # Non-negative
    assert sigma > 0 and sigma <= 1.5  # Non-negative

# Test rician fading (invalid parameters)
@pytest.mark.parametrize("rician_factor, power_los", data_parameter_rician_fading_invalid)
def test_rician_parameters_invalid(rician_factor, power_los):
    # This function will throw runtime warnings due to invalid values passed to
    # NumPy's sqrt() function
    with pytest.warns(RuntimeWarning):
        fading_rician(rician_factor, power_los)

# Test generate channel (valid parameters)
@pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma", data_parameter_generate_channel_valid)
def test_channel_gain_valid(number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma):
    assert number_user == 2
    channel_gain_primary, channel_gain_secondary = generate_channel(
        s, sigma, number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss
    )
    assert channel_gain_primary >= 0  # Non-negative
    assert channel_gain_secondary >= 0  # Non-negative
    assert channel_gain_primary <= channel_gain_secondary

# Test generate channel (invalid parameters)
@pytest.mark.parametrize("exception, number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma", data_parameter_generate_channel_invalid)
def test_channel_gain_invalid(exception, number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma):
    with pytest.raises(exception):
        generate_channel(s, sigma, number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss)
