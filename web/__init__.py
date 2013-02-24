# encoding: utf-8


from flask import Flask
from web.lib.flask_bootstrap import Bootstrap

app = Flask(__name__)

app.debug = True

Bootstrap(app)


