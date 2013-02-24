from flask import render_template
from web import app

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/img_lib')
def image_library():
    return ''


