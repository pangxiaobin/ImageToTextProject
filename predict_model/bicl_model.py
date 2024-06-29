from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from pathlib import Path
import time
from predict_model.base_model import BasePridictModel

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "predict_model/models/blip-image-captioning-large"

print("Loading model from:", MODEL_PATH)


class BICLModelPredict(BasePridictModel):
    """
    use https://huggingface.co/Salesforce/blip-image-captioning-large
    """

    def __init__(self):
        self.processor = BlipProcessor.from_pretrained(MODEL_PATH)
        self.model = BlipForConditionalGeneration.from_pretrained(MODEL_PATH)
        if torch.cuda.is_available():
            self.model.to("cuda")

    def predict(self, raw_image: Image.Image) -> str:
        start_time = time.time()
        print(f"start predicting")
        inputs = self.processor(raw_image, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = self.processor(raw_image, return_tensors="pt").to("cuda")

        output = self.model.generate(
            **inputs, max_new_tokens=50, num_return_sequences=1
        )
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        end_time = time.time()
        print(f"end predicting, use time: {end_time - start_time}")
        return caption


if __name__ == "__main__":
    model = BICLModelPredict()
    img = Image.open(BASE_DIR / "predict_model/test_car.jpg")
    caption = model.predict(img)
    print(caption)
