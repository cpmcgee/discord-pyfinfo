from typing import List
from langchain import PromptTemplate

#TODO: use built in prompt loader instead of this
def load_prompt(file_name: str, input_vars: List[str]) -> PromptTemplate:
    with open(file_name, "r") as f:
        t = f.read()
        return PromptTemplate(
            input_variables = input_vars,
            template = t
        )