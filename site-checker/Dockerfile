FROM ciscotestautomation/pyats:latest
ADD . /scripts
ADD easypy_config.yaml /pyats
VOLUME /reports
WORKDIR /scripts
CMD cd /scripts && pyats run job ./website_check_job.py --html_logs /reports/ --mail-html
