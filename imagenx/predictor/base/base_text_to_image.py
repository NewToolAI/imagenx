from typing import List, Dict
from abc import ABC, abstractmethod


class BaseTextToImage(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def text_to_image(self, prompt: str, size: str):
        raise NotImplementedError
