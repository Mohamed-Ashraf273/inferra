from langchain_groq import ChatGroq

from inferra.src.llms.llm import LLM


class GroqModel(LLM):
    def __init__(self, model_name: str, api_key: str, temperature: float = 0.1):
        super().__init__(model_name, api_key=api_key, temperature=temperature)
        self.model = ChatGroq(
            model=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
        )
