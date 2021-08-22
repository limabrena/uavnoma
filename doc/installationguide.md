# Developer's guide

## How to use this application?

### Download

Cloning the repository via terminal:

```
$ git clone https://github.com/limabrena/uavnoma.git
$ cd uavnoma
```

Download ZIP file directly in my git repository:

```
https://github.com/limabrena/uavnoma/archive/main.zip
```

The user can simply run it from the downloaded folder, provided the necessary requirements are installed. This is the easiest way for the student to be able to study and modify the system model.

### Usage

After installing the package, to run the script on your terminal simply run the following command:

```
$ uavnoma
```

An example on how to use a package can be seen in the uavnoma folder. The script contains an implementation example of an UAV NOMA system using the *uavnoma* package. 

```
$ command_line.py
```

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