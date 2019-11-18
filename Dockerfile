FROM gcr.io/google-appengine/python

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get update
redis-server
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
RUN apt-get install -y xvfb
RUN apt-get install -y firefox
RUN apt-get install git-lfs

LABEL python_version=python

RUN virtualenv --no-download /env -p python
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

ADD . /app/

CMD exec gunicorn -b :$PORT worker_service:app --timeout 180
