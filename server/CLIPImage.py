import torch
import clip
from PIL import Image, ImageFile
import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import open_clip
import time
import functools


def timeit(func):
    @functools.wraps(func)
    def wrapper_timeit(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds.")
        return result
    return wrapper_timeit
"""
已有文本和图片库路径，在库中用CLIP匹配相似度最高的图片出来
"""
def encode_images_ordered(folder_path):
    
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    # Initialize the model and preprocessing tools
    model, _, preprocess = open_clip.create_model_and_transforms( 'ViT-B-32', 
        pretrained='CLIP-ViT-B-32-laion2B-s34B-b79K/open_clip_pytorch_model.bin')

    # Initialize a list to store image features
    all_image_features = []

    # Get a sorted list of files in the folder
    files = sorted(os.listdir(folder_path))

    # Iterate over each file in the sorted list
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Load and preprocess the image
            image = preprocess(Image.open(file_path).convert("RGB")).unsqueeze(0)

            # Encode the image using the model
            with torch.no_grad(), torch.cuda.amp.autocast():
                image_features = model.encode_image(image)
                image_features /= image_features.norm(dim=-1, keepdim=True)
                all_image_features.append(image_features)

    # Combine all features into a single tensor
    all_image_features = torch.vstack(all_image_features)
    torch.save(all_image_features, 'image_embeddings.pt')
    print(all_image_features.shape)
    return all_image_features

@timeit
def matching(text, image_path):
    start_time = time.perf_counter()

    model, _, preprocess = open_clip.create_model_and_transforms( 'ViT-B-32', 
        pretrained='CLIP-ViT-B-32-laion2B-s34B-b79K/open_clip_pytorch_model.bin')
    tokenizer = open_clip.get_tokenizer('ViT-B-32')
    text = tokenizer(text)
    text_features = model.encode_text(text)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    image_features = torch.load("image_embeddings.pt")
    text_probs = (100 * text_features @ image_features.T).softmax(dim=-1)

    files = sorted(os.listdir(image_path))

    if len(text_probs[0]) != len(files):
        print("error")
    # for i in range(len(text_probs[0])):
    #     print(files[i], text_probs[0][i].item())
    # print(text_probs)
    top_images = text_probs.topk(1)
    for score, idx in zip(*top_images):
        print(f"Image {files[idx]} has a similarity of {score.item()}")
        result = os.path.join(image_path, files[idx])
        return image_path + "/" + files[idx]


if __name__ == '__main__':
    # images to embeddings
    # encode_images_ordered("imgs")

    # Retrieve simiilar images
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    text = ["Decorated tree, presents, red and gold ornaments, fireplace, snowflakes, garlands, candlelight"]
    image_folder = 'imgs' 
    retrieved_image_path = matching(text,image_folder)
    retrieved_image = Image.open(retrieved_image_path)
    retrieved_image.show()