import numpy as np
import math
from uavnoma.performance_metrics import *
from uavnoma.generate_values import fading_rician, generate_channel
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
target_rate_primary_user = 0.5 # Target rate bits/s/Hertz  primary user
target_rate_secondary_user = 0.5 # Target rate bits/s/Hertz  secondary user


data_parameter_rate = [    
    ( # Valid
        [2,    # number_user
        10.0,  # axis x user position
        6.0,   # axis y user position
        2.0,   # axis x uav position
        4.0,   # axis y uav position
        35.0,  # uav mean height
        2.0,   # path_loss,
        15.0,  # rician_factor
        1.0,   # power_los
        0.8,   # power_primary
        0.2,   # power_secondary 
        0.05,  # hardware impairments
        0.05]
        ), # imperfect SIC coeffcient
    ( # Invalid
        [4,    # number_user
        25.0,  # axis x user position
        6.0,   # axis y user position
        6.0,   # axis x uav position
        4.0,   # axis y uav position
        80.0,  # uav mean height
        2.0,   # path_loss,
        2.0,  # rician_factor
        3.0,   # power_los
        0,   # power_primary
        0.9,   # power_secondary 
        0.05,  # hardware impairments
        0.05]
        ), # imperfect SIC coeffcient
]

# Test generate channel
@pytest.mark.parametrize("number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, rician_factor, power_los, power_primary, power_secondary, hardw_ip, sic_ip", data_parameter_rate)
def test_rate_primary_user(number_user, x_u, y_u, x_r, y_r, uav_height_mean, path_loss, rician_factor, power_los, power_primary, power_secondary, hardw_ip, sic_ip):
    for mc in range(monte_carlo_samples):
        s, sigma = fading_rician(rician_factor, power_los)
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
"""
def test_rate_secondary_user():
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
        assert channel_gain_primary <= channel_gain_secondary  # Must be in descending order
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

def test_average_rate():
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



def test_outage_probability():
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
    ), "Invalid, must be non-negative." """