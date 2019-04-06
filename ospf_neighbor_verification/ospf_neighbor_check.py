import os
from pyats.easypy import run


# main() function must be defined in each job file
#   - it should have a runtime argument
#   - and contains one or more tasks
def main(runtime):
    pwd = os.path.dirname(__file__)
    testscript = os.path.join(pwd, 'tests/OSPFNeighborCheck.py')
    run(testscript=testscript,
        runtime=runtime)
