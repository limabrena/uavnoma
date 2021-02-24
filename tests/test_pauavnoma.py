import numpy as np
import math

# from pauavnoma.generate_values import random_position_uav,random_position_users,generate_channel,calculate_instantaneous_rate_primary,calculate_instantaneous_rate_secondary
# from pauavnoma.parameters import  init_parameters, generate_power_coeff
from pauavnoma.uavnoma import valuesGen, mainStructure
#from main import main_values

N_users = 2
P_los = 1.0  # 1.0 or 2.0
K = 8  #  0 ~ 10
path_loss_exp = 2
M_uav = 1
radius_uav = 1.0
radius_user = 2.0
target_rate_primary_user = 1
target_rate_secondary_user = 0.5

theta_r = np.random.rand(M_uav, 1) * (math.pi * 2)
rho_r = radius_uav
x_r = rho_r * np.cos(theta_r)
y_r = rho_r * np.sin(theta_r)
z_r = 30.0

theta_u = (np.random.rand(N_users, 1)) * (math.pi * 2)
rho_u = np.sqrt(np.random.rand(N_users, 1)) * radius_user
x_u = rho_u * np.cos(theta_u)
y_u = rho_u * np.sin(theta_u)

s = np.sqrt(K / (K + 1) * P_los)  # Non-Centrality Parameter (mean)
sigma = P_los / np.sqrt(2 * (K + 1))  # Standard deviation
snr_values_dB = np.array(range(10, 51, 2))  # SNR in dB
snr_values_linear = 10 ** (snr_values_dB / 10)  # SNR linear


def test_parameter():
    (
        samples_mc,
        number_users,
        power_los,
        rician_factor,
        path_loss_value,
        number_uav,
        snr_values_dB,
        snr_values_linear,
        radius_value_uav,
        radius_value_user,
        rate_value_primary_user,
        rate_value_secondary_user,
    ) = valuesGen.init_parameters()
    assert (
        10000 <= samples_mc <= 1000000
    ), "Invalid quantity, the value entered must be 10000<=samples_mc <= 1000000."
    assert number_users == 2, "Number of users must be 2."
    assert (
        power_los == 1.0 or power_los == 2.0
    ), "Invalid power of Line-of-Sigth path & scattered paths."
    assert (
        rician_factor >= 0 and rician_factor <= 10
    ), "Invalid Rician factor, the value must be (0<= value <= 10)"
    assert number_uav == 1, "Number of UAV must be 1."
    assert path_loss_value > 1.0 or path_loss_value < 3.0
    assert snr_values_dB.all() >= 0
    assert snr_values_linear.all() >= 0
    assert radius_value_uav >= 1
    assert radius_value_user >= 1
    assert rate_value_primary_user > 0
    assert rate_value_secondary_user > 0


def test_position_user():
    x_u, y_u = valuesGen.random_position_users(N_users, radius_user)
    assert x_u.all() <= radius_user
    assert y_u.all() <= radius_user


def test_position_uav():
    x_r, y_r, height = valuesGen.random_position_uav(M_uav, radius_uav)
    assert M_uav == 1
    assert x_r.all() <= radius_uav
    assert y_r.all() <= radius_uav
    assert height == z_r


def test_power_coeff_sum():
    sum_power = np.sum(valuesGen.generate_power_coeff(N_users))
    assert (sum_power > 0) and (
        sum_power <= 1
    )  # The sum of the powers must be > 0 or <= 1


def test_power_order():
    power_Primary, power_Secondary = valuesGen.generate_power_coeff(N_users)
    assert (
        power_Primary >= power_Secondary
    )  # The power coefficient of the primary user must be greater than that of the Secondary user.


def test_channel_gain():
    channelGain_Primary, channelGain_Secondary = valuesGen.generate_channel(
        s, sigma, N_users, x_u, y_u, x_r, y_r, path_loss_exp, z_r
    )
    assert channelGain_Primary >= 0  # Non-negative
    assert channelGain_Secondary >= 0  # Non-negative
    assert channelGain_Primary >= channelGain_Secondary  # Must be in descending order


def test_rate_primary_user():
    channelGain_Primary, channelGain_Secondary = valuesGen.generate_channel(
        s, sigma, N_users, x_u, y_u, x_r, y_r, path_loss_exp, z_r
    )
    power_Primary = np.max(valuesGen.generate_power_coeff(N_users))
    power_Secondary = np.min(valuesGen.generate_power_coeff(N_users))
    rate_pri = valuesGen.calculate_instantaneous_rate_primary(
        channelGain_Primary,
        channelGain_Secondary,
        snr_values_dB,
        power_Primary,
        power_Secondary,
        target_rate_primary_user,
    )
    assert rate_pri.all() >= 0  # Non-negative


def test_rate_secondary_user():
    channelGain_Secondary = np.min(
        valuesGen.generate_channel(
            s, sigma, N_users, x_u, y_u, x_r, y_r, path_loss_exp, z_r
        )
    )
    power_Secondary = np.min(valuesGen.generate_power_coeff(N_users))
    rate_sec = valuesGen.calculate_instantaneous_rate_secondary(
        channelGain_Secondary, snr_values_dB, power_Secondary
    )
    assert rate_sec.all() > 0  # Non-negative


def test_data_main():
    (
        out_probability_system,
        out_probability_primary_user,
        out_probability_secondary_user,
        instantaneous_rate_primary,
        instantaneous_rate_secondary,
        average_rate, 
        snr_dB,
    ) = mainStructure.main_values()
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
    assert instantaneous_rate_primary.all() >= 0, "Invalid, must be non-negative."
    assert instantaneous_rate_secondary.all() >= 0, "Invalid, must be non-negative."
    assert average_rate.all() >= 0, "Invalid, must be non-negative."
    assert snr_dB.all() >=0, "Invalid, must be non-negative."