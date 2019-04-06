# pyats-network-checks

This repository contains several scripts for network health checking using the
[pyATS Framework](https://developer.cisco.com/site/pyats/).

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

We've provided a [topology.virl](./topology.virl) file for you to test with.

##### Testbed configuration

We've provided a [default_testbed.yaml](./testedbed.yaml) to go along with the sample topology.  You'll likely need to change it to match your devices.

# checks

* #### [BGP_adjacencies](./bgp_adjacencies) - "If a neighbor is configured, it should be established"

* #### [CRC_errors](./crc_errors) - "No interface should be accumulating CRC errors"

* #### [OSPF neighbor verification](./ospf_neighbor_verification) - "This device should have these OSPF neighbors"
