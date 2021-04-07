# challenge_ml
Technical challenge ML - API's public 

# ENV 
into Dockerfile replace load values for env necessary

# Docker AWS
Use AWS ECR and AWS Batch 

    docker build -t ml-challenge .
    docker tag ml-challenge:latest
    docker push # previous login in AWS 

# Create AWS Batch Service
create job_queue and job_definition for execute this scripts.

    analyser.py = Extract information raw from csv file (CSV file upload to AWS S3)
    transformation.py = Extract RAW data and transform data into dict tables, search in API public and save RAW data 
    loader.py = Load data into dict tables 

# API
into folder api is script 
    
    app.py

run script

# Method POST
Load file to api service 
    
    http://127.0.0.1:5000/api/v1/file

# Method GET
    http://127.0.0.1:5000/api/v1/file?item=ID_ITEM

method for search item into API