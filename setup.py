import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pauavnoma",
    version = "0.1.0" ,
    author = "Brena Lima",
    author_email = "brenakslima@gmail.com",
    description = "UAV-NOMA System Model",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/limabrena/power-allocation-UAV-NOMA-two-users",
    packages = ['pauavnoma'],
    install_requires = ['numpy', 'python-math', 'matplotlib'],
    python_requires = '>=3.6',

) 