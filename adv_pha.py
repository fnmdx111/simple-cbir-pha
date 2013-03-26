import cv2
import os
import numpy
from itertools import product, combinations

block_row_idx, block_col_idx = map(lambda end: range(0, end, 8), (480, 640))
block_coordinates = tuple(product(block_row_idx, block_col_idx))


def get_dct(filename='0.jpg'):
    img = cv2.imread(os.path.join('images', filename), cv2.CV_LOAD_IMAGE_GRAYSCALE)
    h, w = img.shape

    ret = numpy.ndarray(h * w / 64, dtype=numpy.dtype((numpy.float32, (8, 8))))
    mat = numpy.zeros((8, 8), numpy.float32)
    for r, c in block_coordinates:
        mat[:8, :8] = img[r:r + 8, c:c + 8]
        dct = cv2.dct(mat)
        ret[r + c / 8][:, :] = dct

    return ret


def get_useful_dc_comp(dct_mat, n=128):
    return numpy.array(map(lambda dct: dct[0, 0], dct_mat)[:n if n else None])


def sort_dc_comp(dc_vector, key=abs):
    return numpy.array(sorted(dc_vector, key=key, reverse=True))


def cosine(v1, v2):
    return 1 - v1.dot(v2) / numpy.sqrt(v1.dot(v1) * v2.dot(v2))


def relative_relation_hash(v):
    return reduce(lambda (h, last), cur: (h << 1 | (1 if last < cur else 0), cur),
                  v,
                  (0, -2147483647))[0]


def relative_relation_hash_match(h1, h2):
    return bin(h1 ^ h2).count('1')



if __name__ == '__main__':
    norm = numpy.linalg.norm

    features = []
    for filename in os.listdir('images'):
        dct_mat = get_dct(filename)

        dc_vector = get_useful_dc_comp(dct_mat, n=0)
        all_dc_vec_hash = relative_relation_hash(dc_vector)

        sorted_dc_vector = sort_dc_comp(dc_vector)
        dc_vector = dc_vector[:128]
        dc_vec_hash = relative_relation_hash(dc_vector)

        # dc_vector = sort_dc_comp(dc_vector)
        features.append((filename,
                         sorted_dc_vector[:128],
                         dc_vec_hash,
                         all_dc_vec_hash))
    for fn, v, h, a_h in features:
        print fn
        print 'norm of v:   ', norm(v)
        print '128bit hash: ', hex(h)
        print '7500bit hash:', hex(a_h)
        print 'variance:    ', numpy.var(v)

    print '% 5s % 5s | % 6s, % 7s, % 8s, % 3s' % ('fn1', 'fn2', 'euc_d', 'cos_v', 'rel_hash', 'all_rel_hash')
    norms = []
    for (fn1, v1, h1, a_h1), (fn2, v2, h2, a_h2) in combinations(features, r=2):
        n = norm(v1 - v2)
        print '% 5s % 5s | %5.1f, %0.5f, % 8d, % 4d' % (fn1, fn2,
                                                        n,
                                                        cosine(v1, v2),
                                                        relative_relation_hash_match(h1, h2),
                                                        relative_relation_hash_match(a_h1, a_h2),
                                                        )
        norms.append((n,
                      cosine(v1, v2),
                      relative_relation_hash_match(h1, h2),
                      relative_relation_hash_match(a_h1, a_h2),
                      fn1, fn2))
    for n, c, r, ra, fn1, fn2 in sorted(norms, key=lambda (n, c, r, ra, fn1, fn2): n):
        print  fn1, ',', fn2, '|', n, c, r, ra


