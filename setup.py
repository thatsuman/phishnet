from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
        Return list of requirements
    """

    requirement_lst:List[str] = []
    
    try:
        with open('requirements.txt','r') as file:
            # read lines from the file
            lines = file.readlines()
            # process each line
            for line in lines:
                requirement = line.strip()
                # ignore empty lines and -e.
                if requirement and requirement != '-e.':
                    requirement_lst.append(requirement)
   
    except FileNotFoundError:
        print("Requirements.txt File Not Found!!")

    return requirement_lst


# print(get_requirements())


setup(
    name="phishnet",
    version="0.0.1",
    author="suman mondal",
    author_email="suman.mondal@outlook.in",
    packages=find_packages(),
    install_requires=get_requirements()
)