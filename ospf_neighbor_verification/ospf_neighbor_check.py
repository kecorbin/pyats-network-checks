from pyats.easypy import run


# main() function must be defined in each job file
#   - it should have a runtime argument
#   - and contains one or more tasks
def main(runtime):
    run(testscript='tests/OSPFNeighborCheck.py',
        runtime=runtime)
