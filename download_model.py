import os
import requests
from tqdm import tqdm

# Configuration
# Configuration
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
# Using a smaller model for optimization: TinyLlama-1.1B
MODEL_URL = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODEL_FILENAME = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

def download_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    
    dest_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
    
    if os.path.exists(dest_path):
        print(f"Model already exists at {dest_path}")
        return

    print(f"Downloading model from {MODEL_URL}...")
    print("This may take a while depending on your internet connection (~4.3GB).")
    
    response = requests.get(MODEL_URL, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 # 1 Kibibyte
    
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    
    with open(dest_path, 'wb') as f:
        for data in response.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    
    if total_size != 0 and t.n != total_size:
        print("ERROR: Something went wrong")
    else:
        print("Download complete!")

if __name__ == "__main__":
    download_model()
