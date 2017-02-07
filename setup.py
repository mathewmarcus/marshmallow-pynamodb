from setuptools import setup, find_packages

setup(
    name="marshmallow-pynamodb",
    version="0.1.4",
    packages=find_packages(),
    description='PynamoDB integration with the marshmallow (de)serialization library',
    author='Mathew Marcus',
    author_email='mathewmarcus456@gmail.com',
    long_description=open('README.rst').read(),
    install_requires=[
        "marshmallow>=2.12.2",
        "pynamodb>=2.0.3",
    ]
)
