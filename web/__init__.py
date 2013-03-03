# encoding: utf-8
import os

from flask import Flask, url_for
from web.lib import misc
from web.lib.flask_bootstrap import Bootstrap
from web.lib.img_lib import ImageLibrary

app = Flask(__name__)

app.debug = True
app.config['UPLOAD_FOLDER'] = os.path.join(misc.prefix, 'images')
app.config['IMG_COUNT'] = misc.get_img_count()

Bootstrap(app)

if 'img_lib' not in locals():
    img_lib = ImageLibrary()

