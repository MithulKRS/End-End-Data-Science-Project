from setuptools import find_packages, setup
from typing import List

cont='-e .'
def get_requirements(file_path:str)->List[str]:
    req=[]
    with open(file_path) as file_obj:
        req=file_obj.readlines()
        req=[r.replace("\n","") for r in req]

        if cont in req:
            req.remove(cont)
    
    return req

setup(
    name='DSProject',
    version='0.0.1',
    author='mithul',
    author_email='mithakku30@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)