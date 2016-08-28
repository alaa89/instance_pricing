from setuptools import setup

setup(
    name='Instance Types Pricing',
    version='0.1',
    long_description=__doc__,
    packages=['instance_pricing'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
