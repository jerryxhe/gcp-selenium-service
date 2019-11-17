FROM gcr.io/google-appengine/python

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get update
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

RUN python -m spacy download en_core_web_sm
RUN python -m polyglot.downloader all-corpora

ADD . /app/

CMD exec gunicorn -b :$PORT main:app --timeout 180
