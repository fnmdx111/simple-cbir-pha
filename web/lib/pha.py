# encoding: utf-8
# ref: http://blog.sina.com.cn/s/blog_6b291d730100wiar.html
from itertools import product

import ImageOps
from PIL import Image
import operator


__CONST_WIDTH = 8
__CONST_HEIGHT = 8
__CONST_POSTERIZE_BIT = 6    # 64 = 2 ** 6
__CONST_SIZE = (__CONST_WIDTH, __CONST_HEIGHT)
__CONST_COORDINATES = tuple(product(*map(range, __CONST_SIZE)))    # itertools.product returns an iterator which will
__CONST_PIXEL_COUNT = operator.mul(*__CONST_SIZE)                  # exhaust after first iteration
__CONST_PIXEL_COUNT_FLOAT = float(__CONST_PIXEL_COUNT)
__CONST_PIXEL_COUNT_LIST = range(__CONST_PIXEL_COUNT)
__CONST_HASH_REDUCE_FUNC = lambda avg, pixels: (
    lambda _hash, i: (_hash + (0 if pixels[i % __CONST_WIDTH, i / __CONST_HEIGHT] < avg else 1)) << 1
)


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

    _hash = 0
    for i in range(size[0] * size[1]):
        _hash += 0 if pixels[i % 8, i / 8] < avg else 1
        _hash <<= 1

    return hex(_hash >> 1)


def get_hash(_im, size=__CONST_SIZE, posterize=False):
    im = Image.open(_im).resize(size).convert('L')
    if posterize:
        im = ImageOps.posterize(im, __CONST_POSTERIZE_BIT)

    pixels = im.load()
    avg = sum([pixels[coord] for coord in __CONST_COORDINATES]) / __CONST_PIXEL_COUNT_FLOAT
    _hash = reduce(__CONST_HASH_REDUCE_FUNC(avg, pixels),
                   __CONST_PIXEL_COUNT_LIST,
                   0) >> 1    # after 64 left-shifts, the result is 65bit, need shift right once to get a 64bit hash

    return _hash


if __name__ == '__main__':
    print get_hash('i.png')
    print __get_hash('o.png')
    print get_hash('s.png')


