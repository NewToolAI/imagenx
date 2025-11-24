from typing import List, Dict
from abc import ABC, abstractmethod


class BaseTextToVideo(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def text_to_video(self, prompt: str, resolution: str, ratio: str, duration: int):
        raise NotImplementedError
