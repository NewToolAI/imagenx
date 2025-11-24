import dashscope
from imagenx.predictor.base.base_text_to_image import BaseTextToImage


class AliyunTextToImage(BaseTextToImage):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def text_to_image(self, prompt: str, size: str = '1328*1328'):
        '''根据提示词生成图片

        Args:
            prompt (str): 图片描述提示词
            size (str): 图片分辨率，1664*928: 16:9, 1472*1140: 4:3, 1328*1328(默认值): 1:1, 1140*1472: 3:4, 928*1664: 9:16
        
        Returns:
            图片url列表
        '''
        message = [
            {'role': 'user', 'content': [{'text': prompt}]}
        ]
        response = dashscope.MultiModalConversation.call(
            model=self.model,
            api_key=self.api_key,
            messages=message,
            size=size.replace('x', '*'),
            watermark=False
        )
        print(response)

        result = []
        for item in response.output.choices[0].message.content:
            result.append(item['image'])
        return result
