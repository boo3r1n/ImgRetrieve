import os
from flask import send_file, jsonify, url_for
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.colors as mcolors
from flask import Flask, request
from flask_cors import CORS
from CLIPImage import matching
from PIL import Image, ImageFile

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '后端服务器已启动'


@app.route('/text-to-image', methods=['POST'])
def text_to_image():
    data = request.get_json()
    if not data or 'text' not in data or not data['text'].strip():  # 如果缺少 `text` 参数或为空
        text = 'a cat' 
    else:
        text = data.get('text', '')
 
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image_folder = 'static/imgs'  
    result_path = matching(text, image_folder)
    if not os.path.exists(result_path):
        return jsonify({"error": "Retrieved image not found"}), 404

    top_colors = get_top_colors(result_path)

    relative_path = os.path.relpath(result_path, 'static')
    return jsonify({
        "image_url": url_for('static', filename=relative_path, _external=True),
        "top_colors": top_colors
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