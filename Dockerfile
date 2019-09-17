FROM alpine:latest

COPY *.py requirements.txt /hal9000/
COPY ./packages /hal9000/packages

RUN apk add --no-cache python3 && \
    pip3 install -r /hal9000/requirements.txt

USER nobody

WORKDIR /hal9000

EXPOSE 3000

ENTRYPOINT ["/usr/bin/python3"]
CMD ["/hal9000/hal9000.py"]
