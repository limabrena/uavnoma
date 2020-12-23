#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
   Numerical Simulation of Power allocation in UAV-NOMA System.
   
   A Python 3.9 implementation of a model of wireless communication 
   system between an area base station and two users. 
   Initially, power allocation is employed manually.

   .. include:: ./documentation.md

'''

import random
import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt
import math



# --------------- Paramenters ---------------
def parameters():
   '''Returns the simulation parameters.

      Enter values for each requested parameter. The entered 
      values are tested to check if the parameters are viable.
   '''
   samples_mc = 10000 # Monte Carlo samples
   print("The greater the number of samples, the more computational time is required.")
   assert 10000<=samples_mc <= 1000000, "Invalid quantity, the value entered must be 10000<=samples_mc <= 1000000."

   number_users =2
   assert number_users == 2, "Number of users must be 2."  

   power_los = 1.0
   assert power_los == 1.0 or power_los == 2.0,  "Invalid power of Line-of-Sigth path & scattered paths."
 
   rician_factor = 6 
   assert rician_factor>=0 and rician_factor <=10, "Invalid Rician factor, the value must be (0<= value <= 10)"
   

   path_loss_value = 2 # Path loss exponent
   number_uav = 1      # Number of UAVs
   assert number_uav == 1, "Number of UAV must be 1." 

   radius_value_uav = 1.0 # Fly trajectory of the UAV in meters
   radius_value_user= 2.0 # Distribution radius of users in the cell in meters.
   # Users' Target Rate
   rate_value_primary_user = 1.0  # Target rate bits/s/Hertz  primary user
   rate_value_secondary_user = 0.5  # Target rate bits/s/Hertz  secondary users
   snr_values_dB = np.array(range(10, 51, 2))  # SNR in dB
   snr_values_linear = 10**(snr_values_dB/10)  # SNR linear

   return samples_mc, number_users, power_los, rician_factor, path_loss_value, number_uav, snr_values_dB, snr_values_linear, radius_value_uav, radius_value_user, rate_value_primary_user, rate_value_secondary_user


def generate_power_Coeff(n_users):
   '''Returns the power coefficient allocation of the users.
     Arguments:

         n_user -- number of users. 
    Return:   

         data_power_Pri --  power coefficients of the Primary users.
         data_power_Sec --  power coefficients of the Secondary users.
   '''

   print('WARNING: The sum of powers must be: [0 <sum(power) <= 1], \n AND the power of the primary user must be greater than that of the secondary in order for their QoS to be satisfied. E.g. user_1 = 0.8 and user_2 =0.2.\n')
   #('Enter the value of power coefficient allocation of the Primary User:  ')
   data_power_Pri = 0.8 #float(input('--> '))
  # ('Enter the value of power coefficient allocation of the Secondart User:  ')
   data_power_Sec = 0.2 #float(input('--> '))
      
   return data_power_Pri, data_power_Sec


N_mc, N_users, P_los, K, path_loss_exp, M_uav, snr_dB, snr_linear, radius_uav,  radius_user, target_rate_primary_user, target_rate_secondary_user = parameters()
powerCoeffPrimary, powerCoeffSecondary = generate_power_Coeff(N_users) 

# Fading modeled by Rician distribution
s=np.sqrt(K/(K+1)*P_los) # Non-Centrality Parameter (mean)
sigma=P_los/np.sqrt(2*(K+1)) # Standard deviation


# Initialization of some arrays
out_probability= np.zeros((N_mc,len(snr_dB),N_users))
out_probability_system = np.zeros((N_mc,len(snr_dB)))
out_probability_secondary_user = np.zeros((N_mc,len(snr_dB)))
out_probability_primary_user = np.zeros((N_mc,len(snr_dB)))
average_rate = np.zeros((N_mc,len(snr_dB)))
instantaneous_rate_secondary = np.zeros((N_mc,len(snr_dB)))
instantaneous_rate_primary = np.zeros((N_mc,len(snr_dB)))

#------------------------------------------------------------------------------------

for mc in range(N_mc):

   def random_Position_UAV(numberUAV, radiusUAV):
      ''' Returns a random UAV position based on 3D Cartesian coordinates.

                x_r: x-axis | y_r: y-axis | z_r: heigth

       `theta_r:` randomly generates an angle  

       `rho_r:` radius in meter of fly trajectory UAV


       `rho_u:` radius in meter of the area where users are distributed

        Arguments:

            umberUAV -- number of UAV.
            radiusUAV -- fly trajectory of the UAV in meters. 
       Return:   

            x_r, y_r, z_r -- position in the x-axis, y-axis and heigth of the UAV.
     '''
      theta_r = (np.random.rand(numberUAV,1)*(math.pi*2))
      rho_r = radiusUAV
      x_r =  (rho_r*np.cos(theta_r))
      y_r =  (rho_r*np.sin(theta_r))
      z_r = 30.0
      return x_r, y_r, z_r     

   def random_Position_Users(numberUsers, radiusUser):
      ''' Returns a random ground users position based on 2D Cartesian coordinates. 

               x_u: x-axis |  y_u: y-axis | height is not considered

       `theta_u:` randomly generates an angle  

       `rho_u:` radius in meter of the area where users are distributed

        Arguments:

            numberUsers -- number of users.
            radiusUser -- distribution radius of users in the cell in meters.
       Return:   

            x_u, y_u -- position in the x-axis and y-axis of the n-th user.  

      '''
      theta_u = (np.random.rand(numberUsers,1))*(math.pi*2)
      rho_u = (np.sqrt(np.random.rand(numberUsers,1))*radiusUser)
      x_u = (rho_u*np.cos(theta_u))
      y_u = (rho_u*np.sin(theta_u))
      return x_u, y_u  

   uav_AxisX, uav_AxisY, uav_heigth = random_Position_UAV(M_uav,radius_uav)
   user_AxisX, user_AxisY = random_Position_Users(N_users,radius_user)

   # Initializing auxiliary arrays to store channel coefficients and distance between UAV and users, respectively:
   h_n = np.zeros(N_users)
   distance = np.zeros(N_users)


   def generate_Channel(s,sigma,numberUser,user_X, user_Y, uav_X, uav_Y, path_loss, uav_Z):
     '''Returns the sorting channel gains of the users over Rician Fading. The channel gains are sorted to identify
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
       
     '''
     for uu in range(numberUser):  

         ch_coeff = np.sqrt( (np.random.normal(s,sigma)**2) + 1j*(np.random.normal(0,sigma)**2) )
         distance[uu]= np.sqrt( (user_X[uu]-uav_X)**2  + (user_Y[uu]-uav_Y)**2   + uav_Z**2  )
         h_n[uu] = np.abs(ch_coeff/np.complex(sqrt(1+(distance[uu])**path_loss),0))**2

     channelGain = sorted(h_n, reverse=True)
     return channelGain  

   channelGainPrimary = np.max(generate_Channel(s,sigma,N_users,user_AxisX, user_AxisY, uav_AxisX, uav_AxisY, path_loss_exp, uav_heigth))
   channelGainSecondary = np.min(generate_Channel(s,sigma,N_users,user_AxisX, user_AxisY, uav_AxisX, uav_AxisY, path_loss_exp, uav_heigth))
      
   ''' Initializating auxiliary arrays of: 

      Signal-to-interference-plus-noise ratio experienced by the primary user.

      Signal-to-interference-plus-noise ratio experienced by the secondary user.
   '''    
   sinr_primary= np.zeros((len(snr_dB))) 
   sinr_secondary = np.zeros((len(snr_dB))) 
   inst_rate_primary = np.zeros((len(snr_dB))) 
   inst_rate_secondary = np.zeros((len(snr_dB))) 

   def calculate_Instantaneous_Rate_Primary(channelPri,channelSec,snrValuesdB,powerPrimary,powerSecondary,target_RatePri):
      '''Returns the instantaneous achievable rate of the primary user for all values of SNR in dB.

         `sinr_primary:` generates the Signal-to-interference-plus-noise ratio (SINR) experienced by the primary user based on NOMA.

         `inst_rate_primary:` calculates instantaneous rate of the primary user based on sinr_primary.

               If the calculated instantaneous rate does not reach the rate desired by the user, OMA is used in order to guarantee 
               the Quality-of-Service requirements. 
 
        Arguments:

            channelPri -- channel gain of the primary user
            channelSec -- channel gain of the secondary user.
            snrValuesdB -- SNR values in dB.
            powerPrimary --  power coefficient allocated to the Primary user.
            powerSecondary --  power coefficient allocated to the Secondary user.
            target_RatePri -- target rate of the primary user.
       Return:   
            
            inst_rate_primary -- instantaneous achievable rate of the primary user.
      '''
      for sn in range(0,len(snrValuesdB)):    

         sinr_primary[sn] = (snr_linear[sn]*channelPri*powerPrimary) / (snr_linear[sn]*channelSec*powerSecondary  + 1)
         inst_rate_primary[sn] = np.log(1+sinr_primary[sn]) # Instantaneous achievable rate of primary user NOMA

         if inst_rate_primary[sn] < target_RatePri: 
            sinr_primary[sn] = (snr_linear[sn]*channelPri)
            inst_rate_primary[sn] = 0.5*np.log(1+sinr_primary[sn]) # Instantaneous achievable rate of primary user OMA
      return inst_rate_primary

   def calculate_Instantaneous_Rate_Secondary(channelSec,snrValues,powerSecondary):
      '''Returns the instantaneous achievable rate of the secondary user for all values of SNR in dB.

         `sinr_secondary:` generates the Signal-to-interference-plus-noise ratio (SINR) experienced by the secondary user based on NOMA.

         `inst_rate_secondary:` calculates instantaneous rate of the secondary user based on sinr_secondary.
 
 
        Arguments:

            channelSec -- channel gain of the secondary user.
            snrValues -- SNR values in dB.
            powerSecondary --  power coefficient allocated to the Secondary user.
       Return:   
            
            inst_rate_secondary -- instantaneous achievable rate of the secondary user.   
      '''

      for sn in range(0,len(snrValues)):    
         sinr_secondary[sn] = (snr_linear[sn]*channelSec*powerSecondary)
         inst_rate_secondary[sn] = np.log(1+sinr_secondary[sn]) # Instantaneous achievable rate of secondary user

      return inst_rate_secondary

   instantaneous_rate_primary[mc,:] = calculate_Instantaneous_Rate_Primary(channelGainPrimary, channelGainSecondary, snr_dB, powerCoeffPrimary, powerCoeffSecondary, target_rate_primary_user)
   instantaneous_rate_secondary[mc,:] = calculate_Instantaneous_Rate_Secondary(channelGainSecondary, snr_dB, powerCoeffSecondary)
  
    
   for sn in range(0,len(snr_dB)):  
      # Calculating of outage probability of the system
      if (instantaneous_rate_primary[mc,sn]  < target_rate_primary_user) or (instantaneous_rate_secondary[mc,sn]  < target_rate_secondary_user) :
         out_probability_system[mc,sn] = 1
      else:
         out_probability_system[mc,sn] = 0      

      # Calculating of outage probability of the primary user
      if (instantaneous_rate_primary[mc,sn]  < target_rate_primary_user):
         out_probability_primary_user[mc,sn] = 1
      else: 
         out_probability_primary_user[mc,sn] = 0

      # Calculating of outage probability of the secondary user
      if (instantaneous_rate_secondary[mc,sn]  < target_rate_secondary_user):
         out_probability_secondary_user[mc,sn] = 1
      else: 
         out_probability_secondary_user[mc,sn] = 0

      # Calculating of average achievable rate  of the system
      average_rate[mc,sn] = (instantaneous_rate_primary[mc,sn]+instantaneous_rate_secondary[mc,sn])/2 # Average achievable rate in bits/s/Hz

#------- FIGURES --------


# Outage Probability 

out_prob_mean = np.mean(out_probability_system, axis=0) # Outage probability of the System
out_prob_primary = np.mean(out_probability_primary_user, axis=0) # Outage probability of the Primary User
out_prob_secondary = np.mean(out_probability_secondary_user, axis=0) # Outage probability of the Secondary User
print('Outage probability system:', out_prob_mean)

#Saving outage probability values in .txt
#print('Outage probability system:', out_prob_mean, '\n\nOutage probability primary user:', out_prob_primary, '\n\nOutage probability secondary user:', out_prob_secondary, file=open("pa-uav-noma/outage_prob_values.txt", "w"))


# Achievable Rate 
average_rate_mean = np.mean(average_rate, axis=0) # Average achievable rate of the system
rate_mean_primary_user = np.mean(instantaneous_rate_primary, axis=0) # Average achievable rate of the Primary User
rate_mean_secondary_user = np.mean(instantaneous_rate_secondary, axis=0) # Average achievable rate of the Secondary User
print('Average Achievable Rate of the System:', average_rate_mean)


# Saving achievable rate values in .txt
#print(' Average Achievable Rate of the System:', average_rate_mean, '\n\nAverage achievable rate of the Primary User:', rate_mean_primary_user, '\n\nAverage achievable rate of the Secondary User:', rate_mean_secondary_user, file=open("pa-uav-noma/achievable_rate_values.txt", "w"))

# To plot the figures, the comments below need to be removed.
'''

plt.semilogy(snr_dB, out_prob_mean, 'go-', label="System", linewidth=2)
plt.semilogy(snr_dB, out_prob_primary, 'b.-', label="Primary user", linewidth=1)
plt.semilogy(snr_dB, out_prob_secondary, 'r.-', label="Secondary user", linewidth=1)
plt.xlabel('SNR (dB)')
plt.ylabel('Outage Probability')
plt.legend(loc="lower left")
plt.xlim(10,50)




# Average Achievable Rate 

plt.figure()
plt.plot(snr_dB, average_rate_mean, 'r.-', label="Fixed PA", linewidth=2)
plt.xlim(10,50)
plt.xlabel('SNR (dB)')
plt.ylabel('Average achievable rate (bits/s/Hz)')
plt.legend(loc="upper left")


plt.figure()
plt.plot(snr_dB, rate_mean_primary_user, 'b.-', label="primary user", linewidth=1)
plt.plot(snr_dB, rate_mean_secondary_user, 'r.-', label="secondary user", linewidth=1)
plt.xlim(10,50)
plt.xlabel('SNR (dB)')
plt.ylabel('Achievable rate (bits/s/Hz)')
plt.legend(loc="upper left")


plt.show()

'''