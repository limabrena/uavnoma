import numpy as np
import math
from pauavnoma.pauavnoma import generate_Channel
from pauavnoma.pauavnoma import calculate_Instantaneous_Rate_Primary
from pauavnoma.pauavnoma import calculate_Instantaneous_Rate_Secondary
from pauavnoma.pauavnoma import generate_power_Coeff

N_users =2
P_los=1.0 # 1.0 or 2.0
K=8  #  0 ~ 10
path_loss_exp = 2
M_uav = 1
radius_uav = 1.0
radius_user = 2.0
target_rate_primary_user = 1
target_rate_secondary_user = 0.5 

theta_r = (np.random.rand(M_uav,1)*(math.pi*2))
rho_r = radius_uav
x_r =  (rho_r*np.cos(theta_r))
y_r =  (rho_r*np.sin(theta_r))
z_r = 30.0

theta_u = (np.random.rand(N_users,1))*(math.pi*2)
rho_u = (np.sqrt(np.random.rand(N_users,1))*radius_user)
x_u = (rho_u*np.cos(theta_u))
y_u = (rho_u*np.sin(theta_u))

s=np.sqrt(K/(K+1)*P_los) # Non-Centrality Parameter (mean)
sigma=P_los/np.sqrt(2*(K+1)) # Standard deviation
snr_values_dB = np.array(range(10, 51, 2))  # SNR in dB
snr_values_linear = 10**(snr_values_dB/10)  # SNR linear

# Testing function of generating power coefficients
def test_power_coeff_sum():
    sum_power = np.sum(generate_power_Coeff(N_users))
    assert (sum_power  > 0 and sum_power)  <=1 # The sum of the powers must be > 0 or <= 1  

def test_power_order():    
    power_Primary, power_Secondary = generate_power_Coeff(N_users)
    assert power_Primary >= power_Secondary # The power coefficient of the primary user must be greater than that of the Secondary user.

def test_channel_gain():
    channelGain_Primary, channelGain_Secondary = generate_Channel(s,sigma,N_users,x_u,y_u,x_r,y_r, path_loss_exp, z_r)
    assert channelGain_Primary >= 0 #Non-negative
    assert  channelGain_Secondary >=0 #Non-negative
    assert channelGain_Primary >= channelGain_Secondary # Must be in descending order

def test_rate_primary_user():
   channelGain_Primary, channelGain_Secondary = generate_Channel(s,sigma,N_users,x_u,y_u,x_r,y_r, path_loss_exp, z_r)
   power_Primary = np.max(generate_power_Coeff(N_users))
   power_Secondary = np.min(generate_power_Coeff(N_users))
   rate_pri = calculate_Instantaneous_Rate_Primary(channelGain_Primary,channelGain_Secondary,snr_values_dB,power_Primary,power_Secondary,target_rate_primary_user)
   assert rate_pri.all()>= 0 # Non-negative

def test_rate_secondary_user():
   channelGain_Secondary = np.min(generate_Channel(s,sigma,N_users,x_u,y_u,x_r,y_r, path_loss_exp, z_r))
   power_Secondary = np.min(generate_power_Coeff(N_users))
   rate_sec = calculate_Instantaneous_Rate_Secondary(channelGain_Secondary,snr_values_dB,power_Secondary)
   assert rate_sec.all() > 0 # Non-negative


