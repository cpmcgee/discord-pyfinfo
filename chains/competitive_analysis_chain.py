import dataclasses
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
import prompt_loader
import json
import data_sources.data_fetcher as data_fetcher
from typing import Dict, List
from chains.competitors_chain import CompetitorsChain


class CompetitiveAnalysisChain(Chain):
    @property
    def input_keys(self) -> List[str]:
        return ['ticker_symbol', 'product_market']

    @property
    def output_keys(self) -> List[str]:
        return ['competitive_analysis']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        llm = ChatOpenAI(temperature=0.2, max_tokens=200)

        competitors_response = CompetitorsChain().run({'ticker_symbol': inputs['ticker_symbol'], 'product_market': inputs['product_market']})
        
        if competitors_response is None: #TODO: debug
            return {'competitive_analysis': f"{inputs['ticker_symbol']} does not compete in {inputs['product_market']}"}

        all_ticker_symbols = competitors_response.replace(" ", "").split(",") + [inputs['ticker_symbol']]

        financial_metrics = data_fetcher.get_valuation_metrics(all_ticker_symbols)
        financial_metrics_str = json.dumps([dataclasses.asdict(f) for f in financial_metrics])

        competitive_analysis_prompt: PromptTemplate = prompt_loader.load_prompt('competitive_analysis_prompt.txt', ['ticker_symbol', 'financial_metrics', 'product_market'])
        competitive_analysis = LLMChain(llm=llm, prompt=competitive_analysis_prompt).run({'ticker_symbol': inputs['ticker_symbol'], 'financial_metrics': financial_metrics_str, 'product_market': inputs['product_market']})

        return {'competitive_analysis': competitive_analysis}