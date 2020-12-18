#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Inteligent PA in NOMA System with Multi-UAV
Copyright for the "main" code:  Brena Lima, 2020

"""
import random
import numpy as np 
from numpy import sqrt
import matplotlib.pyplot as plt
import math
import scipy.stats

# --------------- Paramenters ---------------
N_mc = 10**4  # Monte Carlo samples
N_users = 2       # Number of Users
M_uav = 1        # Number of UAVs
snr_dB = np.array(range(10, 51, 2))     
snr_linear = 10**(snr_dB/10) # SNR linear
path_loss_exp = 2


# Rician Fading
P_los =1.0 # Total power of LOS path & scattered paths
K = 10 # Rician Factor (if K=0, Rayleigh fading)
s=sqrt(K/(K+1)*P_los) # Non-Centrality Parameter (mean)
sigma=P_los/sqrt(2*(K+1)) # Standard deviation

# Users' Target Rate
target_rate_weak_user =0.5  # Target rate bits/s/Hertz  weak user
target_rate_strong_user =1.0  # Target rate bits/s/Hertz  strong users


alpha_u = [0.8, 0.2] # Fixed power factor allocation NOMA
ip_sic = 0.0 # 0.0 <= ip_sic <=1.0  level of imperfect SIC

# Radius
radius_uav = 1.0 # Fly trajectory in the area in meters
radius_user= 2.0 # Distribution of users in the area in meters
z_height = 30.0  # Height UAV in meters

# Initialization of some arrays
rate_us = np.zeros((N_mc,len(snr_dB)))
rate_uw = np.zeros((N_mc,len(snr_dB)))
out_probability= np.zeros((N_mc,len(snr_dB),N_users))
out_probability_system = np.zeros((N_mc,len(snr_dB)))
out_probability_strong_user = np.zeros((N_mc,len(snr_dB)))
out_probability_weak_user = np.zeros((N_mc,len(snr_dB)))
average_rate = np.zeros((N_mc,len(snr_dB)))
inst_rate_strong = np.zeros((N_mc,len(snr_dB)))
inst_rate_weak = np.zeros((N_mc,len(snr_dB)))

#------------------------------------------------------------------------------------

for mc in range(N_mc):
    # Generation random position UAV
    theta_r = (np.random.rand(M_uav,1)*(math.pi*2))
    rho_r = radius_uav
    x_r =  (rho_r*np.cos(theta_r))
    y_r =  (rho_r*np.sin(theta_r))    

    # Generation random position users
    theta_u = (np.random.rand(N_users,1))*(math.pi*2)
    rho_u = (sqrt(np.random.rand(N_users,1))*radius_user)
    x_u =( rho_u*np.cos(theta_u))
    y_u =( rho_u*np.sin(theta_u))
 
  
    # Generation channel coefficients with Rician fading
    h_rn = np.zeros(N_users)
    distance = np.zeros(N_users)
  
    for uu in range(N_users):   
       ch_coeff = np.sqrt( (np.random.normal(s,sigma)**2) + 1j*(np.random.normal(0,sigma)**2) ) # Random Variable Rice with mean=s and variance=sigma
       distance[uu]= sqrt( (x_u[uu]-x_r)**2  + (y_u[uu]-y_r)**2   + z_height**2  )    # Euclidian distance
       h_rn[uu] = np.abs(ch_coeff/np.complex(sqrt(1+(distance[uu])**path_loss_exp),0))**2     # Coefficient channel over distance

    H_rn = np.sort(h_rn) # ordered channel gain
    #------------------------------------------------------------------------------------

    # Initialization of some arrays
    sinr_weak = np.zeros((len(snr_dB))) # Signal for interference and noise ratio experienced by the weak user
    sinr_strong = np.zeros((len(snr_dB))) #Signal for interference and noise ratio experienced by the strong user
    
    #------------------------------------------------------------------------------------

    for sn in range(0,len(snr_dB)):      
       for ii in range(0,N_users): 
          sinr_weak[sn] = (snr_linear[sn]*H_rn[0]*alpha_u[0]) / (snr_linear[sn]*H_rn[0]*alpha_u[1]  + 1)
          inst_rate_weak[mc,sn] = np.log(1+sinr_weak[sn]) # Instantaneous achievable rate of weak user

          sinr_strong[sn] = (snr_linear[sn]*H_rn[1]*alpha_u[1]) / (snr_linear[sn]*H_rn[1]*ip_sic*alpha_u[0]  + 1)
          inst_rate_strong[mc,sn] = np.log(1+sinr_strong[sn]) # Instantaneous achievable rate of strong user
         
          if (inst_rate_weak[mc,sn]  < target_rate_weak_user) or (inst_rate_strong[mc,sn]  < target_rate_strong_user) :
             out_probability_system[mc,sn] = 1
          else:
             out_probability_system[mc,sn] = 0        
     

          if (inst_rate_weak[mc,sn]  < target_rate_weak_user):
             out_probability_weak_user[mc,sn] = 1
          else: 
             out_probability_weak_user[mc,sn] = 0

          if (inst_rate_strong[mc,sn]  < target_rate_strong_user):
             out_probability_strong_user[mc,sn] = 1
          else: 
             out_probability_strong_user[mc,sn] = 0

          average_rate[mc,sn] =(inst_rate_weak[mc,sn]+inst_rate_strong[mc,sn])/2

# Outage Probability Plot

out_prob_mean = np.mean(out_probability_system, axis=0) 
out_prob_weak = np.mean(out_probability_weak_user, axis=0)
out_prob_strong = np.mean(out_probability_strong_user, axis=0)


plt.semilogy(snr_dB, out_prob_mean, 'go-', label="Fixed Power Allocation", linewidth=2)
plt.semilogy(snr_dB, out_prob_weak, 'b.-', label="Weak user", linewidth=1)
plt.semilogy(snr_dB, out_prob_strong, 'r.-', label="Strong user", linewidth=1)

plt.xlabel('SNR (dB)')
plt.ylabel('Outage Probability')
plt.legend(loc="lower left")
plt.xlim(10,50)
#system_out_path = 'C:/Users/breen/Google Drive/PhD Lusofona/Research Software/power-allocation-UAV-NOMA-RL-2users/figures/system_outage_prob.pdf'
#plt.savefig(system_out_path,bbox_inches='tight')

# Saving probability values in .txt
print('Outage probability system:',out_prob_mean,'\n\nOutage probability weak user:', out_prob_weak, '\n\nOutage probability strong user:', out_prob_strong, file=open("outage_prob_values.txt", "w"))


# Average Rate Plot
average_rate_mean = np.mean(average_rate, axis=0)
plt.figure()
plt.plot(snr_dB, average_rate_mean, 'r.-', label="Fixed PA", linewidth=2)
plt.xlim(10,50)
plt.xlabel('SNR (dB)')
plt.ylabel('Average achievable rate (bits/s/Hz)')
plt.legend(loc="upper left")

rate_mean_weak_user = np.mean(inst_rate_weak, axis=0)
rate_mean_strong_user = np.mean(inst_rate_strong, axis=0)
plt.figure()
plt.plot(snr_dB, rate_mean_weak_user, 'b.-', label="Weak user", linewidth=1)
plt.plot(snr_dB, rate_mean_strong_user, 'r.-', label="Strong user", linewidth=1)
plt.xlim(10,50)
plt.xlabel('SNR (dB)')
plt.ylabel('Achievable rate (bits/s/Hz)')
plt.legend(loc="upper left")
plt.show()



