import numpy as np
import tensorflow as tf
from PIL import Image

class ASLPredictor:
    def __init__(self, model_path='asl_base_model.keras'):
        self.model = tf.keras.models.load_model(model_path)
        
        self.class_names = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "del", "nothing", "space"
        ]

    def preprocess_image(self, image: Image.Image, target_size=(128, 128)):
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        resized_image = image.resize(target_size)
        
        img_array = np.array(resized_image, dtype=np.float32)
        
        # تحويل ترتيب الألوان لـ BGR للتوافق مع تدريب الموديل
        img_array = img_array[:, :, ::-1]
        
        # التطبيع
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, image: Image.Image):
        processed_img = self.preprocess_image(image, target_size=(128, 128))
        predictions = self.model.predict(processed_img)[0]
        predicted_index = int(np.argmax(predictions))
        confidence = float(np.max(predictions))
        predicted_class = self.class_names[predicted_index]
        
        all_probabilities = {
            self.class_names[i]: float(predictions[i]) 
            for i in range(len(self.class_names))
        }
        
        return predicted_class, confidence, all_probabilities