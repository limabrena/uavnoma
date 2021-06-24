""" 
    This module contains script to calculate performance metrics: achievable rate and outage probability .
   
"""

import numpy as np

def __init__():
    pass

def calculate_instantaneous_rate_primary(
    channelPri, snrValues, powerPrimary, powerSecondary,  hardw_ip):
    """Returns the instantaneous achievable rate of the primary user for each SNR value in linear.

    `sinr_primary:` generates the Signal-to-interference-plus-noise ratio (SINR) experienced by the primary user based on NOMA.

    `inst_rate_primary:` calculates instantaneous rate of the primary user based on sinr_primary.

    If the calculated instantaneous rate does not reach the rate desired by the user, OMA is used in order to guarantee
    the Quality-of-Service requirements.

    Arguments:

        channelPri -- channel gain of the primary user

        snrValues -- linear SNR values.

        powerPrimary --  power coefficient allocated to the Primary user.

        powerSecondary --  power coefficient allocated to the Secondary user.


    Return:

        inst_rate_primary -- instantaneous achievable rate of the primary user.
    """
    sinr_primary = (snrValues * channelPri * powerPrimary) / (
        snrValues * channelPri * ( powerSecondary + hardw_ip**2  ) + 1
    )
    inst_rate_primary = np.log(
        1 + sinr_primary
    )  # Instantaneous achievable rate of primary user NOMA

    return inst_rate_primary

def calculate_instantaneous_rate_secondary(channelSec, snrValues, powerSecondary, powerPrimary, hardw_ip, sic_ip):
    """Returns the instantaneous achievable rate of the secondary user for all values of SNR in dB.

    `sinr_secondary:` generates the Signal-to-interference-plus-noise ratio (SINR) experienced by the secondary user based on NOMA.

    `inst_rate_secondary:` calculates instantaneous rate of the secondary user based on sinr_secondary.


    Arguments:

        channelSec -- channel gain of the secondary user.

        snrValues -- linear SNR values.

        powerSecondary --  power coefficient allocated to the Secondary user.

        powerPrimary -- power coefficient allocated to the Primary user.

        hardw_ip -- hardware impairments coefficient.

        sic_ip -- imperfect SIC coefficient. 

    Return:

        inst_rate_secondary -- instantaneous achievable rate of the secondary user.
    """
        
    sinr_secondary = ( snrValues * channelSec * powerSecondary ) / (
        snrValues * channelSec * ( powerPrimary*sic_ip + hardw_ip**2 ) + 1
    )
    inst_rate_secondary = np.log(
        1 + sinr_secondary
    )  # Instantaneous achievable rate of secondary user

    return inst_rate_secondary

def average_rate(instantaneous_rate_primary,  instantaneous_rate_secondary):
    """Returns the average achievable rate for SNR value in dB.

    Arguments:

        instantaneous_rate_primary -- instantaneous achievable rate of the primary user.

        instantaneous_rate_secondary -- instantaneous achievable rate of the secondary user.

    Return:

        avr_rate -- averagre achievable rate in bits/s/Hz
    """
    # Calculating of average achievable rate of the system
    avr_rate = (
    instantaneous_rate_primary
    + instantaneous_rate_secondary
    ) / 2  # Average achievable rate in bits/s/Hz

    return  avr_rate

def outage_probability(
    instantaneous_rate_primary, 
    instantaneous_rate_secondary, 
    target_rate_primary_user, 
    target_rate_secondary_user,
    ):
    """Returns the outage probability for the system, primary user, and secondary user
    for SNR value in linear.

    Arguments:

        instantaneous_rate_primary -- instantaneous achievable rate of the primary user.

        instantaneous_rate_secondary -- instantaneous achievable rate of the secondary user.

    Return:

        avr_rate -- averagre achievable rate in bits/s/Hz
    """

    if (instantaneous_rate_primary < target_rate_primary_user) or (
        instantaneous_rate_secondary < target_rate_secondary_user
    ):
        out_probability_system = 1
    else:
        out_probability_system = 0

    # Calculating of outage probability of the primary user
    if instantaneous_rate_primary< target_rate_primary_user:
        out_probability_primary_user = 1
    else:
        out_probability_primary_user = 0

    # Calculating of outage probability of the secondary user
    if instantaneous_rate_secondary < target_rate_secondary_user:
        out_probability_secondary_user = 1
    else:
        out_probability_secondary_user = 0

    return out_probability_system, out_probability_primary_user, out_probability_secondary_user
