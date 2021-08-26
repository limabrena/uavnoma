import numpy as np
from uavnoma.performance_metrics import *
from uavnoma.generate_values import generate_channel
import pytest

# Variable simulation parameters
monte_carlo_samples = 1000  # Monte Carlo samples
snr_dB = np.array(range(10, 51, 2))  # SNR in dB
snr_linear = 10 ** (snr_dB / 10)  # SNR linear

# Initialization of some auxiliary arrays
out_probability_system = np.zeros((monte_carlo_samples, len(snr_dB)))
out_probability_secondary_user = np.zeros((monte_carlo_samples, len(snr_dB)))
out_probability_primary_user = np.zeros((monte_carlo_samples, len(snr_dB)))
system_average_rate = np.zeros((monte_carlo_samples, len(snr_dB)))
rate_secondary_user = np.zeros((monte_carlo_samples, len(snr_dB)))
rate_primary_user = np.zeros((monte_carlo_samples, len(snr_dB)))

#
# Valid and invalid parameters for testing the performance_metrics module
#

data_parameter_rate_valid = [    
    ( 
        2,    # number of users
        np.array([10.0, 6.0]),  # array axis x user 1 and user 2 position
        np.array([2.0, 8.0]),   # array axis y user 1 and user 2 position
        2.0,   # axis x uav position
        4.0,   # axis y uav position
        35.0,  # uav mean height
        2.0,   # path loss exponent,
        0.03,  # mean rician fading
        1.3,   # standard deviation
        0.8,   # power_primary
        0.2,   # power_secondary 
        0.05,  # hardware impairments
        0.05,  # imperfect SIC coeffcient
    ) 
]

""" data_parameter_rate_invalid = [    
    ( 
        4,    # number of users
        np.array([7.0, -16.0]),   # array axis x user 1 and user 2 position
        np.array([25.0, 10.0]),   # array axis y user 1 and user 2 position
        6.0,   # axis x uav position
        4.0,   # axis y uav position
        80.0,  # uav mean height
        2.0,   # path loss exponent,
        -0.1,  # mean rician fading
        3.0,   # standard deviation
        0.0,   # power_primary
        0.9,   # power_secondary 
        0.05,  # hardware impairments
        1.1,   # imperfect SIC coeffcient
    ) 
] """

data_target_rate_valid = [
    # Target rate primary user, Target rate secondary user
    ([0.5, 0.5])
]

""" data_target_rate_invalid = [
    # Target rate primary user, Target rate secondary user
    ([2, -4])
] """

# Test rate primary user (valid parameters)
@pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip", data_parameter_rate_valid)
def test_rate_primary_user(number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip):
    for mc in range(monte_carlo_samples):
        channel_gain_primary, channel_gain_secondary = generate_channel(
            s,
            sigma,
            number_user,
            x_u,
            y_u,
            x_r,
            y_r,
            uav_height_mean,
            path_loss,
        )
        assert number_user == 2
        assert sic_ip >= 0 and sic_ip <= 1
        assert hardw_ip >= 0 and hardw_ip <= 1
        assert channel_gain_primary <= channel_gain_secondary
        assert channel_gain_primary >= 0
        assert channel_gain_secondary >= 0
        for sn in range(0, len(snr_linear)):
            rate_primary_user[mc, sn] = calculate_instantaneous_rate_primary(
                channel_gain_primary,
                snr_linear[sn],
                power_primary,
                power_secondary,
                hardw_ip,
            )

    assert rate_primary_user.all() >= 0  # Non-negative 
@pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip", data_parameter_rate_valid)
def test_rate_secondary_user(number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip):
    for mc in range(monte_carlo_samples):
        channel_gain_primary, channel_gain_secondary = generate_channel(
            s,
            sigma,
            number_user,
            x_u,
            y_u,
            x_r,
            y_r,
            uav_height_mean,
            path_loss,
        )
        assert number_user == 2
        assert sic_ip >= 0 and sic_ip <= 1
        assert hardw_ip >= 0 and hardw_ip <= 1
        assert channel_gain_primary <= channel_gain_secondary
        assert channel_gain_primary >= 0
        assert channel_gain_secondary >= 0
        for sn in range(0, len(snr_linear)):
            rate_secondary_user[mc,sn] = calculate_instantaneous_rate_secondary(
                channel_gain_secondary,
                snr_linear[sn],
                power_secondary,
                power_primary,
                hardw_ip,
                sic_ip
            )

    assert rate_secondary_user.all() >= 0  # Non-negative
@pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip", data_parameter_rate_valid)
def test_average_rate(number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip):
    for mc in range(monte_carlo_samples):
        channel_gain_primary, channel_gain_secondary = generate_channel(
            s,
            sigma,
            number_user,
            x_u,
            y_u,
            x_r,
            y_r,
            uav_height_mean,
            path_loss,
        )
        assert number_user == 2
        assert sic_ip >= 0 and sic_ip <= 1
        assert hardw_ip >= 0 and hardw_ip <= 1
        assert channel_gain_primary <= channel_gain_secondary
        assert channel_gain_primary >= 0
        assert channel_gain_secondary >= 0
        for sn in range(0, len(snr_linear)):
            rate_primary_user[mc, sn] = calculate_instantaneous_rate_primary(
                channel_gain_primary,
                snr_linear[sn],
                power_primary,
                power_secondary,
                hardw_ip,
            )
            rate_secondary_user[mc,sn] = calculate_instantaneous_rate_secondary(
                channel_gain_secondary,
                snr_linear[sn],
                power_secondary,
                power_primary,
                hardw_ip,
                sic_ip,
            )
            system_average_rate[mc, sn] = average_rate(
                rate_primary_user[mc, sn],
                rate_primary_user[mc, sn],
            )

    assert system_average_rate.all() >= 0, "Invalid, must be non-negative."


# Test outage probability (valid parameters)
@pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip", data_parameter_rate_valid)
@pytest.mark.parametrize("target_rate_primary_user, target_rate_secondary_user", data_target_rate_valid)
def test_outage_probability(number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, s, sigma, power_primary, power_secondary, hardw_ip, sic_ip, target_rate_primary_user, target_rate_secondary_user):
    for mc in range(monte_carlo_samples):
        channel_gain_primary, channel_gain_secondary = generate_channel(
            s, sigma, number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss
        )
        for sn in range(0, len(snr_linear)):
            rate_primary_user[mc, sn] = calculate_instantaneous_rate_primary(
                channel_gain_primary,
                snr_linear[sn],
                power_primary,
                power_secondary,
                hardw_ip,
            )
            rate_secondary_user[mc,sn] = calculate_instantaneous_rate_secondary(
                channel_gain_secondary,
                snr_linear[sn],
                power_secondary,
                power_primary,
                hardw_ip,
                sic_ip,
            )
            (
                out_probability_system[mc,sn],
                out_probability_primary_user[mc,sn],
                out_probability_secondary_user[mc,sn],
            ) = outage_probability(
                    rate_primary_user[mc, sn],
                    rate_secondary_user[mc, sn],
                    target_rate_primary_user,
                    target_rate_secondary_user,
                )
    assert (
        out_probability_system.all() >= 0 or out_probability_system.all() <= 1
    ), "Invalid, must be non-negative."
    assert (
        out_probability_primary_user.all() >= 0
        or out_probability_primary_user.all() <= 1
    ), "Invalid, must be non-negative."
    assert (
        out_probability_secondary_user.all() >= 0
        or out_probability_secondary_user.all() <= 1
    ), "Invalid, must be non-negative." 

