import os
from pyats.easypy import run
import yaml

# All run() must be inside a main function
def main():
    # Find the location of the script in relation to the job file
    pwd = os.path.dirname(__file__)
    testscript = os.path.join(pwd, 'websites.py')
    # Execute the testscript
    run(testscript=testscript)
