import base64
from pathlib import Path
import dashscope

from imagenx.predictor.base.base_image_inspector import BaseImageInspector


class AliyunImageInspector(BaseImageInspector):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def inspect(self, prompt: str, image: str) -> str:
        if not image.startswith('http'):
            image = self._image_to_base64(image)

        response = dashscope.MultiModalConversation.call(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {
                    'role': 'user',
                    "content": [
                        {"image": image},
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