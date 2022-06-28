from setuptools import setup, find_packages
from typing import List

PROJECT_NAME="house-price-predictor"
VERSION="0.0.2"
AUTHOR="Sumanth Kashyap"
DESCRIPTION="This is a ritualistic Machine Learning project."
REQUIREMENTS_FILE="requirements.txt"

def get_requirements_list()->List[str]:
    with open(REQUIREMENTS_FILE, encoding='utf-16', mode='r') as requirement_file:
        return requirement_file.readlines().remove("-e .")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list(),
)