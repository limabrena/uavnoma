# Developer's guide

## How to use this application?

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

### Usage

After installing the package, to execute the simulation on your terminal, with default parameters, simply run the following command:

```
$ uavnoma
```

Use the `-h` or `--help` option to list all the available model parameters. The script code, fully commented, also exemplifies how to use the package functions, for example to develop more complex models or implement different scenarios. The script code is available in the `main()` function in the [`uavnoma/command_line.py`](https://github.com/limabrena/uavnoma/blob/main/uavnoma/command_line.py) file.

### Documentation

Project documentation is generated using [pdoc3](https://pdoc3.github.io/pdoc/). To generate the project documentation, running the following command in the project folder `uavnoma`.

```
pdoc3 --html --output-dir docs uavnoma/
```
This comand generates the HTML documentation and salve it in the docs folder.

On the other hand, the documentation can be viewed [here](https://limabrena.github.io/uavnoma/docs/index.html)

### Test

The [pytest](https://docs.pytest.org/en/stable/) and [pytest-cov](https://pypi.org/project/pytest-cov/) packages are required for testing *uavnoma* package.

To run the unit tests, you can use the following command in the project's root folder:

```
pytest
```

To analyze test coverage, run the command below. The command will return an HTML file with test coverage information.

```
pytest --cov=uavnoma --cov-report=html
```