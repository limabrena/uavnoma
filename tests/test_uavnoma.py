import numpy as np
import math

from uavnoma.generate_values import *
from uavnoma.performance_metrics import * 



# Variable simulation parameters
monte_carlo_samples = 100000  # Monte Carlo samples
power_los = 1.0 # power of Line-of-Sigth path & scattered paths (1<= power_los <= 2)
rician_factor = 15 # Rician factor value (10<= rician_factor <= 15)
path_loss = 2.2 # Path loss exponent (2 <= path_loss <= 3)
snr_dB = np.array(range(10, 61, 2)) # SNR in dB
snr_linear = 10.0 ** (snr_dB / 10.0)  # SNR linear
radius_uav = 2.0 # Radius fly trajectory of the UAV in meters
radius_user = 10.0  # Distribution radius of users in the cell in meters.
uav_heigth_mean = 15.0 # Average UAV flight height
target_rate_primary_user = 0.5 # Target rate bits/s/Hertz  primary user
target_rate_secondary_user = 0.5 # Target rate bits/s/Hertz  secondary user
hardw_ip = 0.01 # Residual Hardware Impairments
sic_ip = 0.01  # Residual Imperfect SIC

power_primary = 0.8 # Power allocation factor primary user
power_secondary = 0.2 # Power allocation factor secondary user


# fixed simulation parameters
number_user = 2 # Number of users
number_uav = 1 # Number of UAV

theta_r = np.random.rand(number_uav, 1) * (math.pi * 2)
rho_r = radius_uav
x_r = rho_r * np.cos(theta_r)
y_r = rho_r * np.sin(theta_r)


theta_u = (np.random.rand(number_user, 1)) * (math.pi * 2)
rho_u = np.sqrt(np.random.rand(number_user, 1)) * radius_user
x_u = rho_u * np.cos(theta_u)
y_u = rho_u * np.sin(theta_u)

s = np.sqrt(rician_factor / (rician_factor + 1) * power_los)  # Non-Centrality Parameter (mean)
sigma = power_los / np.sqrt(2 * (rician_factor + 1))  # Standard deviation
snr_dB = np.array(range(10, 51, 2))  # SNR in dB
snr_linear = 10 ** (snr_dB / 10)  # SNR linear

# Initialization of some auxiliary arrays
out_probability_system = np.zeros((monte_carlo_samples, len(snr_dB)))
out_probability_secondary_user = np.zeros((monte_carlo_samples, len(snr_dB)))
out_probability_primary_user = np.zeros((monte_carlo_samples, len(snr_dB)))
system_average_rate = np.zeros((monte_carlo_samples, len(snr_dB)))
rate_secondary_user = np.zeros((monte_carlo_samples, len(snr_dB)))
rate_primary_user = np.zeros((monte_carlo_samples, len(snr_dB)))



def test_parameters():
    assert (
        10000 <= monte_carlo_samples <= 1000000
    ), "Invalid quantity, the value entered must be 10000 <= monte_carlo_samples <= 1000000."
    assert number_user == 2, "Number of users must be 2."
    assert (
        power_los == 1.0 or power_los == 2.0
    ), "Invalid power of Line-of-Sigth path & scattered paths."
    assert (
        rician_factor >= 0 and rician_factor <= 18
    ), "Invalid Rician factor, the value must be (0<= value <= 10)"
    assert number_uav == 1, "Number of UAV must be 1."
    assert number_user == 2, "Number of UAV must be 2."
    assert path_loss > 1.0 or path_loss < 3.0
    assert snr_dB.all() >= 0
    assert snr_linear.all() >= 0
    assert radius_uav >= 1
    assert radius_user >= 1
    assert target_rate_primary_user > 0
    assert target_rate_secondary_user > 0
    assert hardw_ip >= 0
    assert sic_ip >= 0

    assert (
        power_primary >= power_secondary
    ),  "The power coefficient of the primary user must be greater than that of the Secondary user."

    sum_power = power_primary + power_secondary
    assert (sum_power > 0) and (
        sum_power <= 1
    ) , "The sum of the powers must be > 0 or <= 1."


def test_position_user():
    x_u, y_u = random_position_users(number_user, radius_user)
    assert x_u.all() <= radius_user
    assert y_u.all() <= radius_user


def test_position_uav():
    x_r, y_r, height = random_position_uav(number_uav, radius_uav, uav_heigth_mean)
    assert number_uav == 1
    assert x_r.all() <= radius_uav
    assert y_r.all() <= radius_uav
    assert (
       uav_heigth_mean - 5 <= height <= uav_heigth_mean + 5
    )

def test_rician_parameters():
    # Fading modeled by Rician distribution
    s, sigma = fading_rician(rician_factor, power_los)
    assert s >= 0  # Non-negative
    assert sigma >= 0  # Non-negative
 

def test_channel_gain():
    channel_gain_primary, channel_gain_secondary = generate_channel(
        s, sigma, number_user, x_u, y_u, x_r, y_r, uav_heigth_mean, path_loss 
    )
    assert channel_gain_primary >= 0  # Non-negative
    assert channel_gain_secondary >= 0  # Non-negative
    assert channel_gain_primary <= channel_gain_secondary  


def test_rate_primary_user():
    for mc in range(monte_carlo_samples):
        channel_gain_primary, channel_gain_secondary = generate_channel(
            s, 
            sigma, 
            number_user, 
            x_u,
            y_u, 
            x_r, 
            y_r, 
            uav_heigth_mean, 
            path_loss,
        )
        assert channel_gain_primary <= channel_gain_secondary  
        for sn in range(0, len(snr_linear)):
            rate_primary_user[mc, sn] = calculate_instantaneous_rate_primary(
                channel_gain_primary,
                snr_linear[sn],
                power_primary,
                power_secondary,
                hardw_ip,
            )

    assert rate_primary_user.all() >= 0  # Non-negative

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
            uav_heigth_mean, 
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
            uav_heigth_mean, 
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
            s, sigma, number_user, x_u, y_u, x_r, y_r, uav_heigth_mean, path_loss 
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

