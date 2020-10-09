FROM python:3.8
LABEL maintainer="jhnnsrs@gmail.com"

# Install Minimal Dependencies for Django
ADD requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

# Install Arbeid
RUN mkdir /code
RUN mkdir /arbeider
ENV PYTHONPATH="$PYTHONPATH:/arbeider"
ENV DJANGO_SETTINGS_MODULE arbeid.settings
ENV ARNHEIM_MODULES=test
ADD . /arbeider
WORKDIR /code


CMD python /arbeider/manage.py runallworkers