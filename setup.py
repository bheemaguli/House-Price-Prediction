from setuptools import setup, find_packages
from typing import List

PROJECT_NAME="house-price-predictor"
VERSION="0.0.2"
AUTHOR="Sumanth Kashyap"
DESCRIPTION="This is a ritualistic Machine Learning project."
REQUIREMENTS_FILE="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements_list()->List[str]:
    with open(REQUIREMENTS_FILE, encoding='utf-16', mode='r') as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list(),
)