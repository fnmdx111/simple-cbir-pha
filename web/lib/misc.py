# encoding: utf-8
import os

identity = lambda _: _

extension = lambda filename: filename.rsplit('.', 1)[-1]

if os.path.basename(os.getcwd()) == 'web': # directly running __init__.py
    prefix = 'static'
else:
    prefix = 'web/static'


def _reduce_func(acc, filename):
    number = int(filename.split('.')[0])
    return number if number > acc else acc


def get_img_count():
    return reduce(_reduce_func,
                  os.listdir(os.path.realpath(os.path.join(prefix, 'images'))),
                  0)


def _hex(key):
    k = hex(key)
    if 'L' in k:
        k = k[:-1]
    return k

