#!/usr/bin/env python
""" 
    This archive is for plotting the values of the achievable rate and outage probability.

"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import uavnoma

parser = argparse.ArgumentParser(description='Simulation parameters.')
parser.add_argument('monte_carlo_samples', type=int,
                    help='Monte Carlo samples')
parser.add_argument('power_los', type=float,
                    help='power of Line-of-Sigth path & scattered paths (1<= power_los <= 2)')
parser.add_argument('rician_factor', type=int,
                    help='Rician factor value (10<= rician_factor <= 15)')
parser.add_argument('path_loss', type=float,
                    help='Path loss exponent (2 <= path_loss <= 3)')
parser.add_argument('radius_uav', type=float,
                    help='Radius fly trajectory of the UAV in meters')     
parser.add_argument('radius_user', type=float,
                    help='Distribution radius of users in the cell in meters')     
parser.add_argument('uav_heigth_mean', type=float,
                    help='Average UAV flight height') 
parser.add_argument('target_rate_primary_user', type=float,
                    help='Target rate bits/s/Hertz  primary user') 
parser.add_argument('target_rate_secondary_user', type=float,
                    help='Target rate bits/s/Hertz  secondary user') 
parser.add_argument('hardw_ip', type=float,
                    help='Residual Hardware Impairments coefficient 0 <= hardw_ip <=1') 
parser.add_argument('sic_ip', type=float,
                    help='Residual Imperfect SIC coefficient 0 <= sic_ip <=1') 
parser.add_argument('number_user', type=int,
                    help='Number of users must be 2') 
parser.add_argument('number_uav', type=int,
                    help='Number of UAV must be 1')                     
parser.add_argument('power_coeff_primary', type=float,
                    help='The value of power coefficient allocation of the Primary User')  
parser.add_argument('power_coeff_secondary', type=float,
                    help='The value of power coefficient allocation of the Secondary User:')  

args = parser.parse_args( ['10000', '1.0', '15', '2.2', '2.0', '10.0','15.0', '0.5','0.5','0.0', '0.0','2','1', '0.8','0.2'] )


# Initialization of some auxiliary arrays
snr_dB = np.array(range(10, 61, 2)) # SNR in dB
snr_linear = 10.0 ** (snr_dB / 10.0)  # SNR linear
out_probability_system = np.zeros((args.monte_carlo_samples, len(snr_dB)))
out_probability_secondary_user = np.zeros((args.monte_carlo_samples, len(snr_dB)))
out_probability_primary_user = np.zeros((args.monte_carlo_samples, len(snr_dB)))
system_average_rate = np.zeros((args.monte_carlo_samples, len(snr_dB)))
rate_secondary_user = np.zeros((args.monte_carlo_samples, len(snr_dB)))
rate_primary_user = np.zeros((args.monte_carlo_samples, len(snr_dB)))


# ------------------------------------------------------------------------------------
# Fixed power allocation
#power_coeff_primary = float(input('Enter the value of power coefficient allocation of the Primary User: ')) 
#power_coeff_secondary = 1 - power_coeff_primary
assert (
    args.power_coeff_primary >= args.power_coeff_secondary
),  "The power coefficient of the primary user must be greater than that of the Secondary user."

sum_power = args.power_coeff_primary + args.power_coeff_secondary
assert (sum_power > 0) and (
    sum_power <= 1
) , "The sum of the powers must be > 0 or <= 1."

        
for mc in range(args.monte_carlo_samples):
    # Position UAV and users
    uav_axis_x, uav_axis_y, uav_heigth = uavnoma.random_position_uav(args.number_uav, args.radius_uav, args.uav_heigth_mean)
    user_axis_x, user_axis_y = uavnoma.random_position_users(args.number_user, args.radius_user)

    s, sigma = uavnoma.fading_rician(args.rician_factor, args.power_los)

    # Generate channel gains
    channel_gain_primary, channel_gain_secondary =  uavnoma.generate_channel(
        s,
        sigma,
        args.number_user,
        user_axis_x,
        user_axis_y,
        uav_axis_x,
        uav_axis_y,
        uav_heigth,
        args.path_loss,
    )

    # Analyzes system performance metrics for various SNR values
    for sn in range(0, len(snr_dB)):

        # Calculating achievable rate of primary user
        rate_primary_user[mc, sn] = uavnoma.calculate_instantaneous_rate_primary(
            channel_gain_primary,
            snr_linear[sn],
            args.power_coeff_primary,
            args.power_coeff_secondary,
            args.hardw_ip,
        )
        # Calculating achievable rate of secondary user
        rate_secondary_user[mc, sn] = uavnoma.calculate_instantaneous_rate_secondary(
            channel_gain_secondary,
            snr_linear[sn],
            args.power_coeff_secondary,
            args.power_coeff_primary,
            args.hardw_ip,
            args.sic_ip,
        )

        system_average_rate[mc, sn] = uavnoma.average_rate(rate_primary_user[mc, sn], rate_secondary_user[mc, sn])
        
        # Calculating of outage probability of the system
        out_probability_system[mc, sn], out_probability_primary_user[mc, sn], out_probability_secondary_user[mc, sn] = uavnoma.outage_probability(
            rate_primary_user[mc, sn],
            rate_secondary_user[mc, sn], 
            args.target_rate_primary_user,
            args.target_rate_secondary_user,
        )

# Outage Probability
out_prob_mean = np.mean(
    out_probability_system, axis=0
)  # Outage probability of the System
out_prob_primary = np.mean(
    out_probability_primary_user, axis=0
)  # Outage probability of the Primary User
out_prob_secondary = np.mean(
    out_probability_secondary_user, axis=0
)  # Outage probability of the Secondary User

# Achievable Rate
average_rate_mean = np.mean(
    system_average_rate, axis=0
)  # Average achievable rate of the system
rate_mean_primary_user = np.mean(
    rate_primary_user, axis=0
)  # Average achievable rate of the Primary User
rate_mean_secondary_user = np.mean(
    rate_secondary_user, axis=0
)  # Average achievable rate of the Secondary User


print("Outage probability system:", out_prob_mean)
print("Average Achievable Rate of the System:", average_rate_mean)
print("Achievable Rate of the Primary user:", rate_primary_user)
print("Achievable Rate of the Secondary user:", rate_secondary_user)


# Saving outage probability values in .txt
print('Outage probability system:', out_prob_mean, '\n\nOutage probability primary user:', out_prob_primary, '\n\nOutage probability secondary user:', out_prob_secondary, file=open("./uavnoma/txt/outage_prob_values.txt", "w"))

# Saving achievable rate values in .txt
print(' Average Achievable Rate of the System:', average_rate_mean, '\n\nAverage achievable rate of the Primary User:', rate_mean_primary_user, '\n\nAverage achievable rate of the Secondary User:', rate_mean_secondary_user, file=open("./uavnoma/txt/achievable_rate_values.txt", "w"))

# --------------------- FIGURES -----------------------------
plot = "yes" 
if plot == "yes":
    # Outage probability
   # plt.semilogy(snr_dB, out_prob_mean, "go-", label="System", linewidth=2)
    plt.semilogy(snr_dB, out_prob_primary, "b.-", label="Primary user", linewidth=1)
    plt.semilogy(snr_dB, out_prob_secondary, "r.-", label="Secondary user", linewidth=1)
    plt.xlabel("SNR (dB)")
    plt.ylabel("Outage Probability")
    plt.legend(loc="lower left")
    plt.xlim(10, 40)

    # Average Achievable Rate of the users
    plt.figure()
    plt.plot(snr_dB, rate_mean_primary_user, "b.-", label="primary user", linewidth=1)
    plt.plot(
        snr_dB, rate_mean_secondary_user, "r.-", label="secondary user", linewidth=1
    )
    plt.xlim(10, 60)
    plt.xlabel("SNR (dB)")
    plt.ylabel("Achievable rate (bits/s/Hz)")
    plt.legend(loc="upper left")

    plt.show()
    