#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
   Numerical Simulation of UAV-NOMA System under non-ideal conditions.
   
   A Python 3.9 implementation of a model of wireless communication 
   system between an area base station and two users. 
   Initially, power allocation is employed manually.

   .. include:: ./doc/documentation.md

"""


import random
import numpy as np
from numpy import sqrt
import math
import matplotlib.pyplot as plt

class valuesGen:
    def __init__(self):
        pass

    def init_parameters():
        """
        Generates some simulation parameter.
        The user can modify the parameters to analyze the system performance
        """

        samples_mc = 10000  # Monte Carlo samples
        print(
            "The greater the number of samples, the more computational time is required."
        )
        assert (
            10000 <= samples_mc <= 1000000
        ), "Invalid quantity, the value entered must be 10000<=samples_mc <= 1000000."

        number_users = 2
        assert number_users == 2, "Number of users must be 2."

        power_los = 1.0
        assert (
            power_los == 1.0 or power_los == 2.0
        ), "Invalid power of Line-of-Sigth path & scattered paths."

        rician_factor = 6
        assert (
            rician_factor >= 0 and rician_factor <= 10
        ), "Invalid Rician factor, the value must be (0<= value <= 10)"

        path_loss_value = 2  # Path loss exponent
        number_uav = 1  # Number of UAVs
        assert number_uav == 1, "Number of UAV must be 1."

        radius_value_uav = 1.0  # Fly trajectory of the UAV in meters
        radius_value_user = 2.0  # Distribution radius of users in the cell in meters.
        # Users' Target Rate
        rate_value_primary_user = 0.5  # Target rate bits/s/Hertz  primary user
        rate_value_secondary_user = 0.5  # Target rate bits/s/Hertz  secondary users
        snr_values_dB = np.array(range(10, 41, 2))  # SNR in dB
        snr_values_linear = 10 ** (snr_values_dB / 10)  # SNR linear

        coeffHard = 0.05 # Residual Hardware Impairments
        coeffSic = 0.05  # Residual Imperfect SIC

        return (
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
            coeffHard,
            coeffSic,
        )

    def generate_power_coeff(n_users):
        """Returns the power coefficient allocation of the users.

        Arguments:

            n_user -- number of users.

        Return:

            data_power_Pri --  power coefficients of the Primary users.

            data_power_Sec --  power coefficients of the Secondary users.
        """

        print(
            "WARNING: The sum of powers must be: [0 <sum(power) <= 1], \n AND the power of the primary user must be greater than that of the secondary in order for their QoS to be satisfied. E.g. user_1 = 0.8 and user_2 =0.2.\n"
        )
        # ('Enter the value of power coefficient allocation of the Primary User:  ')
        data_power_Pri = 0.6  # float(input('-> '))
        # ('Enter the value of power coefficient allocation of the Secondart User:  ')
        data_power_Sec = 0.4  # float(input('--> '))

        return data_power_Pri, data_power_Sec

    def random_position_uav(numberUAV, radiusUAV):
        """Returns a random UAV position based on 3D Cartesian coordinates.

                x_r: x-axis | y_r: y-axis | z_r: heigth

        `theta_r:` randomly generates an angle

        `rho_r:` radius in meter of fly trajectory UAV

        `rho_u:` radius in meter of the area where users are distributed

        Arguments:

            numberUAV -- number of UAV.

            radiusUAV -- fly trajectory of the UAV in meters.

        Return:

            x_r, y_r, z_r -- position in the x-axis, y-axis and heigth of the UAV.
        """
        theta_r = np.random.rand(numberUAV, 1) * (math.pi * 2)
        rho_r = radiusUAV
        x_r = rho_r * np.cos(theta_r)
        y_r = rho_r * np.sin(theta_r)
        z_r = 20.0
        return x_r, y_r, z_r

    def random_position_users(numberUsers, radiusUser):
        """Returns a random ground users position based on 2D Cartesian coordinates.

                x_u: x-axis |  y_u: y-axis | height is not considered

        `theta_u:` randomly generates an angle

        `rho_u:` radius in meter of the area where users are distributed

        Arguments:

            numberUsers -- number of users.

            radiusUser -- distribution radius of users in the cell in meters.

        Return:

            x_u, y_u -- position in the x-axis and y-axis of the n-th user.

        """
        theta_u = (np.random.rand(numberUsers, 1)) * (math.pi * 2)
        rho_u = np.sqrt(np.random.rand(numberUsers, 1)) * radiusUser
        x_u = rho_u * np.cos(theta_u)
        y_u = rho_u * np.sin(theta_u)
        return x_u, y_u

    def generate_channel(
        s, sigma, numberUser, user_X, user_Y, uav_X, uav_Y, path_loss, uav_Z
    ):
        """Returns the sorting channel gains of the users over Rician Fading. The channel gains are sorted to identify
        the primary user and secondary user.

        `ch_coeff:` calculating channel coefficients with Random Variable Rice of mean=s and variance=sigma.

        `distance:` calculating distance between UAV and users.

        `h_n:` calculates channel coefficients based on the distance.

        `channelGain:` calculates the channel gains and sorting in descending order.

            Primary user:  channelGain[0]   -> max value

            Secondary user:  channelGain[1] -> min value

        Arguments:

            s -- non-Centrality Parameter (mean).

            sigma -- standard deviation.

            numberUser -- number of user.

            user_X -- position axis x of n-th user.

            user_Y -- position axis y of n-th user.

            uav_X -- position axis x of UAV.

            uav_Y -- position axis y of UAV.

            path_loss -- path loss exponent.

            uav_z -- UAV heigth.

        Return:

            channelGain -- sorted channel gain of the users.

        """
        # Initializing auxiliary arrays to store channel coefficients and distance between UAV and users, respectively:
        h_n = np.zeros(numberUser)
        distance = np.zeros(numberUser)
        for uu in range(numberUser):

            ch_coeff = np.sqrt(
                (np.random.normal(s, sigma) ** 2)
                + 1j * (np.random.normal(0, sigma) ** 2)
            )
            distance[uu] = np.sqrt(
                (user_X[uu] - uav_X) ** 2 + (user_Y[uu] - uav_Y) ** 2 + uav_Z ** 2
            )
            h_n[uu] = (
                np.abs(ch_coeff / np.complex(sqrt(1 + (distance[uu]) ** path_loss), 0))
                ** 2
            )

        channelGain = sorted(h_n, reverse=True)
        return channelGain

    def calculate_instantaneous_rate_primary(
        channelPri, channelSec, snrValues, powerPrimary, powerSecondary, target_RatePri, coeffHard, coeffSic,
    ):
        """Returns the instantaneous achievable rate of the primary user for all values of SNR in dB.

        `sinr_primary:` generates the Signal-to-interference-plus-noise ratio (SINR) experienced by the primary user based on NOMA.

        `inst_rate_primary:` calculates instantaneous rate of the primary user based on sinr_primary.

        If the calculated instantaneous rate does not reach the rate desired by the user, OMA is used in order to guarantee
        the Quality-of-Service requirements.

        Arguments:

            channelPri -- channel gain of the primary user

            channelSec -- channel gain of the secondary user.

            snrValues -- linear SNR values.

            powerPrimary --  power coefficient allocated to the Primary user.

            powerSecondary --  power coefficient allocated to the Secondary user.

            target_RatePri -- target rate of the primary user.

        Return:

            inst_rate_primary -- instantaneous achievable rate of the primary user.
        """
        sinr_primary = np.zeros(
            (len(snrValues))
        )  # Initializating auxiliary array of Signal-to-interference-plus-noise ratio experienced by the primary user.
        inst_rate_primary = np.zeros((len(snrValues)))
        for sn in range(0, len(snrValues)):

            sinr_primary[sn] = (snrValues[sn] * channelPri * powerPrimary) / (
                snrValues[sn] * channelSec * ( powerSecondary + coeffHard**2  ) + 1
            )
            inst_rate_primary[sn] = np.log(
                1 + sinr_primary[sn]
            )  # Instantaneous achievable rate of primary user NOMA
            '''
            if inst_rate_primary[sn] < target_RatePri:
                sinr_primary[sn] = snrValues[sn] * channelPri
                inst_rate_primary[sn] = 0.5 * np.log(
                    1 + sinr_primary[sn]
                )  # Instantaneous achievable rate of primary user OMA'''
        return inst_rate_primary

    def calculate_instantaneous_rate_secondary(channelSec, snrValues, powerSecondary, powerPrimary, coeffHard, coeffSic):
        """Returns the instantaneous achievable rate of the secondary user for all values of SNR in dB.

        `sinr_secondary:` generates the Signal-to-interference-plus-noise ratio (SINR) experienced by the secondary user based on NOMA.

        `inst_rate_secondary:` calculates instantaneous rate of the secondary user based on sinr_secondary.


        Arguments:

            channelSec -- channel gain of the secondary user.

            snrValues -- linear SNR values.

            powerSecondary --  power coefficient allocated to the Secondary user.

        Return:

            inst_rate_secondary -- instantaneous achievable rate of the secondary user.
        """
        sinr_secondary = np.zeros(
            (len(snrValues))
        )  # Initializating auxiliary arrays of Signal-to-interference-plus-noise ratio experienced by the secondary user.
        inst_rate_secondary = np.zeros((len(snrValues)))
        for sn in range(0, len(snrValues)):
            sinr_secondary[sn] = ( snrValues[sn] * channelSec * powerSecondary ) / (
                snrValues[sn] * channelSec * ( powerPrimary*coeffSic + coeffHard**2 ) + 1
            )
            inst_rate_secondary[sn] = np.log(
                1 + sinr_secondary[sn]
            )  # Instantaneous achievable rate of secondary user

        return inst_rate_secondary


class mainStructure():
    def __init__(self):
        pass

    def main_values():
        """Calculates the  outage probability and achievable rate.

        Returns:

            out_probability_system -- outage probability of the system.
            
            out_probability_primary_user -- outage probability of the primary user.
            
            out_probability_secondary_user -- outage probability of the secondary user.
            
            instantaneous_rate_primary -- achievable rate of the primary user.
            
            instantaneous_rate_secondary -- achievable rate of the secondary user.
            
            average_rate -- average achievable rate of the system.
            
            snr_dB -- SNR values in dB.
        """
        # --------------- Parameters ---------------
        (
            N_mc,
            N_users,
            P_los,
            K,
            path_loss_exp,
            M_uav,
            snr_dB,
            snr_linear,
            radius_uav,
            radius_user,
            target_rate_primary_user,
            target_rate_secondary_user,
            hardw_ip,
            sic_ip,
        ) = valuesGen.init_parameters()
        powerCoeffPrimary, powerCoeffSecondary = valuesGen.generate_power_coeff(N_users)

        # Fading modeled by Rician distribution
        s = np.sqrt(K / (K + 1) * P_los)  # Non-Centrality Parameter (mean)
        assert s >= 0  # Non-negative
        sigma = P_los / np.sqrt(2 * (K + 1))  # Standard deviation
        assert s >= 0  # Non-negative


        # Initialization of some auxiliary arrays
        out_probability_system = np.zeros((N_mc, len(snr_dB)))
        out_probability_secondary_user = np.zeros((N_mc, len(snr_dB)))
        out_probability_primary_user = np.zeros((N_mc, len(snr_dB)))
        average_rate = np.zeros((N_mc, len(snr_dB)))
        instantaneous_rate_secondary = np.zeros((N_mc, len(snr_dB)))
        instantaneous_rate_primary = np.zeros((N_mc, len(snr_dB)))

        # ------------------------------------------------------------------------------------
        for mc in range(N_mc):
            # Position
            uav_AxisX, uav_AxisY, uav_heigth = valuesGen.random_position_uav(M_uav, radius_uav)
            user_AxisX, user_AxisY = valuesGen.random_position_users(N_users, radius_user)

            # Generate channel gains
            channelGainPrimary = np.max(
                valuesGen.generate_channel(
                    s,
                    sigma,
                    N_users,
                    user_AxisX,
                    user_AxisY,
                    uav_AxisX,
                    uav_AxisY,
                    path_loss_exp,
                    uav_heigth,
                )
            )
            channelGainSecondary = np.min(
                valuesGen.generate_channel(
                    s,
                    sigma,
                    N_users,
                    user_AxisX,
                    user_AxisY,
                    uav_AxisX,
                    uav_AxisY,
                    path_loss_exp,
                    uav_heigth,
                )
            )

            # Calculating achievable rate of each user
            instantaneous_rate_primary[mc, :] = valuesGen.calculate_instantaneous_rate_primary(
                channelGainPrimary,
                channelGainSecondary,
                snr_linear,
                powerCoeffPrimary,
                powerCoeffSecondary,
                target_rate_primary_user,
                hardw_ip,
                sic_ip,
            )
            instantaneous_rate_secondary[
                mc, :
            ] = valuesGen.calculate_instantaneous_rate_secondary(
                channelGainSecondary,
                snr_linear,
                powerCoeffSecondary,
                powerCoeffPrimary,
                hardw_ip,
                sic_ip,
            )

            for sn in range(0, len(snr_dB)):
                # Calculating of outage probability of the system
                if (instantaneous_rate_primary[mc, sn] < target_rate_primary_user) or (
                    instantaneous_rate_secondary[mc, sn] < target_rate_secondary_user
                ):
                    out_probability_system[mc, sn] = 1
                else:
                    out_probability_system[mc, sn] = 0

                # Calculating of outage probability of the primary user
                if instantaneous_rate_primary[mc, sn] < target_rate_primary_user:
                    out_probability_primary_user[mc, sn] = 1
                else:
                    out_probability_primary_user[mc, sn] = 0

                # Calculating of outage probability of the secondary user
                if instantaneous_rate_secondary[mc, sn] < target_rate_secondary_user:
                    out_probability_secondary_user[mc, sn] = 1
                else:
                    out_probability_secondary_user[mc, sn] = 0

                # Calculating of average achievable rate of the system
                average_rate[mc, sn] = (
                    instantaneous_rate_primary[mc, sn]
                    + instantaneous_rate_secondary[mc, sn]
                ) / 2  # Average achievable rate in bits/s/Hz
        return (
            out_probability_system,
            out_probability_primary_user,
            out_probability_secondary_user,
            instantaneous_rate_primary,
            instantaneous_rate_secondary,
            average_rate,
            snr_dB,
        )

    