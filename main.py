# encoding: utf-8

from itertools import combinations
import os
from lib import pha
from lib.constants import IMAGE_LIBRARY_PATH as image_lib_path, confidence
from lib.disjoint_set import DisjointSet


if __name__ == '__main__':
    hashes, img_set = [], DisjointSet()
    for filename in os.listdir(image_lib_path):
        hash = pha.get_hash(os.path.join(image_lib_path, filename))
        hashes.append((hash, filename.decode('gbk').encode('utf-8')))

    for pair in hashes:
        img_set.union(pair, pair)

    for (h1, f1), (h2, f2) in combinations(hashes, 2):
        cnt = bin(h1 ^ h2).count('1')
        if cnt <= confidence:
            img_set.union((h1, f1), (h2, f2))


        print '-' * 64
        print '%016x' % h1, '%016x' % h2
        print '% 16s' % f1, '% 16s' % f2
        print 'similarity: %2.2f%%' % (((64 - cnt) / 64.) * 100)
        print '{0:064b}'.format(h1 ^ h2)
        print '-' * 64

    for s in img_set:
        print s

    print '% 30s % 30s' % ('value', 'key')
    for pair in img_set.inverse.iteritems():
        print map(lambda (h, f): ('%016x' % h, f), pair)
