import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from chains.competitive_analysis_chain import CompetitiveAnalysisChain
from models.financial_metrics import FinancialMetrics
import json
import os

class SmokeTests(TestCase):

    dummy_data = [
            FinancialMetrics(
                asset_name="Microsoft Corporation",
                symbol="MSFT",
                ttm_pe_ratio=31.715872,
                market_cap=2127140356096,
                price_to_book=11.62004,
                ttm_peg_ratio=2.1255
            ),
            FinancialMetrics(
                asset_name="Amazon Inc.",
                symbol="AAPL",
                ttm_pe_ratio=28.965872,
                market_cap=2837140356096,
                price_to_book=39.34,
                ttm_peg_ratio=3.37
            ),
            FinancialMetrics(
                asset_name="Amazon.com, Inc.",
                symbol="AMZN",
                ttm_pe_ratio=50.30,
                market_cap=1097140356096,
                price_to_book=12.00,
                ttm_peg_ratio=2.97
            )
        ]


    @classmethod
    def setUpClass(self):
        config = json.load(open('config.json'))
        os.environ["OPENAI_API_KEY"] = config['openai_api_key']

    def setUp(self):
        #runs prior to each test
        None

    #@patch("data.data_fetcher.get_financial_metrics", Mock(return_value=dummy_data))
    def test_competitive_analysis(self):
        chain = CompetitiveAnalysisChain()
        msg = chain.run({"ticker_symbol": "MSFT", "product_market": "cloud computing"})
        print(msg)

if __name__ == '__main__':
    unittest.main()