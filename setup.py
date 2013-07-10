from distutils.core import setup

setup(
    name="Velopyraptor",
    version="0.2dev",
    packages=['velopyraptor', 'velopyraptor.distributions',],
    license='Apache License, Version 2.0',
    requires=['bitarray', 'numpy',],
    long_description=open('README.txt').read()
)
