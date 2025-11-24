from typing import List, Dict
from abc import ABC, abstractmethod


class BaseImageInspector(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def inspect(self, prompt: str, image: str):
        raise NotImplementedError
