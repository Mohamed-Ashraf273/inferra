class LLM:
    def __init__(self, model_name: str, api_key: str = None, temperature: float = 0.1):
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.model = None
