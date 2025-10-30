from abc import ABC, abstractmethod


class BaseImageGenerator(ABC):

    @abstractmethod
    def __init__(self, mdoel: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def text_to_image(self, prompt: str, size: str) -> bytes:
        raise NotImplementedError
