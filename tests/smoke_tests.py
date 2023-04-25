import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from models.valuation_metrics import ValuationMetrics
from models.price_info import PriceInfo
import message_generator
import json
import os

class SmokeTests(TestCase):

    # Dummy data for mocks

    dummy_valuation_metrics = [
            ValuationMetrics(
                asset_name="Microsoft Corporation",
                symbol="MSFT",
                ttm_pe_ratio=31.715872,
                market_cap=2127140356096,
                price_to_book=11.62004,
                ttm_peg_ratio=2.1255
            ),
            ValuationMetrics(
                asset_name="Amazon Inc.",
                symbol="AAPL",
                ttm_pe_ratio=28.965872,
                market_cap=2837140356096,
                price_to_book=39.34,
                ttm_peg_ratio=3.37
            ),
            ValuationMetrics(
                asset_name="Amazon.com, Inc.",
                symbol="AMZN",
                ttm_pe_ratio=50.30,
                market_cap=1097140356096,
                price_to_book=12.00,
                ttm_peg_ratio=2.97
            )
        ]
    
    dummy_msft_price_info = [
        PriceInfo(
            asset_name="Microsoft Corporation",
            symbol="MSFT",
            day_last_price=285.75,
            day_open_price=284.25,
            day_high_price=286.83,
            day_low_price=283.34
        )
    ]

    dummy_eth_price_info = [
        PriceInfo(
            asset_name="Ethereum",
            symbol="ETH-BTC",
            day_last_price=0.0659356960,
            day_open_price=0.0640275940,
            day_high_price=0.0660883952,
            day_low_price=0.0630280690
        )
    ]

    # Setup methods

    @classmethod
    def setUpClass(self):
        config = json.load(open('config.json'))
        os.environ["OPENAI_API_KEY"] = config['openai_api_key']
        message_generator.config = config


    def setUp(self):
        #runs prior to each test
        None

    # Tests

    @patch("data_sources.data_fetcher.get_price_infos", Mock(return_value=dummy_msft_price_info))
    def test_traditional_asset_price_info(self):
        msg = message_generator.get_price_info_msg("MSFT")
        print(msg)
        self.assertIsNotNone(msg)
        self.assertGreater(len(msg), 0)
        self.assertNotRegex(msg, "I ran into a problem")


    @patch("data_sources.data_fetcher.get_price_infos", Mock(return_value=dummy_eth_price_info))
    def test_crypto_asset_price_info(self):
        msg = message_generator.get_price_info_msg("ETH-BTC")
        print(msg)
        self.assertIsNotNone(msg)
        self.assertGreater(len(msg), 0)   
        self.assertNotRegex(msg, "I ran into a problem")


    @patch("data_sources.data_fetcher.get_valuation_metrics", Mock(return_value=dummy_msft_price_info))
    def test_competitive_analysis(self):
        msg = message_generator.get_competitive_analysis_msg("MSFT", "cloud computing")
        print(msg)
        self.assertIsNotNone(msg)
        self.assertGreater(len(msg), 0)
        self.assertNotRegex(msg, "I ran into a problem")


    def test_chat_response_message(self):
        msg = message_generator.get_chat_response_msg("What is your name?")
        print(msg)
        self.assertIsNotNone(msg)
        self.assertGreater(len(msg), 0)
        self.assertNotRegex(msg, "I ran into a problem")


    def test_news_message(self):
        msg = message_generator.get_latest_news_msg("MSFT", 5)
        print(msg)
        self.assertIsNotNone(msg['content'])
        self.assertNotRegex(msg['content'], "I ran into a problem")
    


if __name__ == '__main__':
    unittest.main()