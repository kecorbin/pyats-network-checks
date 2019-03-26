import logging
import os

# from requests_toolbelt.multipart.encoder import MultipartEncoder

from pyats.easypy.plugins.bases import BasePlugin

logger = logging.getLogger("WEBEXTEAMS-NOTIFICATION")


class WebExTeamsNotification(BasePlugin):
    '''
    Runs after each task, sends notification upon failure
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = os.getenv('SPARK_TOKEN')
        self.room = os.getenv('ROOM_ID')

    def post_task(self, task):
        logger.info('RoomId: {}'.format(self.room))
        logger.info('Task Result: {}'.format(task.result))
        if str(task.result) == 'passed':
            logger.info('Task passed, no need to send notification')
            # webex_teams_notifications.send_html_report()
        else:
            logger.info('Task failed, lets notify some people')
            # webex_teams_notifications.send_html_report()
    #
    # def post_job(self, job):
    #     # import pdb;pdb.set_trace()
    #
    #     logger.info('RoomId: {}'.format(self.room))
    #     logger.info('BANANA')
    #     # if str(task.result) == 'passed':
        #     logger.info('Task passed, no need to send notification')
        #     webex_teams_notifications.send_html_report()
        # else:
        #     logger.info('Task failed, lets notify some people')
        #     # webex_teams_notifications.send_html_report()
