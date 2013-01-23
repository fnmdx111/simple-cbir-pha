from collections import defaultdict

class DisjointSet(object):
    def __init__(self):
        self.d = defaultdict(set)


    def insert(self, value, father):
        father_equiv_elem = self.get_equiv_elem(father)
        value_equiv_elem = self.get_equiv_elem(value)

        if father_equiv_elem and father_equiv_elem == value_equiv_elem:
            return

        if father_equiv_elem:
            if value_equiv_elem:
                self.d[father_equiv_elem] |= self.d[value_equiv_elem]
                del self.d[value_equiv_elem]
            else:
                self.d[father_equiv_elem].add(value)
        else:
            if value_equiv_elem:
                self.d[value_equiv_elem].add(father)
            else:
                self.d[father].add(value)
                self.d[father].add(father)


    def sets(self):
        return self.d.values()


    def get_equiv_elem(self, value):
        for key, values in self.d.iteritems():
            if value in values:
                return key
        return None


    def query(self, value1, value2):
        return self.get_equiv_elem(value1) == self.get_equiv_elem(value2)


    def __iter__(self):
        return iter(self.d.values())



if __name__ == '__main__':
    disjoint_set = DisjointSet()
    disjoint_set.insert(1, 1)
    disjoint_set.insert(2, 1)
    disjoint_set.insert(3, 1)
    disjoint_set.insert(5, 4)
    print disjoint_set.query(1, 2)
    print disjoint_set.query(3, 5)
    print disjoint_set.query(4, 5)
    print disjoint_set.query(6, 4)
    print disjoint_set.sets()
