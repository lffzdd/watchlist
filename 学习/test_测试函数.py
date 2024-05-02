from 测试函数 import *
import unittest


class TestFunctions(unittest.TestCase):
    def setUp(self):  # 每个测试函数执行前都会执行
        print('setUp')
        self.a = 1
        self.b = 2

    def tearDown(self):  # 每个测试函数执行后都会执行
        print('tearDown')
        del self.a
        del self.b

    def test_add(self):
        self.assertEqual(add(self.a, self.b), 3)
        # self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(self.a, self.b), -1)
        # self.assertEqual(subtract(-1, 1), -2)

    def test_multiply(self):
        self.assertEqual(multiply(self.a, self.b), 2)
        # self.assertEqual(multiply(-1, 1), -1)

    def test_divide(self):
        self.assertEqual(divide(self.a, self.b), 0.5)
        with self.assertRaises(ValueError):
            divide(1, 0)
        self.assertRaises(ValueError, divide, 1, 0)  # 与上面等价


# python -m unittest 测试函数.py
if __name__ == '__main__':
    unittest.main()
