from flask import Flask
from flask_restful import Api

from parsers.books_toscrape import toscrape
from parsers.parser_bundes import bundes
from parsers.parser_labirint import labirint
from parsers.parse_roscarservis import roscarservis


app = Flask(__name__)

app.config.from_object('application.config.Config')
api = Api(app)

api.add_resource(toscrape.ToScrapeResource, '/toscrape')
api.add_resource(bundes.BundesResource, '/bundes')
api.add_resource(labirint.LabirintResource, '/labirint')
api.add_resource(roscarservis.RosCarServisResource, '/roscarservis')

