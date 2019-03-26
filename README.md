# pyats-network-checks

This repository contains several scripts for network health checking using the
[pyATS Framework](https://developer.cisco.com/site/pyats/)

These are intended be examples/starting points for solving common network operations
challenges.


# Installation / configuration

##### Installation
```
git clone https://github.com/kecorbin/pyats-network-checks
cd pyats-network-checks
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
##### Simulation

we've provided a [topology.virl](./topology.virl) file for you to test with.

##### Testbed configuration

we've provided a [default_testbed.yaml](./testedbed.yaml) to go along with the sample topology.  you'll likely need to change it to match your devices

# checks

* #### [bgp_adjacencies](./bgp_adjacencies) - "if a neighbor is configured, it should be established"

* #### [crc_errors](./crc_errors) - "No interface should be accumulating CRC errors"

* #### [OSPF Neighbor Verification](./ospf_neighbor_verification) - "This device should
have these OSPF neighbors"
