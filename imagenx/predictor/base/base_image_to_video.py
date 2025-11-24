from typing import List, Dict
from abc import ABC, abstractmethod


class BaseImageToVideo(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def image_to_video(self, prompt: str, first_frame: str, last_frame: str|None, 
                       resolution: str, ratio: str, duration: int):
        raise NotImplementedError
