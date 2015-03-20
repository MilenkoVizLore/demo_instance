FROM mjdsys/ubuntu-saucy-i386
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN apt-get update
RUN apt-get install -y sqlite3
RUN apt-get install -y python-pip
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 4545
RUN python manage.py migrate
ENTRYPOINT ["python", "manage.py", "runserver" ]
CMD ["0.0.0.0:4545"]
