import os
from flask import send_file, jsonify, url_for
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.colors as mcolors
from flask import Flask, request
from flask_cors import CORS
from CLIPImage import matching
from PIL import Image, ImageFile
from modules.language_model import OpenAI
from modules.qa_generator import QAGenerator
from dotenv import load_dotenv
import openai
import argparse

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return '后端服务器已启动'

@app.route('/new-colors', methods=['POST'])
def new_colors():
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
    data = request.get_json()
    color_palette = data.get('color_palette')  # color_palette 必须在请求中
    new_color_prompt = data.get('prompt')  # 用户优化调色板的输入

    if not color_palette:
        return jsonify({"error": "Invalid or missing color_palette"}), 400

    # 调用调色板优化方法
    new_colors = qa_generator.get_new_color(color_palette, new_color_prompt)
    return jsonify({"new_colors": new_colors})

@app.route('/text-to-image', methods=['POST'])
def text_to_image():
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
    data = request.get_json()
    if not data or 'text' not in data or not data['text'].strip():  # 如果缺少 `text` 参数或为空
        text = 'a cat' 
    else:
        text = data.get('text', '')
 
    new_text=qa_generator.get_new_prompt(text)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image_folder = 'static/imgs' 
    result_path = matching(new_text, image_folder)
    if not os.path.exists(result_path):
        return jsonify({"error": "Retrieved image not found"}), 404

    top_colors = get_top_colors(result_path)

    relative_path = os.path.relpath(result_path, 'static')
    return jsonify({
        "image_url": url_for('static', filename=relative_path, _external=True),
        "top_colors": top_colors,
        "detailed_description": new_text
    })

def get_top_colors(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.resize((100, 100))  # 调整图像大小以加快处理速度
    image_np = np.array(image)
    image_np = image_np.reshape((image_np.shape[0] * image_np.shape[1], 3))

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(image_np)
    colors = kmeans.cluster_centers_

    hex_colors = [mcolors.to_hex(color / 255.0) for color in colors]
    return hex_colors

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
    