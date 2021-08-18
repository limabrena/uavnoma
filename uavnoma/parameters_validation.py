import sys
import numpy as np


def validation(args):

    if ( args.monte_carlo_samples < 100 or args.monte_carlo_samples > 100000 ):
        print("Invalid Monte Carlo samples, the value must be (100 <= monte_carlo_samples <= 100000)", file=sys.stderr)
        sys.exit(1)

    if (args.power_los < 1.0 or args.power_los > 2.0 ):
        print("Error Detected! The power must be (1.0 <= value <= 2.0)", file=sys.stderr)
        sys.exit(1)

    if (args.rician_factor < 10.0 or args.rician_factor > 18.0):
        print("Error Detected! Rician factor must be (10 <= value <= 18)", file=sys.stderr)
        sys.exit(1)

    if (args.path_loss < 2.0 or args.path_loss > 3.0):
        print("Error Detected! Path loss value must be (2.0 <= value <= 3.0)", file=sys.stderr)
        sys.exit(1)

    if (args.radius_uav < 1 or args.radius_uav > 5.0):
        print("Error Detected! Radius UAV value must be (1.0 <= value <= 5.0)", file=sys.stderr)
        sys.exit(1)

    if (args.radius_user < 1 or args.radius_user > 20.0):
        print("Error Detected! Radius user value must be (1.0 <= value <= 20.0)", file=sys.stderr)
        sys.exit(1)

    if (args.uav_height_mean < 10 or args.uav_height_mean > 50):
        print("Error Detected! Heigth UAV value must be (10 <= value <= 40)", file=sys.stderr)
        sys.exit(1)

    if (args.number_user != 2):
        print("Error Detected! Number of user value must be 2)", file=sys.stderr)
        sys.exit(1)

    if (args.number_uav !=1):
        print("Error Detected! Number UAV value must be 1", file=sys.stderr)
        sys.exit(1)

    if (args.target_rate_primary_user < 0 or args.target_rate_primary_user > 2):
        print("Error Detected! Target rate of primary user must be (0.1<= value <= 2)", file=sys.stderr)
        sys.exit(1)

    if (args.target_rate_secondary_user < 0 or args.target_rate_secondary_user > 2):
        print("Error Detected! Target rate of secondary user must be (0.1 <= value <= 2)", file=sys.stderr)
        sys.exit(1)

    if (args.hardw_ip < 0 or args.hardw_ip > 1):
        print("Error Detected! Residual Hardware impairment must be (0 <= value <= 1.0)", file=sys.stderr)
        sys.exit(1)

    if (args.sic_ip < 0 or args.sic_ip > 1):
        print("Error Detected! Residual imperfect SIC must be (0 <= value <= 1.0)", file=sys.stderr)
        sys.exit(1)

    if (args.snr_min < 0 or args.snr_min > 15):
        print("Error Detected! SNR minimum value must be (0 <= value <= 15)", file=sys.stderr)
        sys.exit(1)

    if (args.snr_max < 30 or args.snr_max > 80):
        print("Error Detected! SNR maximum value must be (30 <= value <= 80)", file=sys.stderr)
        sys.exit(1)

    if (args.power_coeff_primary < args.power_coeff_secondary):
        print("Error Detected! The power coefficient of the primary user must be greater than that of the Secondary user.", file=sys.stderr)
        sys.exit(1)

    sum_power = args.power_coeff_primary + args.power_coeff_secondary
    if(sum_power < 0.0 or  sum_power > 1.0 ):
        print("Error Detected! The sum of the power coefficients must be (0.0 < value <= 1.0)", file=sys.stderr)
        sys.exit(1)
    # If a seed was defined, set it
    if (args.seed != None):
        np.random.seed(args.seed)

    return args