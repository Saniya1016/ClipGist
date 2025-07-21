from transformers import CLIPProcessor, CLIPModel
import torch
import os
import json
from PIL import Image


#load the CLIP model and processor

def load_clip_model(model_name='openai/clip-vit-base-patch32'):
    model = CLIPModel.from_pretrained(model_name)
    processor = CLIPProcessor.from_pretrained(model_name)
    return model, processor

def generate_embeddings(frame_segment_pairs_path, model, processor):
    """
    Generate embeddings for a given image using the CLIP model.
    
    Args:
        frame_segment_pairs_path (str): Path to the frame-segment pairs json file.
        model: Pretrained CLIP model.
        processor: Pretrained CLIP processor.
    
    Returns:
        torch.Tensor: Image embeddings.
    """

    with open(frame_segment_pairs_path, 'r') as f:
        frame_segment_pairs = json.load(f)
    
    embeddings = []
    for pair in frame_segment_pairs:

        image_path = pair['frame_path']
        if not os.path.exists(image_path):
            print(f"Image {image_path} does not exist. Skipping.")
            continue
        
        image = Image.open(image_path).convert("RGB")
        text = pair['text']
        inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
            image_embedding = outputs.image_embeds[0]
            text_embedding = outputs.text_embeds[0]
        
        embeddings.append({
            'image_embedding': image_embedding.cpu().numpy().tolist(),
            'text_embedding': text_embedding.cpu().numpy().tolist(),
        })

    return {'embeddings': embeddings}


if __name__ == "__main__":
    model, processor = load_clip_model()
    frame_segment_embeddings = generate_embeddings('data/frame_segment_pairs.json', model, processor)
    print("Generated embeddings for all frame-segment pairs.")
    # Save embeddings to a file
    with open('data/embeddings/frame_segment_embeddings.json', 'w') as f:
        json.dump(frame_segment_embeddings, f, indent=4)
    print("Embeddings saved to data/embeddings/frame_segment_embeddings.json")
    torch.save(model.state_dict(), 'data/model/clip_model.pth')
    print("Model state saved to data/model/clip_model.pth")
    print("Done.")

    