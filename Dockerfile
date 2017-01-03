FROM ubuntu
RUN apt-get update
RUN apt-get install -y ffmpeg libjpeg-dev libpng-dev libtiff-dev libjasper-dev libgtk2.0-dev python-numpy python-pycurl webp python-opencv python-dev python-pip
COPY . /thumbor
VOLUME /thumbor
WORKDIR /thumbor
RUN python setup.py install
RUN cp bin/webpconvertor /usr/local/bin/webp
ENTRYPOINT thumbor -c thumbor/thumbor.conf