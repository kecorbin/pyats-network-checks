#!/usr/bin/env python
import yaml
import logging
import requests
from pyats import aetest
from pyats.aetest.loop import Iteration

# Get your logger for your script
log = logging.getLogger(__name__)


class SitesToTest(object):
    """ Generates site/proxy combinations """
    def __init__(self, loopee):
        with open('proxies.yaml', 'r') as fh:
            self.proxies = yaml.safe_load(fh)
        with open('websites.yaml', 'r') as fh:
            self.sites = yaml.safe_load(fh)

    def __iter__(self):
        for p in self.proxies.keys():
            proxy = self.proxies[p]
            for site, info in self.sites.items():
                yield Iteration(uid='{}_via_{}'.format(site, p),
                                parameters={'site': info, 'proxy': proxy})


@aetest.loop(generator=SitesToTest)
class CheckWebSite(aetest.Testcase):

    @aetest.test
    def response_code(self, proxy, site):
        url = site['url']
        log.info("Checking {}".format(site))
        resp = requests.get(url, proxies=proxy)

        if resp.ok:
            self.passed('all good')
        else:
            self.failed('rur roh')

    @aetest.test
    def response_time(self, proxy, site):
        url = site['url']
        threshold = site['threshold']
        log.info("Accessing {} via {})".format(site, proxy))
        resp = requests.get(url, proxies=proxy)
        load_time = resp.elapsed.total_seconds()
        log.info('Page load time was {} threshold {}'.format(load_time,
                                                             threshold))
        if load_time < threshold:
            self.passed('all good')
        else:
            self.failed('rur roh')


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
