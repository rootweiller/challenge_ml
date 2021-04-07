import logging
import pandas as pd
from datetime import datetime
from os.path import splitext

from models.core import ConfigDatabase, File, Extension, Items


class DatabaseHandler:
    """
    class for use database project
    """

    def __init__(self):
        self.db = ConfigDatabase()
        self.ALLOWED_EXTENSIONS = ['.txt', '.csv']

    def save_file(self, file):
        delimiter = self.identify_delimiter(file)
        file_format = self.identify_extension(file)
        file = File(
            name=file.filename, format=file_format, separator=delimiter, created_at=datetime.utcnow()
        )
        self.db.session.add(file)
        self.db.session.commit()
        return file.id

    def identify_delimiter(self, file):
        delimiter = self.db.session.query(Extension).filter(Extension.is_active.is_(True)).all()
        for item in delimiter:
            data_raw = pd.read_csv(file, sep=str(item.name), engine='python')
            if data_raw.columns.all():
                delimiter_file = item.name
                return delimiter_file
            else:
                logging.info("No delimiter")

    def identify_extension(self, file):
        file_extension = splitext(file.filename)[-1].lower()
        if file_extension in self.ALLOWED_EXTENSIONS:
            return file_extension
        else:
            logging.info("Not supported extension file")

    def add_item_dict(self, **kwargs):
        try:
            item_new = Items(**kwargs)
            self.db.session.add(item_new)
            self.db.session.commit()
        except Exception as error:
            logging.info("Failed when save item {0} with error {1}".format(kwargs['name'], error))
            self.db.session.rollback()
