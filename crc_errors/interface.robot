# Execute a Test Case from Robot
# ================================================

*** Settings ***
Library        ats.robot.pyATSRobot

*** Variables ***
# Defining variables that can be used elsewhere in the test data.
${testbed}     ../evpn_fabric.yaml


*** TestCases ***

Initialize
    # select the testbed to use
    use testbed "${testbed}"
    run testcase "CRC_Count_check:common_setup"


CRC_Check
    run testcase "CRC_Count_check.CRC_count_check"
