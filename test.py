import unittest
from pyfsr import FSRFunction, LFSR, NLFSR


class TestFSRFunction(unittest.TestCase):
    def test_xor(self):
        func = FSRFunction([0,1,"+"])
        self.assertEqual(func.solve([0,0]), 0)
        self.assertEqual(func.solve([1,0]), 1)
        self.assertEqual(func.solve([0,1]), 1)
        self.assertEqual(func.solve([1,1]), 0)

    def test_and(self):
        func = FSRFunction([0,1,"*"])
        self.assertEqual(func.solve([0,0]), 0)
        self.assertEqual(func.solve([1,0]), 0)
        self.assertEqual(func.solve([0,1]), 0)
        self.assertEqual(func.solve([1,1]), 1)

    def test_expression_order(self):
        func = FSRFunction([0,1,2, "+", "+"])
        self.assertEqual(func.solve([0,1,0]), 1)
        func = FSRFunction([0,1, "+",2, "+"])
        self.assertEqual(func.solve([0,1,0]), 1)
        func = FSRFunction([0,1,2, "*", "+"])
        self.assertEqual(func.solve([1,1,0]), 1)
        self.assertEqual(func.solve([0,1,0]), 0)
        func = FSRFunction([0,1,2, "+", "*"])
        self.assertEqual(func.solve([1,1,0]), 1)
        self.assertEqual(func.solve([0,1,0]), 0)

    def test_raise_exception(self):
        func = FSRFunction([0,1,"+"])
        with self.assertRaises(Exception):
            func.solve([1])
        with self.assertRaises(Exception):
            func = FSRFunction([0,1])
        with self.assertRaises(Exception):
            func = FSRFunction([0, "+"])
        with self.assertRaises(Exception):
            func = FSRFunction([0,1, "+", "+"])

class TestLFSR(unittest.TestCase):

    def test_simple_cycle(self):
        l = LFSR(poly=[3,2], initstate=[0,1,1], initcycles=3)
        self.assertListEqual(l.state.tolist(), [0,1,0])
        self.assertEqual(l.shift(), 0)
        self.assertListEqual(l.state.tolist(), [1,0,1])
        self.assertEqual(l.shift(), 1)
        self.assertListEqual(l.state.tolist(), [1,1,0])
        self.assertEqual(l.shift(), 0)
        self.assertListEqual(l.state.tolist(), [1,1,1])
        self.assertEqual(l.shift(), 1)
        self.assertListEqual(l.state.tolist(), [0,1,1])

    def test_raise_exception(self):
        with self.assertRaises(Exception):
            LFSR(poly=[3,2], initstate=[0])
        with self.assertRaises(Exception):
            LFSR(poly=[3,2], initstate=[0,0,0,0])

class TestNLFSR(unittest.TestCase):
    def test_simple_cycle(self):
        infunc = FSRFunction([0,1,2, "*", "+"])
        nl = NLFSR(initstate="ones", infunc=infunc, size=3)
        self.assertListEqual(nl.state.tolist(), [1,1,1])
        self.assertEqual(nl.shift(), 1)
        self.assertListEqual(nl.state.tolist(), [0,1,1])
        self.assertEqual(nl.shift(), 1)
        self.assertListEqual(nl.state.tolist(), [1,0,1])
        self.assertEqual(nl.shift(), 1)
        self.assertListEqual(nl.state.tolist(), [1,1,0])
        self.assertEqual(nl.shift(), 0)
        self.assertListEqual(nl.state.tolist(), [1,1,1])

    def test_raise_exception(self):
        infunc = FSRFunction([0,1,2, "*", "+"])
        with self.assertRaises(Exception):
             nl = NLFSR(initstate="random", infunc=infunc)
        nl = NLFSR(initstate=[0,1], infunc=infunc)
        with self.assertRaises(Exception):
            nl.shift()
        nl = NLFSR(initstate="random", infunc=infunc, outfunc=FSRFunction([5]), size=1)
        with self.assertRaises(Exception):
            nl.shift()


if __name__ == '__main__':
    unittest.main()
