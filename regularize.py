# encoding: utf-8

import os
from web.lib.constants import IMAGE_LIBRARY_PATH

if __name__ == '__main__':
    concat_img_lib_path = lambda filename: os.path.join(IMAGE_LIBRARY_PATH, filename)
    get_extension = lambda filename: filename.split('.')[1]

    files = os.listdir(IMAGE_LIBRARY_PATH)
    pairs = map(lambda (i, filename): (concat_img_lib_path(filename),
                                       concat_img_lib_path('%s.%s' % (i, get_extension(filename)))),
                enumerate(files))
    print pairs
    for pair in pairs:
        os.rename(*pair)

