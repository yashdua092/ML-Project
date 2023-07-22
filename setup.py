from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ." # basically triggers setup.py automatically as try to download requirements

def get_requirements(file_path: str)->List[str]:
    '''
    returns the list of requirements as a list
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines() # will add all the packages to requirements as a para
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements



setup(
    name="ML-Project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt') # packages listed in this file, converted to list and passed to install requires(requires a list)
)