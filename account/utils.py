import tensorflow as tf
import base64
import io
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
    
model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False)

def decode_base64_to_image(base64_string):
    img_data = base64.b64decode(base64_string.split(",")[1])
    img = Image.open(io.BytesIO(img_data)).convert('RGB')
    return img

# Decode base64 images
def calculate_signature_similarity(base64_img1, base64_img2):
    img1 = decode_base64_to_image(base64_img1)
    img2 = decode_base64_to_image(base64_img2)

    # Resize to match MobileNetV2 expected input
    img1 = img1.resize((224, 224))
    img2 = img2.resize((224, 224))

    # Convert to arrays
    img1_array = tf.keras.preprocessing.image.img_to_array(img1)
    img2_array = tf.keras.preprocessing.image.img_to_array(img2)

    # Preprocess
    img1_array = tf.keras.applications.mobilenet_v2.preprocess_input(img1_array)
    img2_array = tf.keras.applications.mobilenet_v2.preprocess_input(img2_array)
    # Get embeddings
    emb1 = model.predict(img1_array[None, ...])
    emb2 = model.predict(img2_array[None, ...])

    # Calculate cosine similarity
    similarity = cosine_similarity(emb1.flatten().reshape(1, -1), emb2.flatten().reshape(1, -1))
    return similarity
