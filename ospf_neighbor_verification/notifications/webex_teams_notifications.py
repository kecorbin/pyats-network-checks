import socket
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import logging
import os


logger = logging.getLogger('webex_teams_notifications')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # noqa
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


token = os.getenv('SPARK_TOKEN')
room_id = os.getenv('ROOM_ID')

router_name = os.getenv('ROUTER_NAME')
server_name = os.getenv('SERVER_NAME')
url = "https://api.ciscospark.com/v1/messages"


def get_url(container_id):
    return "http://{}:9000/#/containers/{}".format(server_name, container_id)


def get_job_id():
    return get_container_id()


def get_container_id():
    """retrieves the container_id """
    hostname = socket.gethostname()
    return hostname


def send_html_report():
    logger.info("sending html task report to webex teams")
    job_id = get_job_id()
    job_url = get_url(job_id)
    msg = "Job Summary Report for {} job id {} ({})".format(router_name,
                                                            job_id,
                                                            job_url)

    m = MultipartEncoder({'roomId': room_id,
                          'text': msg,
                          'files': ('SummaryReport.html',
                                    open('TaskLog.html', 'rb'),
                                    'application/html')
                          })

    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                      headers={
                        'Authorization': 'Bearer {}'.format(token),
                        'Content-Type': m.content_type})

    logger.info("Response from Webex Teams: {}".format(r.text))


def send_archive_zip():

    logging.info("sending archive zip report to webex teams")

    # get the archive zip filename, we assume there is only one
    # because we are running in docker

    # this line just returns the path to the only zip file in the archive dir
    f = [os.path.join(r, file) for r, d, f in os.walk("archive") for file in f]
    zip_filename = f[0]
    job_id = get_job_id()
    job_url = get_url(job_id)
    msg = "Job Archive Report for job id {} ({})".format(router_name,
                                                         job_id,
                                                         job_url)

    m = MultipartEncoder({'roomId': room_id,
                          'text': msg,
                          'files': (zip_filename,
                                    open(zip_filename, 'rb'),
                                    'application/zip')
                          })

    r = requests.post('https://api.ciscospark.com/v1/messages',
                      data=m,
                      headers={
                        'Authorization': 'Bearer {}'.format(token),
                        'Content-Type': m.content_type})

    logger.info("Response from Webex Teams: {}".format(r.text))


def main():
    result = os.getenv('RESULT')
    if token and room_id:
        pass
    else:
        exit("Token and Room ID not found in environment")

    if result == "Passed":
        logger.info('All Tests Passed, nothing to do')
        exit(0)
    else:
        logger.info("Tests Failed Sending Webex Notifications")
        send_html_report()
        send_archive_zip()



if __name__ == "__main__":
    main()
