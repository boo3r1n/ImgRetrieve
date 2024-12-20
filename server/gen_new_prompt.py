from modules.language_model import OpenAI
from modules.qa_generator import QAGenerator
from dotenv import load_dotenv
import openai
import os
import argparse
import json

if __name__ == '__main__':
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE") 

    parser = argparse.ArgumentParser()
    parser.add_argument("--chat_model", type=str, default="openai")
    parser.add_argument("--k", type=int, default="5")

    args = parser.parse_args()

    chat_model = args.chat_model
    k=args.k
    chat_model_mapping = {                                                                                                                  
            "openai": OpenAI(model_name='gpt-3.5-turbo', temperature=0.0),
            "openai-16k": OpenAI(model_name='gpt-3.5-turbo-16k', temperature=0.0),
            "openai-gpt4": OpenAI(model_name='gpt-4-1106-preview', temperature=0.0),
        }
    
    llm = chat_model_mapping[chat_model]
    qa_generator = QAGenerator(llm)
    new_prompt = qa_generator.get_new_prompt("A cat")
    print("New prompt is: ", new_prompt)
    new_color = qa_generator.get_new_color(["#493826", "#f36b55", "#735347", "#2e2219", "#c81a26"], "I like more blue")
    print("New color is: ", new_color)