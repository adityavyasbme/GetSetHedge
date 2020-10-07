FROM python:3.7.7

WORKDIR .

ARG PIP_EXTRA_INDEX_URL

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["bash", "./run.sh"]
