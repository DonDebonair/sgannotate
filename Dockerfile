# start with a base image
FROM ubuntu:14.10

# install dependencies
RUN apt-get -y update
RUN apt-get install -y python python-dev python-pip

# add requirements.txt and install
COPY requirements/prod.txt /code/requirements.txt
COPY sgannotate/ /code/sgannotate/
COPY migrations/ /code/migrations/
COPY manage.py /code/manage.py
COPY wsgi.py /code/wsgi.py
RUN pip install -r /code/requirements.txt

VOLUME /db

WORKDIR /code

EXPOSE 5000

# Run that shit
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000"]
