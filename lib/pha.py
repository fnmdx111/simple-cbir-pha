# encoding: utf-8
# ref: http://blog.sina.com.cn/s/blog_6b291d730100wiar.html
from itertools import product

import ImageOps
from PIL import Image
import operator
from lib.constants import identity

def __get_hash(im_path, size=(8, 8), posterize=False):
    im = Image.open(im_path).resize(size).convert('L')
    if posterize:
        im = ImageOps.posterize(im, 6)    # 64 = 2 ** 6

    pixels = im.load()

    avg = 0
    for i in range(size[0]):
        for j in range(size[1]):
            avg += pixels[i, j]
    avg /= 64.

    hash = 0
    for i in range(size[0] * size[1]):
        hash += 0 if pixels[i % 8, i / 8] < avg else 1
        hash <<= 1

    return hex(hash >> 1)


def get_hash(im_path, size=(8, 8), posterize=False, pretty=False):
    im = Image.open(im_path).resize(size).convert('L')
    if posterize:
        im = ImageOps.posterize(im, 6)    # 64 = 2 ** 6

    pixels = im.load()
    avg = sum(pixels[coord] for coord in product(*map(range, size))) / 64.
    hash = reduce(lambda hash, i: (hash + (0 if pixels[i % 8, i / 8] < avg else 1)) << 1,
                  range(operator.mul(*size)), 0) >> 1

    return (hex if pretty else identity)(hash)


if __name__ == '__main__':
    print get_hash('i.png')
    print __get_hash('o.png')
    print get_hash('s.png')

