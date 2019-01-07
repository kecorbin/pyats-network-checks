#!/bin/env python
import logging
from ats import aetest
from ats.log.utils import banner
from genie.conf import Genie
from genie.libs import ops # noqa

log = logging.getLogger(__name__)


class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            # Mark testcase with looping information
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
                device_list.append(device)

            except Exception as e:
                msg = "Failed to connect to {} will not be checked!"
                log.info(msg.format(device.name))

        # run local_user_check against each device in the list
        aetest.loop.mark(local_user_check, device=device_list)


class local_user_check(aetest.Testcase):

    @aetest.test
    def check_for_username(self, device, expected_local_users):
        log.info('Checking for {} in local user database'.format(expected_local_users))
        usernames = device.execute('show run | inc username')
        lines = usernames.split('\r\n')
        cfg_local_users = [w.split(' ')[1] for w in lines]
        log.info('Local Users: {}'.format(cfg_local_users))

        if not sorted(expected_local_users) == sorted(cfg_local_users):
            self.failed("User lists are not same")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
