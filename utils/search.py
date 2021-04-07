from models.core import ConfigDatabase, Items


class SearchItem:
    """
    class to search item
    """

    def __init__(self):
        self.db = ConfigDatabase()

    def search_item(self, item):
        item_search = self.db.session.query(Items).filter(Items.id == item).first()
        if item_search:
            return item_search
        else:
            return None
