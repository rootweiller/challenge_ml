import logging
import os
import requests
from flask import jsonify


class ConnectAPI:
    """
    class connect API
    """

    def __init__(self):
        self.url = os.environ.get('URL_API')

    def get_item_api(self, get_url):
        url = self.url + get_url
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify(status_code=400, message='Failed search')
