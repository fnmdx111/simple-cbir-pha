# encoding: utf-8

import os
from flask import render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from web import app, img_lib
from web.lib import misc
from web.lib.misc import _hex


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/img_lib')
def image_library():
    img_lib.refresh()
    return render_template('img_lib.html')


@app.route('/get_img_lib', methods=['POST'])
def get_image_library():
    return jsonify(result=map(lambda (key, value): (_hex(key),
                                                    value,
                                                    img_lib.img_set.inverse[(key, value)][1]),
                              img_lib.all()))


@app.route('/upload_image', methods=['POST'])
def upload_image():
    img_file = request.files['image']
    if img_file:
        ext = misc.extension(img_file.filename)
        app.config['IMG_COUNT'] = misc.get_img_count() + 1

        filename = secure_filename('.'.join([str(app.config['IMG_COUNT']), ext]))
        img_file.save(os.path.realpath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

        return jsonify({'status': 'successful'})


@app.route('/query_by_url', methods=['POST'])
def query_resemble_images_by_url():
    image_url = request.form['param']

    result = img_lib.query(image_url=image_url)
    result = map(lambda (key, value): (_hex(key), value), result)
    print result

    return jsonify(result=result)


@app.route('/query_by_hash', methods=['POST'])
def query_resemble_images_by_hash():
    image_hash = request.form['param']
    base = 10
    if image_hash.startswith('0b'):
        base = 2
    elif image_hash.startswith('0x'):
        base = 16
    elif image_hash.startswith('0o'):
        base = 8
    image_hash = int(image_hash, base=base)

    result = img_lib.query(image_hash=image_hash)
    result = map(lambda (key, value): (_hex(key), value), result)
    print result

    return jsonify(result=result)


@app.route('/serve/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(img_lib.image_lib_path, filename)


@app.route('/thumb/<path:filename>', methods=['GET'])
def serve_thumbnail(filename):
    return send_file(img_lib.get_thumbnail(filename))


