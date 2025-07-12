'''
    The setup.py file is an essential part of packaging and distributing Python projects.
    It is used by setuptools to define configuration of your project such as its
    metadata, dependencies, and more. 
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    This function pulls all the required packages from requirements.txt and passes it to install_requires
    '''
    try: 
        requirements = []
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # removes \n and leading/trailing spaces
                if line and line != '-e .': #removes -e. during package building
                    requirements.append(line)

        return requirements
    
    except FileNotFoundError:
        print('requirements.txt file not found')

#Metadata about the entire project
setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Saad Abdullah',
    author_email='sabdullah201098@gmail.com',
    #When this is run, it looks for the app package inside the project folder 
    packages=find_packages(),
    #This finds all the dependicies 
    install_requires=get_requirements('requirements.txt')
)