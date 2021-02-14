import yfinance as yf
import unittest, os

# To run tests: 
# . .local_env.sh
# python test/yfiance_test.py

class YFinanceTest(unittest.TestCase):
    def test1(self):
        btc = yf.Ticker("BTC-USD")
        curr = btc.history(period="1d")
        print(curr["Close"][0])

if __name__ == '__main__':
    unittest.main()
