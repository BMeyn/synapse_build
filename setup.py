"""Setup.py script for packaging project."""

from setuptools import setup, find_packages

import os
import yaml

from setuptools import setup

# read the contents of your README file
from pathlib import Path


def get_long_description():
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()
    return long_description


def load_requirements(requirements_path):
    """function that loads the requirements.txt file and returns a list of packages to be installed"""
    with open(requirements_path, 'r') as stream:
        requirements = stream.read().splitlines()
    return requirements


def load_project_config(config_path):
    """ load_project_config Module """
    with open(config_path, 'r') as stream:
        config_dict = yaml.full_load(stream)
    return config_dict


if __name__ == '__main__':

    project_config = load_project_config("config/project_config.yml")
    dependencies = load_requirements("requirements_pkg.txt")
    long_description = get_long_description()

    setup(
        name=project_config['package_name'],
        version=os.getenv('GITVERSION_SEMVER'),
        package_dir={'': 'src'},
        packages=find_packages('src', include=[
            'synapse_build*'
        ]),
        long_description=long_description,
        long_description_content_type='text/markdown',
        description=project_config["package_description"],
        install_requires=dependencies
    )
