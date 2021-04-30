FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TX JST-9
ENV TERM xterm

WORKDIR /app
ADD ./app /app

RUN apt-get install -y vim less ffmpeg open-jtalk open-jtalk-mecab-naist-jdic
RUN wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.6/MMDAgent_Example-1.6.zip/download -O MMDAgent_Example-1.6.zip
RUN unzip MMDAgent_Example-1.6.zip MMDAgent_Example-1.6/Voice/*
RUN cp -r MMDAgent_Example-1.6/Voice/mei/ /usr/share/hts-voice
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install discord.py[voice]
RUN pip install sqlalchemy
RUN pip install pymysql

CMD python entry.py