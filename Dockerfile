FROM gcr.io/google-appengine/python

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.listl'
RUN apt-get update
RUN apt-get install -y redis-server
RUN apt-get install -y source-highlight
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
RUN apt-get install -y xvfb
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y lua5.3
RUN apt-get install -y firefox
RUN apt-get install git-lfs
ADD . supervisord.conf
COPY supervisord.conf /etc/supervisord.conf
LABEL python_version=python3
RUN virtualenv --no-download /env -p python
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install redis
RUN pip install redis
RUN pip install --upgrade setuptools

ADD . /app/
#CMD exec gunicorn -b :$PORT main_server:app --timeout 180
CMD ["supervisord", "-n"]
