FROM python:3.8

WORKDIR /code

COPY . /code/

RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

ENV SECRET_KEY=''

# AWS
ENV AWS_ACCESS_ID=''
ENV AWS_ACCESS_KEY=''
ENV AWS_REGION_NAME=''
ENV AWS_BUCKET_NAME=''

# RDS Database
ENV DB_HOST=''
ENV DB_PORT=''
ENV DB_USER=''
ENV DB_PASSWORD=''
ENV DB_NAME=''


# AWS Batch
ENV JOB_QUEUE=''
ENV JOB_DEFINITION=''

# API URL
ENV URL_API=''
