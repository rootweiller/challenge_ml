import os
import pandas as pd

import boto3


class Dispatcher:
    """
    class to dispatcher different platforms and providers
    """

    def __init__(self, resource):
        self.client = boto3.client(
            resource,
            aws_access_key_id=os.environ.get('AWS_ACCESS_ID'),
            aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION_NAME')
        )

    def aws_batch(self, **kwargs):
        command = ['python', kwargs['script']]
        if kwargs.get('parameter'):
            command.append(kwargs['parameter'])
        response = self.client.submit_job(
            jobName=kwargs['job_name'],
            jobQueue=os.environ.get('JOB_QUEUE'),
            jobDefinition=os.environ.get('JOB_DEFINITION'),
            containerOverrides={
                'vcpus': 1,
                'memory': 3600,
                'command': command
            },
            timeout={
                'attemptDurationSeconds': 1800
            },
        )
        return response

    def upload_file_s3(self, file, acl='public-read'):
        try:
            file_upload = self.client.upload_fileobj(
                file, os.environ.get('AWS_BUCKET_NAME'), file.filename, ExtraArgs={
                    "ACL": acl, "ContentType": file.content_type
                }
            )
            return file_upload
        except Exception as error:
            print("Something Wrong when upload file: ", error)
            return error

    def read_file_s3(self, bucket_name, item_name):
        obj = self.client.get_object(Bucket=bucket_name, Key=item_name)
        data_raw = pd.read_csv(obj['Body'])
        change_column = data_raw.rename(columns={'id': 'identification'})
        change_column['is_processed'] = False
        return change_column
