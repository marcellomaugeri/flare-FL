import sys
from setuptools import setup, find_packages
import os

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up two levels

setup(
    name=NAME,
    version=VERSION,
    description="Model Validation API",
    author_email="",
    url="",
    keywords=["OpenAPI", "Model Validation API"],
    install_requires=REQUIRES,
    packages=find_packages(where=BASE_DIR),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    API for validating a model with provided weights
    """
)

