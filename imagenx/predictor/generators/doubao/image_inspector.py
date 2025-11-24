import base64
from pathlib import Path
from typing import List, Dict
from volcenginesdkarkruntime import Ark

from imagenx.predictor.base.base_image_inspector import BaseImageInspector


class DoubaoImageInspector(BaseImageInspector):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def inspect(self, prompt: str, image: str) -> str:
        if not image.startswith('http'):
            image = self._image_to_base64(image)

        response = self.client.chat.completions.create(
            model=self.model,   
            messages=[
                {
                    'role': 'user',
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return response.output.choices[0].message.content[0]['text']

    def _image_to_base64(self, image_path: str) -> str:
        image_path = Path(image_path)

        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_image = f'data:image/{image_path.suffix.strip(".")};base64,{base64_image}'

        return base64_image