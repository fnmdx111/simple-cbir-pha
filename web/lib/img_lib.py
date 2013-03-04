# encoding: utf-8

from StringIO import StringIO
from itertools import combinations
import os
import urllib2
import operator
import Image
from web.lib import constants
from web.lib.disjoint_set import DisjointSet
from web.lib.misc import prefix
from web.lib.pha import get_hash


filesystem_encoding = 'utf-8'
if 'nt' in os.name:
    filesystem_encoding = 'gbk'


class ImageLibrary(object):
    def __init__(self,
                 image_lib_path=os.path.realpath(os.path.join(prefix, constants.IMAGE_LIBRARY_PATH)),
                 confidence=constants.confidence):
        self.image_lib_path = image_lib_path
        self.hashes = []
        self.img_set = DisjointSet()
        self.confidence = confidence

        self.refresh()


    def refresh(self):
        self.hashes = []
        self.img_set = DisjointSet()

        for filename in os.listdir(self.image_lib_path):
            print filename
            _hash = get_hash(os.path.join(self.image_lib_path, filename))
            self.hashes.append((_hash, filename.decode(filesystem_encoding).encode('utf-8')))

        for pair in self.hashes:
            self.img_set.union(pair, pair)

        for (h1, f1), (h2, f2) in combinations(self.hashes, 2):
            if self._resemble(h1, h2):
                self.img_set.union((h1, f1), (h2, f2))


    def append(self, image_filename):
        _hash = get_hash(os.path.join(self.image_lib_path, image_filename))
        pair = _hash, image_filename
        self.hashes.append(pair)

        for cur_hash, f in self.hashes:
            if self._resemble(_hash, cur_hash):
                self.img_set.union(pair, (cur_hash, f))
        self.img_set.union(pair, pair)


    def _resemble(self, h1, h2):
        return bin(h1 ^ h2).count('1') <= self.confidence


    def _query(self, _hash):
        for h, f in self.hashes:
            if self._resemble(h, _hash):
                pair = self.img_set.get_equiv_elem((h, f))
                return self.img_set.d[self.img_set.get_equiv_elem(pair)]

        return []


    def query(self, image_handle=None, image_path=None, image_url=None, image_hash=None):
        print 'in query'
        if image_hash:
            print 'image hash'
            return self._query(image_hash)

        if image_handle:
            print 'image handle'
            return self._query(get_hash(image_handle))

        if image_path:
            print 'image path'
            return self._query(get_hash(image_path))

        if image_url:
            print 'image url'
            print 'retrieving image from %s' % image_url
            raw_image = urllib2.urlopen(image_url).read()
            print 'image retrieved'

            image_handle = StringIO(raw_image)
            return self._query(get_hash(image_handle))

        return []


    def all(self):
        return reduce(operator.or_, self.img_set.d.values(), set())


    def get_thumbnail(self, filename, size=(75, 75), anti_alias=True):
        path = os.path.realpath(os.path.join(self.image_lib_path, filename))

        image = Image.open(path)
        image.thumbnail(size, Image.ANTIALIAS if anti_alias else Image.NEAREST)

        thumbnail = StringIO()
        image.save(thumbnail, image.format)
        thumbnail.seek(0)

        return thumbnail

