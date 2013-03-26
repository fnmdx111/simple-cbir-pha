# encoding: utf-8

import os
from PIL import Image
# from web.lib.constants import IMAGE_LIBRARY_PATH
IMAGE_LIBRARY_PATH = 'images'

if __name__ == '__main__':
    concat_img_lib_path = lambda filename: os.path.join(IMAGE_LIBRARY_PATH, filename)
    get_extension = lambda filename: filename.split('.')[1]
    get_filename = lambda filename: filename.split('.')[0]

    files = os.listdir(IMAGE_LIBRARY_PATH)
    pairs = map(lambda (i, filename): (concat_img_lib_path(filename),
                                       concat_img_lib_path('%s.%s' % (get_filename(filename), 'jpg'))),
                enumerate(files))
    print pairs
    for pair in pairs:
        im = Image.open(pair[0]).resize((640, 480)).save(pair[1])
        # os.rename(*pair)

