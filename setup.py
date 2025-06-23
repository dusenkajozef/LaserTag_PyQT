from setuptools import setup, find_packages

setup(
    name="laser_tag",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.4.0',
    ],
    python_requires='>=3.8',
)
