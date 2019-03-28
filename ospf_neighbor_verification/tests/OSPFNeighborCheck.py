import logging
from pyats import aetest
from genie.conf import Genie
from ats.log.utils import banner

try:
    from genie.ops.utils import get_ops
except ModuleNotFoundError:
    from genie.ops.base import get_ops

log = logging.getLogger(__name__)


class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed
    @aetest.subsection
    def setup(self, testbed):
        # initalize genie testbed
        testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = testbed
        # used for tracking neighbor / recovery info
        self.parent.parameters['failed_nbrs'] = list()
        self.parent.parameters['recovery_queue'] = list()

        reason = "being conservative"
        aetest.skipUnless.affix(section=DoubleCheck,
                                condition=False,
                                reason=reason)

        aetest.skipUnless.affix(section=Recovery,
                                condition=False,
                                reason=reason)

        # neighbor check for each device in the testbed using loops
        aetest.loop.mark(CheckForNeighbor, device=testbed.devices)


class CheckForNeighbor(aetest.Testcase):

    @aetest.setup
    def setup(self, testbed, device):
        device = testbed.devices[device]
        nbrs = device.custom['expected_ospf_neighbors']['neighbors']
        names = ['check_for_{}'.format(n) for n in nbrs.keys()]
        aetest.loop.mark(self.check_for_neighbor, uids=names, nbr=nbrs.keys())

    @aetest.test
    def connect(self, testbed, device):
        device = testbed.devices[device]
        device.connect(log_stdout=False)

    @aetest.test
    def collect_ospf_info(self, testbed, device):
        device = testbed.devices[device]

        # grab some info from testbed/config
        nbr_details = device.custom['expected_ospf_neighbors']
        ospf_process = nbr_details['ospf_process']
        ospf_area = nbr_details['ospf_area']

        # Retrieve Ospf Class for this device
        ospf_cls = get_ops('ospf', device)

        # Instantiate the class, and provides some attributes
        # Attributes limit the # of clis to use;
        # It will only learn the neighbors,  nothing else.
        attributes = ['info[vrf][(.*)][address_family][ipv4]'
                      '[instance][{OSPF_PROCESS}]'
                      '[areas][{OSPF_AREA}]'
                      '[interfaces][(.*)]'
                      '[neighbors][(.*)]'
                      .format(OSPF_PROCESS=ospf_process,
                              OSPF_AREA=ospf_area)]

        # parse ospf on device
        ospf = ospf_cls(device, attributes=attributes)
        ospf.learn()

        # pass/fail based on whether OSPF was parsed succesfully
        if ospf.info:
            # stash the parsed info so we can query it later
            self.parent.parameters['ospf_ops'] = ospf
            log.info(ospf.info)
            self.passed("Collected OSPF Information")
        else:
            self.failed("Could not collect OSPF information")

    @aetest.test
    def check_for_neighbor(self, testbed, device, nbr):
        log.info("Checking for OSPF neighbor {}".format(nbr))
        # get neighbor info from config

        device = testbed.devices[device]
        nbr_config = device.custom['expected_ospf_neighbors']
        ospf_process = nbr_config['ospf_process']
        ospf_area = nbr_config['ospf_area']
        vrf = nbr_config['vrf']
        nbrs = nbr_config['neighbors']

        # check for expected neighbor
        name = nbr
        nbr = nbrs[nbr]

        # in case a specific neighbor is a different area/process
        try:
            ospf_area = nbr['ospf_area']
        except KeyError:
            pass

        try:
            ospf_process = nbr['ospf_process']
        except KeyError:
            pass

        expected_interface = nbr['expected_interface']
        expected_neighbor = nbr['expected_neighbor']
        try:
            ospf_data = self.parent.parameters['ospf_ops']
            vrf_data = ospf_data.info["vrf"][vrf]
            instance = vrf_data['address_family']['ipv4']['instance'][str(ospf_process)] # noqa
            area = instance['areas'][ospf_area]
            intf = area['interfaces'][expected_interface]
            nbrs = intf['neighbors']

        except KeyError as e:
            log.error(banner("Could not parse ospf neighbors: {}".format(e)))

        if expected_neighbor in nbrs.keys():
            # we do not need to perform any recovery action
            self.passed('yay!')

        else:
            # fail check and mark to be  double checked
            nbr['device'] = device
            nbr['name'] = name
            self.parent.parameters['failed_nbrs'].append(nbr)
            aetest.skipUnless.affix(section=DoubleCheck,
                                    condition=True,
                                    reason="{}".format(nbr))

            self.failed('MISSING NEIGHBOR: {}'.format(nbr))


class DoubleCheck(aetest.Testcase):
    """Double Check after failure scenario, this testcase is skipped when
    NeighborTest suceeds"""

    @aetest.test
    def check(self):

        failed_nbrs = self.parent.parameters['failed_nbrs']
        prfx = 'double_check_for_{}'
        nbr_names = [prfx.format(nbr['name']) for nbr in failed_nbrs]
        aetest.loop.mark(self.double_check, uids=nbr_names, nbr=failed_nbrs)

    @aetest.test
    def double_check(self, nbr):

        log.info("Performing Double Check Action for {}".format(nbr))
        dev = nbr['device']
        output = dev.execute('show ip ospf neigh')
        log.info(output)
        if nbr['expected_neighbor'] in output:
            # drop them from the recovery queue
            self.parent.parameters['failed_nbrs'].remove(nbr)
            self.passed('{} Passed double check verification removing'
                        ' from recovery queue'.format(nbr))
        else:
            aetest.skipUnless.affix(section=Recovery,
                                    condition=True,
                                    reason="{}".format(nbr))

            # add this neighbor to recovery queue
            self.parent.parameters['recovery_queue'].append(nbr)
            self.failed('Still broken')


class Recovery(aetest.Testcase):
    """Recover from failure scenario, this testcase is skipped if
    NeighborTest/DoubleCheck succeed"""

    @aetest.setup
    def setup(self):
        recovery_queue = self.parent.parameters['recovery_queue']
        prfx = 'perform_recovery_for_{}'
        uids = [prfx.format(nbr['name']) for nbr in recovery_queue]
        # here we mark the recovery action to be performed on all neighbors
        # that are still "failed"
        aetest.loop.mark(self.recovery_action, uids=uids, nbr=recovery_queue)

    @aetest.test
    def recovery_action(self, nbr):
        log.info("Performing Recovery Action for {}".format(nbr))
        reason = "{} not found on {} interface {}"
        reason = reason.format(nbr['expected_neighbor'],
                               nbr['device'],
                               nbr['expected_interface']
                               )
        log.info(reason)
        action = 'Will perform corrective action on associated_network {}'
        log.info(action.format(nbr['associated_network']))

        # place your recovery code here
        self.passed('Looks like we saved the day')
