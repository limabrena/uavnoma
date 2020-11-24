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
snr_dB = np.array(range(0, 41, 2))     
snr_linear = 10**(snr_dB/10) # SNR linear
path_loss_exp = 2


# Rician Fading
P_los =1 # Total power of LOS path & scattered paths
K = 10 # Rician Factor (if K=0, Rayleigh fading)
s=sqrt(K/(K+1)*P_los) # Non-Centrality Parameter (mean)
sigma=P_los/sqrt(2*(K+1)) # Standard deviation

# Users' Target Rate
target_rate =[0.5, 1]  # Target rate bits/s/Hertz  users
#R_uw = 0.2 # Target rate  bits/s/Hertz  weak user
#R_t2= 2**(R_us) - 1 
#R_t1= 2**(R_uw) - 1

alpha_u = [0.2,0.8] # coefficient power allocation NOMA
ip_sic = 0 # 0 <= ip_sic <=1  level of imperfect SIC

# Radius
radius_uav = 1 # Fly trajectory in the area
radius_user= 2  # Distribution of users in the area
z_height = 100  # Height UAV


rate_us = np.zeros((N_mc,len(snr_dB)))
rate_uw = np.zeros((N_mc,len(snr_dB)))
out_probability= np.zeros((N_mc,len(snr_dB),N_users))
out_probability_system = np.zeros((N_mc,len(snr_dB)))
out_probability_strong_user = np.zeros((N_mc,len(snr_dB)))
out_probability_weak_user = np.zeros((N_mc,len(snr_dB)))
average_rate = np.zeros((N_mc,len(snr_dB)))

# ----------------------------------------------

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
 
    h_ru = np.zeros(N_users)
    distance = np.zeros(N_users)
    # Generation channel coefficients with Rician fading
    for uu in range(N_users):   
       ch_coeff =(random.gauss(s,sigma)+ 1j*random.gauss(0,sigma)) # Gaussian Random Variables with mean=s and variance=sigma
       #ch_coeff = np.random.normal(s,sigma) + 1j*np.random.normal(0,sigma)
       distance[uu]= sqrt( (x_u[uu]-x_r)**2  + (y_u[uu]-y_r)**2   + z_height**2  )    # Euclidian distance
       h_ru[uu] = ch_coeff/(sqrt((distance[uu])**path_loss_exp))      # Coefficient channel/distance

    H_ru = np.sort(np.abs(h_ru)**0.5) # channel gain
    sinr = np.zeros((len(snr_dB),N_users))
    inst_rate = np.zeros((len(snr_dB),N_users))

    for sn in range(0,len(snr_dB)):      
       for ii in range(0,N_users): 
          sinr[sn,ii] = (snr_linear[sn]*H_ru[ii]*alpha_u[ii]) #/ (snr_linear[sn]*H_ru[ii]*np.sum(alpha_u[ii+1:N_users-1]) + ip_sic*np.sum(alpha_u[0:ii-1])) + 1)
          inst_rate[sn,ii] = np.log(1+sinr[sn,ii])
         
          if (inst_rate[sn,ii]  < target_rate[ii]):
             out_probability[mc,sn,ii] = 1
          else:
             out_probability[mc,sn,ii] = 0
          
       if (N_users==2):    # For just 2 users

          if (inst_rate[sn,0]  < target_rate[0]):
             out_probability_weak_user[mc,sn] = 1

          if (inst_rate[sn,1]  < target_rate[1]):
             out_probability_weak_user[mc,sn] = 1

       if np.sum(out_probability[mc,sn,:]) >= 1: # For multiple users
          out_probability_system[mc,sn] = 1
       else:
          out_probability_system[mc,sn] =0
# Plots
out_prob_mean = np.mean(out_probability_system,axis=0)
plt.plot(snr_dB, out_prob_mean, 'b.-')
plt.yscale('log')
plt.xlabel('SNR (dB)')
plt.ylabel('Outage Probability')
g_path = 'C:/Users/breen/Google Drive/PhD Lusofona/Research Software/project-research-software/out_prob.pdf'
plt.savefig(g_path,bbox_inches='tight')
plt.show()