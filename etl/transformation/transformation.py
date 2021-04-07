import logging
from datetime import datetime

from utils.connect_api import ConnectAPI
from models.core import ConfigDatabase, Country, SearchRAW
from utils.dispatcher_aws import Dispatcher


class Transformation:
    """
    class to transform data from database and consult into API
    """

    def __init__(self):
        self.db = ConfigDatabase()

    def execute(self):
        category = self.db.session.query(Country).filter(Country.is_processed.is_(False)).all()
        for item in category:
            category_id = item.site + item.identification[:4]
            search = 'sites/' + item.site + '/search?category=' + category_id
            response = ConnectAPI().get_item_api(search)
            if response:
                self.save_data_raw(response, item.site, item.identification, category_id, item.id)
                logging.info("Save data for category {0}".format(category_id))
            else:
                logging.info("No data for this category {0}".format(category_id))
        values = {
            'job_name': str('Loader-ALL-') + str(datetime.today().date()),
            'script': str('loader.py')
        }
        Dispatcher('batch').aws_batch(**values)

    def save_data_raw(self, data, site, identification, category, _id):
        try:
            data = SearchRAW(
                site=site, identification=identification, category=category, json_data=data, is_processed=False,
                created_at=datetime.utcnow()
            )
            self.db.session.add(data)
            self.db.session.query(Country).filter(Country.id == _id).update({'is_processed': True})
            self.db.session.commit()
        except Exception as error:
            logging.info("Failed when sava data raw {0} with error {1}".format(category, error))
            self.db.session.rollback()
