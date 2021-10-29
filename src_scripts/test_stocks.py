import stocks_2 as stk
import pandas as pd
import unittest   # The test framework
mystock = stk.stock('JNJ')


class Test_TestIncrementDecrement(unittest.TestCase):


    def test_summary(self):
        self.assertEqual(mystock.info['shortName'], 'Johnson & Johnson')
        print(mystock.info['shortName'])

    def test_bid_ask(self):
        self.assertIsNotNone(mystock.get_bid_ask())
        self.assertIs(type(mystock.get_bid_ask()[1]),type(162.35))

    def test_period(self):
        x = '6mo'
        mystock.__set_period__(x)
        self.assertEqual(mystock.period,x)
    
    def test_interval(self):
        x = '5m'
        mystock.__set_interval__(x)
        self.assertEqual(mystock.interval,x)

    def test_set_ohlc(self):
        x = '1m'
        mystock.__set_interval__(x)
        y = '1d'
        mystock.__set_period__(y)
        mystock.set_ohlc_data()
        a = mystock.get_ohlc().index[2] - mystock.get_ohlc().index[1]
        self.assertEqual(a.total_seconds(),float(60))


    





        
        
if __name__ == '__main__':
    unittest.main()


