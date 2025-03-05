class MissingLLMResponseKeyError(Exception):
    def __init__(self, key):
        super().__init__(f"Missing expected key '{key}' in llm_response.")