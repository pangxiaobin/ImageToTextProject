from abc import ABC, abstractmethod
from PIL import Image


class BasePridictModel(ABC):
    @abstractmethod
    def predict(self, image: Image.Image) -> str:
        pass
