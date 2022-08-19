# System Model of UAV-NOMA System with Two-users

[![Tests](https://github.com/limabrena/uavnoma/actions/workflows/test.yml/badge.svg)](https://github.com/limabrena/uavnoma/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/limabrena/uavnoma/branch/main/graph/badge.svg)](https://app.codecov.io/gh/limabrena/uavnoma)

A Python 3.8 implementation of the System Model of Unmanned Aerial Vehicle with Non-Orthogonal Multiple Access (UAV-NOMA) System and 2 ground users under considerations of non-ideal conditions, such as imperfect successive interference cancelation (SIC) and residual hardware impairments (RHI). We consider a downlink UAV-aided NOMA network, as illustrated in the figure below.

![System model.](https://media.githubusercontent.com/media/limabrena/uavnoma/main/figures/uav_system_model_ex.png)

## Features

The **uavnoma** package allows the user to study the modeling of a UAV-NOMA network and use it as a basis for implementing other technologies. This application can be used as a study tool to understand the behavior of the achievable rate by two users and the influence of the allocation of power coefficients in a UAV-NOMA system under non-ideal conditions. The communication model presented is a base of UAV-NOMA principles and can be expanded to several other scenarios, such as cooperative systems, full-duplex communication,  and others in order to improve system performance.

The user can modify parameters and analyze the system's behavior. Based on this, new methods can be proposed to solve UAV trajectory problems, power allocation, user pairing, energy harvesting for UAV maintenance, decoding order and others.

The package contains functions to:

- Calculate the position of the UAV and users;
- Generate the channel gain between UAV and users;
- Calculate of the Signal Interference Noise Ratio (SINR);
- Analyze system performance using as metrics the instantaneous achievable rate and outage probability.

A command line script is also included, allowing for anyone to experiment with the model without knowing or using Python. The user can run a simulation with default parameters using the following command:

```
uavnoma
```

The script is fully parameterizable, and the available parameters can be listed with:

```
uavnoma --help
```

## Requirements

The implementation requires Python 3.8+ to run.
The following libraries are also required:

- `numpy`
- `matplotlib`
- `pandas`
- `tabulate`
- `argparse`

## How to install

### From PyPI

```
pip install uavnoma
```

### From source/GitHub

Directly using pip:

```
pip install git+https://github.com/limabrena/uavnoma.git#egg=uavnoma
```

Or each step at a time:

```
git clone https://github.com/limabrena/uavnoma.git
cd uavnoma
pip install .
```

### Installing for development and/or improving the package

```
git clone https://github.com/limabrena/uavnoma.git
cd uavnoma
pip install -e .[dev]
```

This way, the package is installed in development mode. As a result, the pytest dependencies/plugins are also installed.

## Documentation

* [*uavnoma* package documentation](https://limabrena.github.io/uavnoma/docs/index.html)
* [Developer's guide](https://limabrena.github.io/uavnoma/docs/index.html#developers-guide)
* [Scenario Description](https://limabrena.github.io/uavnoma/docs/index.html#scenario-description)

## License

[MIT License](LICENSE.txt)
