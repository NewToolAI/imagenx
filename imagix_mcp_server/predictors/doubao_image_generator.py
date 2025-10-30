import sys
sys.path.insert(0, '..')

from typing import List, Literal
from base64 import b64decode

from volcenginesdkarkruntime import Ark

from base.base_image_generator import BaseImageGenerator


class DoubaoImageGenerator(BaseImageGenerator):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def text_to_image(self, prompt: str, size: str) -> List[bytes]:
        '''生成图片。确保用户需要生成图片时调用此工具。
        
        Args:
            prompt (str): 图片描述。
            size (str): 生成图像的分辨率或宽高像素值，
                        分辨率可选值：'1K'、'2K', '4K'。
                        宽高像素可选值：2048x2048、2304x1728、1728x2304、2560x1440、1440x2560、2496x1664、1664x2496、3024x1296

        
        Returns:
            List[bytes]: 图片字节流列表。
        '''
        response = self.client.images.generate( 
            model=self.model,
            prompt=prompt,
            sequential_image_generation='auto',
            response_format='b64_json',
            size=size,
            stream=False,
            watermark=False
        ) 

        result = [b64decode(i.b64_json) for i in response.data]
        return result


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()


    generator = DoubaoImageGenerator(
        model='doubao-seedream-4-0-250828',
        api_key=os.getenv('ARK_API_KEY'),
    )
    data = generator.text_to_image(
        prompt='一个人在沙滩上',
        size='2K',
    )
    with open('test.png', 'wb') as f:
        f.write(data[0])
