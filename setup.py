from setuptools import setup, find_packages
from typing import List


requirement_lst=[]
def get_requirements()->List[str]:
    try:
        with open('requirements.txt') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")
    return requirement_lst

setup(
    name='Network Security Project',
    version='0.0.1',
    author='Pushkar Chuadhari',
    packages=find_packages(),
    install_requires=get_requirements(),
)