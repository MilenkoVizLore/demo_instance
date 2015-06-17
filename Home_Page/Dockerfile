FROM ubuntu
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code/
WORKDIR /code/home_page
RUN apt-get update && apt-get install -y python-pip sqlite && pip install django
RUN python manage.py syncdb --noinput
EXPOSE 8080
ENTRYPOINT ["python", "manage.py", "runserver" ]
CMD ["0.0.0.0:8080"]