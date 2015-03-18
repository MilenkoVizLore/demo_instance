FROM ubuntu 
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update
RUN apt-get install -y python-pip
RUN apt-get install -y python-numpy
RUN apt-get install -y python-scipy
RUN apt-get install -y python-sklearn
RUN apt-get install -y sqlite3
RUN pip install -r requirements.txt
ADD . /code/
WORKDIR /code/Classifier/
RUN python generate_dataset.py
RUN python generate_classifier.py
RUN python generate_classifier_acceleration.py
RUN python generate_enhanced_classifier.py
RUN python generate_enhanced_classifier_acceleration.py
WORKDIR /code/ActivityRecognition/
RUN python manage.py migrate