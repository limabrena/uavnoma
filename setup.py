import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "uavnoma",
    version = "0.1.1" ,
    author = "Brena Lima",
    author_email = "brenakslima@gmail.com",
    description = "UAV-NOMA System Model",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/limabrena/uavnoma",
    packages = ['uavnoma'],
    install_requires = ['numpy', 'matplotlib'],
    python_requires = '>=3.8',
    scripts=['bin/uavnoma-cli'],
    include_package_data = True,

)