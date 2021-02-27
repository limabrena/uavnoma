#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
   Numerical Simulation of Power allocation in UAV-NOMA System.
   
   A Python 3.9 implementation of a model of wireless communication 
   system between an area base station and two users. 
   Initially, power allocation is employed manually.

   .. include:: ./doc/documentation.md

"""

import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt

# import generate_values as func
# import parameters as init
from pauavnoma.uavnoma import mainStructure as gen

(
    outage_probability_total,
    outage_primary,
    outage_secondary,
    rate_primary,
    rate_secondary,
    average_sum_rate,
    snr_dB,
) = gen.main_values()
# Outage Probability
out_prob_mean = np.mean(
    outage_probability_total, axis=0
)  # Outage probability of the System
out_prob_primary = np.mean(
    outage_primary, axis=0
)  # Outage probability of the Primary User
out_prob_secondary = np.mean(
    outage_secondary, axis=0
)  # Outage probability of the Secondary User
print("Outage probability system:", out_prob_mean)

# Saving outage probability values in .txt
# print('Outage probability system:', out_prob_mean, '\n\nOutage probability primary user:', out_prob_primary, '\n\nOutage probability secondary user:', out_prob_secondary, file=open("pauavnoma/doc/outage_prob_values.txt", "w"))


# Achievable Rate
average_rate_mean = np.mean(
    average_sum_rate, axis=0
)  # Average achievable rate of the system
rate_mean_primary_user = np.mean(
    rate_primary, axis=0
)  # Average achievable rate of the Primary User
rate_mean_secondary_user = np.mean(
    rate_secondary, axis=0
)  # Average achievable rate of the Secondary User
print("Average Achievable Rate of the System:", average_rate_mean)
print("Achievable Rate of the Primary user:", rate_primary)
print("Achievable Rate of the Secondary user:", rate_secondary)


# Saving achievable rate values in .txt
print(' Average Achievable Rate of the System:', average_rate_mean, '\n\nAverage achievable rate of the Primary User:', rate_mean_primary_user, '\n\nAverage achievable rate of the Secondary User:', rate_mean_secondary_user, file=open("pauavnoma/doc/achievable_rate_values.txt", "w"))

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
    plt.xlim(10, 40)
    plt.xlabel("SNR (dB)")
    plt.ylabel("Achievable rate (bits/s/Hz)")
    plt.legend(loc="upper left")

    plt.show()
    