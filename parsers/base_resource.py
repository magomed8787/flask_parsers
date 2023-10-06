from flask_restful import Resource, reqparse
import requests
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


class BaseResource(Resource):
    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pages_count', default=10, type=int, required=False, location='args')
        self.reqparse.add_argument('count', default=12, type=int, location='args', help='count of results')
        self.args = self.reqparse.parse_args()
        self.session = requests.Session()
        self.session.headers = {'User-Agent': self.USER_AGENT}
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()

    def parse(self):
        raise NotImplementedError

    def get(self):
        return self.parse()
