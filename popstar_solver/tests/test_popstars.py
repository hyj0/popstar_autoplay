import unittest
import popstars


class TestPopstarsNodes(unittest.TestCase):

    def setUp(self):
        self.node = popstars.PopstarsNode([['B', 'B', 'R', 'P', 'G', 'Y'],
                                           ['G', 'Y', 'G', 'G', 'R', 'R'],
                                           ['B', 'B', 'G', 'P', 'G', 'G'],
                                           ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                           ['G', 'Y', 'P', 'G', 'R', 'R'],
                                           ['Y', 'R', 'Y', 'B', 'Y', 'B']])
        self.solver = popstars.PopstarsSolver(self.node)

    def test_calc_new_status(self):
        assert self.node.calc_new_status([(1, 2), (1, 3), (2, 2),
                                          (3, 2), (3, 3), (4, 3)]) == [
            ['B', 'B', '',  '', 'G', 'Y'],
            ['G', 'Y', '',  '', 'R', 'R'],
            ['B', 'B', '',  '', 'G', 'G'],
            ['R', 'Y', 'R', 'P', 'Y', 'P'],
            ['G', 'Y', 'P', 'P', 'R', 'R'],
            ['Y', 'R', 'Y', 'B', 'Y', 'B']]
        assert self.node.calc_new_status([(0, 2), (1, 2), (1, 3), (2, 2),
                                          (3, 2), (3, 3), (4, 2), (4, 3),
                                          (5, 2)]) == [
            ['B', 'B', '',  'G', 'Y'],
            ['G', 'Y', '',  'R', 'R'],
            ['B', 'B', '',  'G', 'G'],
            ['R', 'Y', 'P', 'Y', 'P'],
            ['G', 'Y', 'P', 'R', 'R'],
            ['Y', 'R', 'B', 'Y', 'B']]

    def test_convert_coordinations(self):
        assert self.node.convert_coordinations([(0, 0)]) == [(0, 5)]
        assert self.node.convert_coordinations([(3, 2)]) == [(2, 2)]

    def test_find_next_moves(self):
        result = list(self.node.find_next_moves())
        assert len(result) == 7
        assert ([(0, 3), (1, 3)], 20, [['',  '',  'R', 'P', 'G', 'Y'],
                                       ['B', 'B', 'G', 'G', 'R', 'R'],
                                       ['G', 'Y', 'G', 'P', 'G', 'G'],
                                       ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                       ['G', 'Y', 'P', 'G', 'R', 'R'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result
        assert ([(0, 5), (1, 5)], 20, [['',  '',  'R', 'P', 'G', 'Y'],
                                       ['G', 'Y', 'G', 'G', 'R', 'R'],
                                       ['B', 'B', 'G', 'P', 'G', 'G'],
                                       ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                       ['G', 'Y', 'P', 'G', 'R', 'R'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result
        assert ([(1, 1), (1, 2)], 20, [['B', '',  'R', 'P', 'G', 'Y'],
                                       ['G', '',  'G', 'G', 'R', 'R'],
                                       ['B', 'B', 'G', 'P', 'G', 'G'],
                                       ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                       ['G', 'B', 'P', 'G', 'R', 'R'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result
        assert ([(2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4)],
                180, [['B', 'B', '',  '',  'G', 'Y'],
                      ['G', 'Y', '',  '',  'R', 'R'],
                      ['B', 'B', '',  '',  'G', 'G'],
                      ['R', 'Y', 'R', 'P', 'Y', 'P'],
                      ['G', 'Y', 'P', 'P', 'R', 'R'],
                      ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result
        assert ([(4, 1), (5, 1)], 20, [['B', 'B', 'R', 'P', '',  ''],
                                       ['G', 'Y', 'G', 'G', 'G', 'Y'],
                                       ['B', 'B', 'G', 'P', 'R', 'R'],
                                       ['R', 'Y', 'G', 'G', 'G', 'G'],
                                       ['G', 'Y', 'P', 'G', 'Y', 'P'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result
        assert ([(4, 3), (5, 3)], 20, [['B', 'B', 'R', 'P', '',  ''],
                                       ['G', 'Y', 'G', 'G', 'G', 'Y'],
                                       ['B', 'B', 'G', 'P', 'R', 'R'],
                                       ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                       ['G', 'Y', 'P', 'G', 'R', 'R'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result
        assert ([(4, 4), (5, 4)], 20, [['B', 'B', 'R', 'P', '',  ''],
                                       ['G', 'Y', 'G', 'G', 'G', 'Y'],
                                       ['B', 'B', 'G', 'P', 'G', 'G'],
                                       ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                       ['G', 'Y', 'P', 'G', 'R', 'R'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) in result

    def test_find_result(self):
        assert self.solver.search() == 2405
        print(self.solver.find_result())


class TestPopstarsNodes2(unittest.TestCase):

    def setUp(self):
        self.node = popstars.PopstarsNode([['',  '',  'R', 'P', 'G', 'Y'],
                                           ['B', 'B', 'G', 'G', 'R', 'R'],
                                           ['G', 'Y', 'G', 'P', 'G', 'G'],
                                           ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                           ['G', 'Y', 'P', 'G', 'R', 'R'],
                                           ['Y', 'R', 'Y', 'B', 'Y', 'B']])

    def test_find_next_moves(self):
        result = list(self.node.find_next_moves())
        assert ([(0, 5), (1, 5)], 20, [['',  '',  'R', 'P', 'G', 'Y'],
                                       ['G', 'Y', 'G', 'G', 'R', 'R'],
                                       ['B', 'B', 'G', 'P', 'G', 'G'],
                                       ['R', 'Y', 'G', 'G', 'Y', 'P'],
                                       ['G', 'Y', 'P', 'G', 'R', 'R'],
                                       ['Y', 'R', 'Y', 'B', 'Y', 'B']]) not in result


class TestPopstarsNodes3(unittest.TestCase):

    def setUp(self):
        self.node = popstars.PopstarsNode([['Y', 'B', 'Y'],
                                           ['B', 'B', 'Y']])
        self.solver = popstars.PopstarsSolver(self.node)

    def test_find_next_moves(self):
        result = list(self.node.find_next_moves())
        assert len(result) == 2
        assert ([(0, 0), (1, 0), (1, 1)], 45, [['', 'Y'],
                                               ['Y', 'Y']]) in result
        assert ([(2, 0), (2, 1)], 20, [['Y', 'B'],
                                       ['B', 'B']]) in result

    def test_convert_coordinations(self):
        assert self.node.convert_coordinations([(0, 0)]) == [(0, 1)]
        assert self.node.convert_coordinations([(0, 1)]) == [(1, 1)]
        assert self.node.convert_coordinations([(0, 2)]) == [(2, 1)]
        assert self.node.convert_coordinations([(1, 0)]) == [(0, 0)]
        assert self.node.convert_coordinations([(1, 1)]) == [(1, 0)]
        assert self.node.convert_coordinations([(1, 2)]) == [(2, 0)]

    def test_find_result(self):
        assert self.solver.search() == 2090
        print(self.solver.find_result())
        # assert 0


class TestPopstarsSolver(unittest.TestCase):

    def setUp(self):
        start_node = popstars.PopstarsNode([['P', 'G', 'Y'],
                                            ['G', 'R', 'R'],
                                            ['P', 'G', 'G']])
        self.solver = popstars.PopstarsSolver(start_node)

    def test_find_result(self):
        assert self.solver.search() == 2100
        print(self.solver.find_result())
