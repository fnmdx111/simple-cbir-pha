# encoding: utf-8

from collections import defaultdict

class DisjointSet(object):
    def __init__(self):
        self.d = defaultdict(set)
        self.inverse = {}


    def _register(self, father, elem):
        self.d[father].add(elem)
        self.inverse[elem] = father


    def _init_set(self, equiv_elem):
        s = self.d[equiv_elem]
        if not s:
            s.add(equiv_elem)
            self.inverse[equiv_elem] = equiv_elem


    def union(self, elem1, elem2):
        equiv_elem1 = self.get_equiv_elem(elem1)
        equiv_elem2 = self.get_equiv_elem(elem2)

        self._init_set(equiv_elem2)
        self._init_set(equiv_elem1)

        if equiv_elem2 == equiv_elem1:
            pass
        else:
            self.d[equiv_elem2] |= self.d[equiv_elem1]
            self.inverse.update(
                {elem: equiv_elem2 for elem in self.d[equiv_elem1]}
            )
            del self.d[equiv_elem1]


    def sets(self):
        return self.d.values()


    def get_equiv_elem(self, elem):
        for equiv_elem, elements in self.d.iteritems():
            if elem in elements:
                return equiv_elem
        return elem


    def query(self, elem1, elem2):
        return self.get_equiv_elem(elem1) == self.get_equiv_elem(elem2)


    def __iter__(self):
        return iter(self.d.values())



if __name__ == '__main__':
    disjoint_set = DisjointSet()
    disjoint_set.union(1, 1)
    disjoint_set.union(2, 1)
    disjoint_set.union(3, 1)
    disjoint_set.union(5, 4)
    print disjoint_set.query(1, 2)
    print disjoint_set.query(3, 5)
    print disjoint_set.query(4, 5)
    print disjoint_set.query(6, 4)
    print disjoint_set.sets()

    print disjoint_set.inverse

