from setuptools import setup

setup(
    name="Velopyraptor",
    version="0.2dev",
    packages=['velopyraptor', 'velopyraptor.distributions',],
    license='Apache License, Version 2.0',
    install_requires=['bitarray', 'networkx', 'numpy',],
    long_description=open('README.txt').read()
)
