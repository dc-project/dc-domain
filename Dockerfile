FROM python:3.6.3-slim-stretch

MAINTAINER ysicing

RUN pip install urllib3 -i https://pypi.douban.com/simple

ADD . /tmp/

ENV VERSION=__VERSION__

ENTRYPOINT ["/tmp/domain.sh"]




