from setuptools import setup

setup(
    name = "Surface-Vessel-Temp-Logger",
    version = "0.0.1",
    author = "Alexei Sondergeld",
    packages=['SurfVessTempLog'],
    install_requires=['numpy','matplotlib', 'pandas', 'time', 'datetime'],
)
