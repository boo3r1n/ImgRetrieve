import openai
from dataclasses import dataclass

@dataclass
class OpenAI:
    model_name: str = "gpt-3.5-turbo-1106"
    temperature: float = 0.0
    top_p: float = 1.0
    streaming: bool = False
    
    def call(self, prompt):
        return openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            top_p=self.top_p,
            stream=self.streaming,
        )

