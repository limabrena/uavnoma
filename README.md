## Power Allocation in UAV-NOMA System with Two-users

A Python 3.9 implementation of the Power Allocation Algorithm for UAV-NOMA System with 2 Users.

Brena Lima.

COPELABS, Lusófona University


-------------------------
### Scenario Description:


We consider a uplink UAV-aided NOMA network, as illustrated in figure below. 
![System model.](pa-uav-noma/figures/UAV_system_model.png)

In this scenario, a UAV is deployed as an air base station that communicates with two-user $$N_1$$ and $$N_2$$.  We consider that each node is equipped with a single antenna and both UAV and users operate in the half-duplex mode.
The system is inspired on cognitive radio (CR) concept to decode the user's messages.
Based on this, the user $$N_1$$ is viewed as the primary user and $$N_2$$ is viewed as secondary user.
In order to guarantee primary user's Quality-of-Service requirements, the UAV first decodes the $$N_1$$'s message.
Then, the UAV decodes the message from the secondary user $$N_2$$ without experiencing any performance degradation due to the primary user.

*Example:*

	`$$N_1$$ may be an Internet of Things (IoT) healthcare device which needs to send health status changes.` 

	`$$N_2$$ an IoT device sending personal tasks records, where the transmission is a delay tolerant.`

Different levels of power coefficients must be allocated to each user's signal, so that users' QoS requirements are satisfied.

----------------
### Requirement:


The implementation requires Python 3.9+ to run.
The following libraries are required:

 - `numpy` 
 - `matplotlib.pyplot`
 - `math`
 - `random`

---------------------------------
### How can use this application? 


- Download:

		$ git clone https://github.com/limabrena/power-allocation-UAV-NOMA-RL-2users.git

		Direct download ZIP in my git repository: limabrena/power-allocation-UAV-NOMA-RL-2users
	  
- Usage: 

	This application can be used as a study tool to understand the 
	behavior of the achievable rate by two users and the influence
	of the allocation of power coefficients in a UAV-NOMA system. 
	The communication model presented is a base of UAV-NOMA principles and 
	can be expanded to several other scenarios, such as massive MIMO, 
	full-duplex communication, and others in order to 
	improve the users' rate performance.
		
	The user can modify parameters and analyze the system's behavior. 
	Based on this, new methods can be proposed to solve trajectory problems, 
	power allocation, decoding order and others.
	
	Example: when the Rician Factor `K=0`, fading is similar to Rayleigh's.
 

-------------------------
### Algorithm description:


Adaptive power allocation algorithm was not implemented in the present version.

