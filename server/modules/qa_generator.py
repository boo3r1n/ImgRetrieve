from modules.language_model import OpenAI
from dotenv import load_dotenv
import openai
import os
import argparse
import json
import ast

class QAGenerator:
    def __init__(self,llm):
        self.llm=llm
    def get_new_prompt(self, text):
        prompt=f"""You are a creative assistant specializing in detailed scene descriptions.
        I want to generate a photo that captures the essence of '{text}'. For this purpose, I need "6 detailed explanations" to be generated in a JSON format.
Each explanation should vividly describe the content of '{text}' from unique and diverse perspectives, ensuring a rich and clear visualization.
Please include in each description a series of specific, visually descriptive keywords, separated by commas. Aim for each explanation to contain more than 10 such keywords.
Focus on translating the abstract and fuzzy aspects of '{text}' into concrete, vivid, and pictorial descriptions that clearly convey distinct scenes or elements.
The structure of the output should be an array of explanations, formatted as:[{{prompt:"description1"}}, {{prompt:"description2"}}, ...], where each array element is a string of descriptive keywords.
Emphasize the inclusion of tangible details like colors, objects, activities, and settings in the descriptions to ensure they are directly translatable into visual imagery.
Avoid vague or generic terms, opting instead for descriptions that provide a clear and immediate mental picture, suitable for creating detailed and varied images.
Consider cultural, historical, futuristic, and fantasy elements where applicable to '{text}', to offer a broad spectrum of visual interpretations.
Ensure that the explanations are diverse in theme and style, each painting a unique picture of '{0}' that stands out distinctly from the others.
The goal is to create prompts that are ready to be input into an AI image generation model, capable of producing distinct and accurate visual representations of each explanation.
Each prompt should be less than "20 words long"
        """
        response = self.llm.call(prompt)
        new_prompt = response.choices[0].message['content']
        return new_prompt
    def get_new_color(self, color_palette, user_input):
        prompt = f"""
                You are an expert in color theory and design.
                Here is the original color palette consisting of five colors in HEX format:{color_palette}
                I now want to generate a discrete palette with as much contrast between the colors as possible and alternating between light and dark.
Please help me pick 5 colors from these, and finally form a harmonious palette.
Then make subtle adjustments to this palette based on  {user_input} and color theory, focusing on lightness and chroma, rather than overhauling the entire palette.
                Your task is to modify the palette to align with the user's request, while maintaining overall aesthetic coherence.
                Ensure the new palette also contains exactly five colors, returned as a Python list of HEX values.
                Please keep the following format and no other answer needed, here is an format sample: 
                ['#000000', '#000000', '#000000', '#000000', '#000000']
        """


        response = self.llm.call(prompt)
        new_color_palette_str = response.choices[0].message['content']
        try:
            new_color_palette = ast.literal_eval(new_color_palette_str)
        # 验证解析结果是否为列表且包含合法 HEX 值
            if isinstance(new_color_palette, list) and all(
                isinstance(color, str) and color.startswith("#") and len(color) == 7
            for color in new_color_palette
            ):
                return new_color_palette
            else:
                raise ValueError("Generated palette is not valid.")
        except (SyntaxError, ValueError):
            raise ValueError(f"Failed to parse the color palette: {new_color_palette_str}")

