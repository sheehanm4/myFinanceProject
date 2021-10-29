import stocks_2 as stk

mystock = stk.stock('JNJ')

import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_summary(self):
        self.assertEqual(mystock.info['shortName'], 'Johnson & Johnson')
        
        
if __name__ == '__main__':
    unittest.main()


