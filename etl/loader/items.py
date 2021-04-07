from utils.connect_api import ConnectAPI
from models.core import ConfigDatabase, SearchRAW
from utils.database import DatabaseHandler


class LoaderItems:
    """
    class to load items to dict tables
    """

    def __init__(self):
        self.db = ConfigDatabase()
        self.site = ''

    def execute(self):
        data_raw = self.db.session.query(SearchRAW).all()
        for item in data_raw:
            self.load_data_dict(item)

    def load_data_dict(self, data):
        self.site = data.site
        for item in data.json_data['results']:
            values = {
                'price': item.get('price'),
                'start_time': item.get('start_time'),
                'name': self._search_category(item.get('category_id')),
                'description': self._search_currency(item.get('currency_id')),
                'nickname': self._search_nickname(item.get('seller')['id'])
            }
            DatabaseHandler().add_item_dict(**values)

    @staticmethod
    def _search_category(category_id):
        search = 'categories/' + category_id
        category = ConnectAPI().get_item_api(search)
        if category:
            return category.get('name')
        else:
            return None

    @staticmethod
    def _search_currency(currency_id):
        search = 'currencies/' + currency_id
        currency = ConnectAPI().get_item_api(search)
        if currency:
            return currency.get('description')
        else:
            return None

    @staticmethod
    def _search_nickname(user_id):
        search = 'users/' + str(user_id)
        nickname = ConnectAPI().get_item_api(search)
        if nickname:
            return nickname.get('nickname')
        else:
            return None

