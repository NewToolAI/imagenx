import base64
from pathlib import Path
from typing import List, Dict
from volcenginesdkarkruntime import Ark

from imagenx.predictor.base.base_image_to_image import BaseImageToImage


class DoubaoImageToImage(BaseImageToImage):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def image_to_image(self, prompt: str, images: List[str], size: str) -> List[Dict[str, str]]:
        '''根据输入的提示词和图片生成图片。

        Args:
            prompt (str): 生成图片的提示词
            images (List[str]): 输入图片url列表或文件路径列表
            size (str): 生成图像的分辨率或宽高像素值
                    分辨率可选值：'1K'、'2K', '4K'
                    宽高像素可选值：2048x2048、2304x1728、1728x2304、2560x1440、1440x2560、2496x1664、1664x2496、3024x1296
        
        Returns:
            List[Dict[str: str]]: 图片url列表。
        '''
        if len(images) == 0:
            pass_images = None
        else:
            pass_images = []

        for i in images:
            if str(i).startswith('http'):
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