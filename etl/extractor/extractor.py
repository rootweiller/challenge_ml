import logging
import os

from models.core import ConfigDatabase, File
from utils.dispatcher_aws import Dispatcher


class Extractor:
    """
    class to extract info from file
    """

    def __init__(self, file_id):
        self.bucket_name = os.environ.get('AWS_BUCKET_NAME')
        self.file_id = file_id
        self.db = ConfigDatabase()
        self.dispatcher = Dispatcher('s3')

    def execute(self):
        file = self.db.session.query(File).filter(File.id == self.file_id).first()
        if file:
            read_file = self.dispatcher.read_file_s3(self.bucket_name, file.name)
            read_file.to_sql('config_country', self.db.engine, if_exists='append', index=False)
            self.update_is_processed(file.id)
            values = {
                'job_name': 'Transformation-' + str(file.id),
                'script': str('transformation.py')
            }
            Dispatcher('batch').aws_batch(**values)
            logging.info("Extract file successfully {0}".format(file.name))
        else:
            logging.info("File processed")

    def update_is_processed(self, file_id):
        try:
            self.db.session.query(File).filter(File.id == file_id).update({'is_processed': True})
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            logging.info("Failed to update file {0} with error {1}".format(file_id, error))
            return False

