"""
    This script performs the tests of simulation parameters.
"""


def test_command_line_script(script_runner):
    result = script_runner.run('uavnoma', '-s', str(1000))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''

def test_parameter_power_los(script_runner):
    result = script_runner.run('uavnoma','-p', str(1.0))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''

def test_parameter_power_los_err(script_runner):
    result = script_runner.run('uavnoma','-p', str(-1.0))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_rician(script_runner):
    result = script_runner.run('uavnoma','-f', str(15.0))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''  

def test_parameter_pathloss(script_runner):
    result = script_runner.run('uavnoma','-l', str(2.0))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''  

def test_parameter_pathloss_err(script_runner):
    result = script_runner.run('uavnoma','-l', str(-2.0))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_command_line_samples(script_runner):
    result = script_runner.run('uavnoma', '-s', str(10), '-f', str(20.0))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_rician_err(script_runner):
    result = script_runner.run('uavnoma', '-f', str(20.0))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_imperfect(script_runner):
    result = script_runner.run('uavnoma','-hi', str(0.1), '--sic-ip', str(0.05))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''  

def test_parameter_power_coeff(script_runner):
    result = script_runner.run('uavnoma','-p1', str(0.8), '-p2', str(0.2))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''    

def test_parameter_power_coeff_err(script_runner):
    result = script_runner.run('uavnoma','-p1', str(0), '-p2', str(0.8))
    assert result.returncode == 1
    assert not result.success
    assert result.stderr == '' 


def test_parameter_hardimpairments(script_runner):
    result = script_runner.run('uavnoma','-hi', str(2), '--sic-ip', str(2))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_sic(script_runner):
    result = script_runner.run('uavnoma', '--sic-ip', str(2))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''


def test_parameter_radius_user(script_runner):
    result = script_runner.run('uavnoma','-ur', str(50))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_radius_uav(script_runner):
    result = script_runner.run('uavnoma','-r', str(-3), '-uh', str(2))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_height_uav(script_runner):
    result = script_runner.run('uavnoma', '-uh', str(15))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''

def test_parameter_height_uav_err(script_runner):
    result = script_runner.run('uavnoma', '-uh', str(2))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_rate(script_runner):
    result = script_runner.run('uavnoma','-t1', str(0.5), '-t2', str(1.0))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''

def test_parameter_rate_pri(script_runner):
    result = script_runner.run('uavnoma','-t1', str(5.0), '-t2', str(-1.0))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''   

def test_parameter_rate_sec(script_runner):
    result = script_runner.run('uavnoma', '-t2', str(-1.0))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == '' 

def test_parameter_snr(script_runner):
    result = script_runner.run('uavnoma', '--snr-min', str(10), '--snr-max', str(50))
    assert result.success
    assert result.returncode == 0
    assert result.stderr == ''

def test_parameter_snr(script_runner):
    result = script_runner.run('uavnoma', '--snr-min', str(30), '--snr-max', str(10))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_snrmax(script_runner):
    result = script_runner.run('uavnoma', '--snr-max', str(10))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''

def test_parameter_numberuav(script_runner):
    result = script_runner.run('uavnoma','--number-uav', str(2))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''  

def test_parameter_numberuser(script_runner):
    result = script_runner.run('uavnoma','--number-user', str(4))
    assert not result.success
    assert result.returncode == 1
    assert result.stderr == ''  