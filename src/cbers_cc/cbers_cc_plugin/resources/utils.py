

from cbers_cc_plugin.resources.types import (
    Image,
    Embedding,
)


def calculate_tile_embedding(image: Image, model, processor) -> Embedding:
    # converts the images into model-acceptable inputs and applies padding
    inputs = processor(images=image, return_tensors="jax", padding=True)
    # passes the images through the CLIP model and extracts image features
    emb = model.get_image_features(**inputs)
    # converts the embedding vectors into a Python list and returns them
    return emb.tolist()[0]