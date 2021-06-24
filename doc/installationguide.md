# Developer's guide

## How to use this application?

### Download

Cloning the repository via terminal:

```
$ git clone https://github.com/limabrena/power-allocation-UAV-NOMA-two-users.git
$ cd uavnoma
```

Download ZIP file directly in my git repository:

```
https://github.com/limabrena/power-allocation-UAV-NOMA-two-users/archive/main.zip
```

The user can simply run it from the downloaded folder, provided the necessary requirements are installed. This is the easiest way for the student to be able to study and modify the system model.

### Usage

An example on how to use a package can be seen in the examples folder.
The folder contains a tutorial file `uavnoma_tutorial.ipynb`  and an example implementation of a UAV NOMA system using the *uavnoma* package.
Running the example file can be done with the following command from the project's root folder:
```
$ python plot_figures.py
```
or access the project folder from an IDE.

### Documentation

Project documentation is generated using [pdoc3](https://pdoc3.github.io/pdoc/). To generate the project documentation, running the following command in the folder `uavnoma`. 

```
pdoc3 --html --output-dir docs uavnoma/
```
This comand generates the HTML documentation and salve it in the docs folder.

On the other hand, the documentation can be viewed [here](https://limabrena.github.io/pauavnoma/docs/uavnoma.html)

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