import base64
from pathlib import Path
from typing import List, Dict
from volcenginesdkarkruntime import Ark

from imgenx.predictor.base.base_image_generator import BaseImageGenerator


class DoubaoImageGenerator(BaseImageGenerator):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def text_to_image(self, prompt: str, size: str) -> List[Dict[str, str]]:
        response = self.client.images.generate( 
            model=self.model,
            prompt=prompt,
            sequential_image_generation='auto',
            response_format='url',
            size=size,
            stream=False,
            watermark=False
        ) 

        result = []
        for item in response.model_dump()['data']:
            if 'b64_json' in item:
                item.pop('b64_json')

            result.append(item)

        return result

    def image_to_image(self, prompt: str, images: List[str], size: str) -> List[Dict[str, str]]:
        if len(images) == 0:
            pass_images = None
        else:
            pass_images = []

        for i in images:
            if i.startswith('http'):
                pass_images.append(i)
            else:
                pass_images.append(self._image_to_base64(i))

        response = self.client.images.generate( 
            model=self.model,
            prompt=prompt,
            sequential_image_generation='auto',
            response_format='url',
            image=pass_images,
            size=size,
            stream=False,
            watermark=False
        ) 

        result = []
        for item in response.model_dump()['data']:
            if 'b64_json' in item:
                item.pop('b64_json')

            result.append(item)

        return result

    def _image_to_base64(self, image_path: str) -> str:
        image_path = Path(image_path)

        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_image = f'data:image/{image_path.suffix.strip(".")};base64,{base64_image}'

        return base64_image
