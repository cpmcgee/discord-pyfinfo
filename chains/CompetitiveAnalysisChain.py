from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
import prompt_loader
import json
import data_fetcher
from typing import Dict, List


class CompetitiveAnalysisChain(Chain):
    ticker_symbol: str
    product_market: str

    def __init__(self, ticker_symbol, product_market):
        self.ticker_symbol = ticker_symbol
        self.instance_variable_2 = product_market

    @property
    def input_keys(self) -> List[str]:
        return ['ticker_symbol', 'product_market']

    @property
    def output_keys(self) -> List[str]:
        return ['competitive_analysis']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        llm = ChatOpenAI(temperature=0.2, max_tokens=200)

        #TODO: Break into separate custom chain w/ validation
        competitors_prompt: PromptTemplate = prompt_loader.load_prompt('competitors_prompt.txt', ['ticker_symbol', 'product_market'])
        competitor_ticker_symbols = LLMChain(llm=llm, prompt=competitors_prompt).run({'ticker_symbol': self.ticker_symbol, 'product_market': self.product_market})
        all_ticker_symbols = competitor_ticker_symbols + self.ticker_symbol

        financial_metrics = data_fetcher.get_financial_metrics(all_ticker_symbols)
        financial_metrics_str = json.dumps(financial_metrics.__dict__)

        competitive_analysis_prompt: PromptTemplate = prompt_loader.load_prompt('competitive_analysis_prompt.txt', ['ticker_symbol', 'financial_metrics', 'product_market'])
        competitive_analysis = LLMChain(llm=llm, prompt=competitive_analysis_prompt).run({'ticker_symbol': self.ticker_symbol, 'financial_metrics': financial_metrics_str, 'product_market': self.product_market})

        return {'competitive_analysis': competitive_analysis}