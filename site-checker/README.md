# pyATS site checker

In the course of normal network validation, the ability to reach a series of websites is often checked. Additionally, accessing these sites though a number of proxy severs is desirable.  

This directory shows an example of how this can be easily accomplished using [pyATS](https://developer.cisco.com/pyats/)


## Site / Proxy Configuration

This example uses three primary YAML files for configuration. These files should
be pretty straightforward to modify to suit your needs.

* [websites.yaml](./websites.yaml) - defines all of the websites which will be checked
* [proxies.yaml](./proxies.yaml) - defines all of the proxies that will be tested.
* [easypy_config.yaml](./easypy.yaml) - defines SMTP server and email recipient information

The operation of the script is to attempt to connect to all of the websites defined, using each of the proxies, and email some nice reports based on the job run.  

To accomplish this the script makes use of pyATS [Looping](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/loop.html#looping-sections) which allows a custom generator to
be defined to dynamically configure the looping based on `# of proxies * # of sites`


## Build + Run

The easiest way to execute the tests is to build a docker image using the provided
[Dockerfile](./Dockerfile)

### Build
```
docker build -t my-site-checker .
```

### Run
```
docker run -v $(pwd):/reports my-site-checker
```

**Note:** this maps your current directory to /reports where the full HTML logs will place.  after
executing the tests you should have a TaskLog.html file in your current directory
