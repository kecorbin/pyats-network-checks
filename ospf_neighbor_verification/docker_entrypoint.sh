#!/bin/bash
# docker  will restart the container whenever it exits,
# so this is how long we wait before rerunning the test
echo "Sleeping for $POLLING_INTERVAL seconds"
sleep $POLLING_INTERVAL

# activate workspace
# ------------------
source ${WORKSPACE}/bin/activate

# run tests
cd /scripts
export PYTHONPATH=$PYTHONPATH:$(pwd)
easypy ospf_neighbor_check.py -configuration easypy_config.yaml -html_logs . -testbed_file testbed.yaml

# if all tests succeed, easypy exits with code 0
# set an environment variable to determine whether notifications will fire
if [ $? -eq 0 ]; then
    export RESULT="Passed"
else
    export RESULT="Failed"
fi
echo "RESULT set to $RESULT"

# these scripts use the env variable above to decide independently whether
# or not they send anything
python notifications/webex_teams_notifications.py

# cleanup
rm -rf archive
rm -rf TaskLog.html
