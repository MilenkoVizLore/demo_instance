FROM netways/debian-wheezy-x86
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update
RUN apt-get install -y python-numpy
RUN apt-get install -y python-scipy
RUN apt-get install -y python-sklearn
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y postgresql postgresql-contrib
RUN pip install -r requirements.txt
ADD . /code/
RUN python Classifier/generate_dataset.py
RUN python Classifier/generate_classifier.py
RUN python Classifier/generate_classifier_acceleration.py
RUN python Classifier/generate_enhanced_classifier.py
RUN python Classifier/generate_enhanced_classifier_acceleration.py
RUN python ActivityRecognition/manage.py syncdb
