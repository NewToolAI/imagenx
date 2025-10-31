from typing import List, Dict
from abc import ABC, abstractmethod


class BaseImageGenerator(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def text_to_image(self, prompt: str, size: str) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def image_to_image(self, prompt: str, images: List[str], size: str) -> List[Dict[str, str]]:
        raise NotImplementedError
