import base64
from pathlib import Path
from dashscope import MultiModalConversation

from imagenx.predictor.base.base_image_to_image import BaseImageToImage


class AliyunImageToImage(BaseImageToImage):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def image_to_image(self, prompt: str, images: list, size: str):
        '''根据提示词和图片生成图片

        Args:
            prompt (str): 图片描述提示词
            images (List[str]): 输入图片url列表或文件路径列表
            size (str): 图片分辨率
        
        Returns:
            图片url列表
        '''
        messages = [{'role': 'user', 'content': []}]

        for i in images:
            if not str(i).startswith('http'):
                i = self._image_to_base64(i)
            messages[-1]['content'].append({'image': i})

        messages[-1]['content'].append({'text': prompt})

        response = MultiModalConversation.call(
            model=self.model,
            api_key=self.api_key,
            result_format='message',
            stream=False,
            watermark=False,
            negative_prompt="",
            messages=messages
        )

        result = []
        for image_url in response.output.choices[0].message.content:
            result.append(image_url)

        return result

    def _image_to_base64(self, image_path: str) -> str:
        image_path = Path(image_path)

        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_image = f'data:image/{image_path.suffix.strip(".")};base64,{base64_image}'

        return base64_image