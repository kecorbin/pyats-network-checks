FROM ciscotestautomation/pyats:latest
COPY requirements.txt /pyats/requirements.txt
RUN /pyats/bin/pip install -r /pyats/requirements.txt
COPY . /scripts
WORKDIR /scripts
CMD /scripts/docker_entrypoint.sh
