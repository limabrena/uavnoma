"""
Tests for the command line script.
"""
import pytest
import numpy as np
import tempfile
import os
from unittest.mock import patch

# Script name
script_name = 'uavnoma'

# Valid parameters, for testing one or two of them at a time
# Here we use both short and long forms
data_params_valid_individual = [
    (['-h']),     # Request for help is a valid input
    (['--help']), # Request for help is a valid input
    ([]),         # No parameters is valid input
    (['-s', str(100)]),
    (['--monte-carlo-samples', str(200)]),
    (['-p', str(1.0)]),
    (['--power-los', str(1.1)]),
    (['-f', str(15.0)]),
    (['--rician-factor', str(12.0)]),
    (['-l', str(2.0)]),
    (['--path-loss', str(3.0)]),
    (['-hi', str(0.1), '--sic-ip', str(0.05)]), # Imperfect
    (['-p1', str(0.8), '-p2', str(0.2)]),       # Power coefficients
    (['-t1', str(0.5), '-t2', str(1.0)]),
    (['-uh', str(15)]),
    (['--snr-min', str(10), '--snr-max', str(50)]),
    # ([]), ([]),
    # etc...
]

# Invalid parameters, for testing one or two of them at a time
# No need to repeat both short and long forms, use only one of them
data_params_invalid_individual = [
    (['-p', str(-1.0)]),
    (['-l', str(-2.0)]),
    (['-s', str(10), '-f', str(20.0)]),
    ([ '-f', str(20.0)]),
    (['-p1', str(0), '-p2', str(0.8)]),
    (['-p1', str(0.6), '-p2', str(0.6)]),
    (['-hi', str(2), '--sic-ip', str(2)]),
    (['--sic-ip', str(2)]),
    (['-ur', str(50)]),
    (['-r', str(-3), '-uh', str(2)]),
    (['-uh', str(2)]),
    (['-t1', str(5.0), '-t2', str(-1.0)]),
    (['-t2', str(-1.0)]),
    (['--snr-min', str(30), '--snr-max', str(10)]),
    (['--snr-max', str(10)]),
    (['--number-uav', str(2)]),
    (['--number-user', str(4)]),
]

# How many values of each parameter to test in combination
# 2 - Minimum, will only test the limit values
# 3 - More through testing, also tests the middle value between limits
# More - Better, but very slow...
num_values = 2

# Valid combinations of parameters
s_range = [100] # Only test with 100 monte carlo samples, otherwise it takes too long
p_range = np.linspace(1.0, 2.0, num=num_values)
f_range = np.linspace(10.0, 18.0, num=num_values)
l_range = np.linspace(2.0, 3.0, num=num_values)
r_range = np.linspace(1.0, 4.0, num=num_values)
ur_range = np.linspace(10.0, 20.0, num=num_values)
uh_range = np.linspace(10, 30, num=num_values)
t1_range = np.linspace(0.1, 1.0, num=num_values)
t2_range = np.linspace(0.1, 1.0, num=num_values)
hi_range = np.linspace(0.0, 1.0, num=num_values)
si_range = np.linspace(0.0, 1.0, num=num_values)
p1_range = np.linspace(0.1, 1.0, num=num_values)
p2_range = np.linspace(0.1, 1.0, num=num_values)
snr_min_range = np.linspace(10.0, 15.0, num=num_values)
snr_max_range = np.linspace(30.0, 80.0, num=num_values)
snr_samples_range = [round(x) for x in np.linspace(10, 40, num=num_values)]
seed_range = [123] # Use just one seed, otherwise it takes too long

# Create valid combinations of parameters
data_params_valid_combination = [
    (
        '-s', str(s), '-p', str(p), '-f', str(f), '-l', str(l), '-r', str(r),
        '-ur', str(ur), '-uh', str(uh), '-t1', str(t1), '-t2', str(t2),
        '-hi', str(hi), '-si', str(si), '-p1', str(p1), '-p2', str(p2),
        '--snr-min', str(snr_min), '--snr-max', str(snr_max),
        '--snr-samples', str(snr_samples), '--seed', str(seed)
    )
    for s in s_range
    for p in p_range
    for f in f_range
    for l in l_range
    for r in r_range
    for ur in ur_range
    for uh in uh_range
    for t1 in t1_range
    for t2 in t2_range
    for hi in hi_range
    for si in si_range
    for p1 in p1_range
    for p2 in p2_range if p1 + p2 <= 1.0
    for snr_max in snr_max_range
    for snr_min in snr_min_range
    for snr_samples in snr_samples_range
    for seed in seed_range
]

# Test valid individual parameters
@pytest.mark.parametrize('params', data_params_valid_individual)
def test_success_individual(script_runner, params):
    subtest_success(script_runner, params)

# This is a slow test, to avoid running it use `pytest -m "not slow"`
@pytest.mark.slow
@pytest.mark.parametrize('params', data_params_valid_combination)
def test_success_combination(script_runner, params):
    subtest_success(script_runner, params)

# This function is not directly a test; it will be called by other actual test
# functions
def subtest_success(script_runner, params):
    result = script_runner.run(script_name, *params)
    assert result.success          # Successful run
    assert result.returncode == 0  # Code 0 means successful run
    assert len(result.stdout) > 0  # Measurable output in standard output stream
    assert len(result.stderr) == 0 # No output in error output stream

# Test invalid individual parameters
@pytest.mark.parametrize('params', data_params_invalid_individual)
def test_failure(script_runner, params):
    result = script_runner.run(script_name, *params)
    assert not result.success     # Unsuccessful run
    assert result.returncode == 1 # Error code 1 returned due to invalid params
    assert len(result.stderr) > 0 # Check for output in error output stream

# Test that no output is produced when using the --no-print option
def test_success_no_print(script_runner):
    result = script_runner.run(script_name, '--no-print')
    assert result.success          # Successful run
    assert result.returncode == 0  # Code 0 means successful run
    assert len(result.stdout) == 0 # No output in stdout due to --no-print
    assert len(result.stderr) == 0 # No output in error output stream

# Test that a file is created when the -o option is specified
def test_file_creation(script_runner):
    with tempfile.TemporaryDirectory() as tmp:
        output_file = os.path.join(tmp, 'tempfile.csv')
        result = script_runner.run(script_name, '--output', output_file)
        assert os.path.exists(output_file) # Check file was created successfully
        assert result.success          # Successful run
        assert result.returncode == 0  # Code 0 means successful run
        assert len(result.stderr) == 0 # No output in error output stream

# Test successful run when generating plots (the plots themselves are not tested)
@patch("uavnoma.command_line.plt") # Avoid getting stuck when calling plot.show()
def test_success_plot(plt, script_runner):
    result = script_runner.run(script_name, '--plot')
    assert result.success          # Successful run
    assert result.returncode == 0  # Code 0 means successful run
    assert len(result.stderr) == 0 # No output in error output stream
