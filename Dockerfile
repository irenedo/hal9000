FROM alpine:latest

RUN apk add --no-cache python3 py3-psutil && \
    pip3 install slackclient slackeventsapi

ADD *.py /hal9000/

USER nobody

EXPOSE 3000

ENTRYPOINT ["/usr/bin/python3"]
CMD ["/hal9000/hal9000.py"]
