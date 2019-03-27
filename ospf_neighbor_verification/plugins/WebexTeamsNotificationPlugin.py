import logging
import os
import json
import requests
# from requests_toolbelt.multipart.encoder import MultipartEncoder
from ats.log.utils import banner
from pyats.easypy.plugins.bases import BasePlugin

logger = logging.getLogger("WEBEXTEAMS-NOTIFICATION")

MESSAGE_TEMPLATE = """
## JOB RESULT REPORT

### Job Information

**Total Tasks**    : {results[total]}

**Overall Stats**

Passed     : {results[passed]}\n
Passx      : {results[passx]}\n
Failed     : {results[failed]}\n
Aborted    : {results[aborted]}\n
Blocked    : {results[blocked]}\n
Skipped    : {results[skipped]}\n
Errored    : {results[errored]}\n

"""

class WebExTeamsNotification(BasePlugin):
    '''
    Runs after each task, sends notification upon failure
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token = os.getenv('SPARK_TOKEN')
        self.room = os.getenv('ROOM_ID')
        self.enabled = True
        if not self.token and self.room:
            logger.info("SPARK_TOKEN or ROOM_ID not found in env, disabling")
            self.enabled = False

    def _headers(self, content_type='application/json'):
        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-Type': content_type}
        return headers

    def _send_msg(self, msg):
        payload = {'roomId': self.room,
                   'markdown': msg}
        url = 'https://api.ciscospark.com/v1/messages'
        if self.enabled:
            logger.info('Sending WebEx Teams notification')
            r = requests.post(url,
                              data=json.dumps(payload),
                              headers=self._headers())
            logger.info(r.text)

    def post_job(self, job):

        logger.info('Running post job plugin')
        logger.info(banner("JOB RESULTS"))
        logger.info(job.results)
        self._send_msg(MESSAGE_TEMPLATE.format(results=job.results))
