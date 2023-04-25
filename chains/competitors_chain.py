from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
import prompt_loader
from typing import Dict, List
import re


class CompetitorsChain(Chain):
    @property
    def input_keys(self) -> List[str]:
        return ['ticker_symbol', 'product_market']

    @property
    def output_keys(self) -> List[str]:
        return ['competitors']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        llm = ChatOpenAI(temperature=0.2, max_tokens=200)

        competitors_prompt: PromptTemplate = prompt_loader.load_prompt('competitors_prompt.txt', ['ticker_symbol', 'product_market'])
        competitors_response = LLMChain(llm=llm, prompt=competitors_prompt).run({'ticker_symbol': inputs['ticker_symbol'], 'product_market': inputs['product_market']}).replace(" ", "")
        
        if not re.match("^[A-Za-z]+[,a-zA-Z]*", competitors_response): #TODO: debug
            return {'competitors': None}
        
        return {'competitors': competitors_response}