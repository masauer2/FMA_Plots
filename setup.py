from setuptools import setup, find_packages

setup(
    name='FMAPlots',
    version='0.1.0',
    packages=find_packages(include=['FMAPlots', 'FMAPlots.*']),
    install_requires=['numpy>=1.14.5','matplotlib==3.9.2', 'pandas']
)
