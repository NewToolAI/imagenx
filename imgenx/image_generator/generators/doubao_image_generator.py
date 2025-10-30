from typing import List, Dict
from volcenginesdkarkruntime import Ark

from imgenx.image_generator.base.base_image_generator import BaseImageGenerator


class DoubaoImageGenerator(BaseImageGenerator):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def text_to_image(self, prompt: str, size: str) -> List[Dict[str, str]]:
        '''生成图片。确保用户需要生成图片时调用此工具。
        
        Args:
            prompt (str): 生成图片的提示词
            size (str): 生成图像的分辨率或宽高像素值
                        分辨率可选值：'1K'、'2K', '4K'
                        宽高像素可选值：2048x2048、2304x1728、1728x2304、2560x1440、1440x2560、2496x1664、1664x2496、3024x1296
        
        Returns:
             List[Dict[str: str]]: 图片url列表。
        '''
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
