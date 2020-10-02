FROM python:3.6
MAINTAINER Aman Singh

WORKDIR .
COPY /assets /assets
COPY listings_details.csv /listings_details.csv
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY layout.py /layout.py
COPY airbnb_analytics.py /airbnb_analytics.py
COPY airbnb_property_details.py /airbnb_property_details.py

CMD python /airbnb_property_details.py