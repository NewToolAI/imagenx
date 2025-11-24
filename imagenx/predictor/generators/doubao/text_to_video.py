import time
from volcenginesdkarkruntime import Ark

from imagenx.predictor.base.base_text_to_video import BaseTextToVideo


class DoubaoTextToVideo(BaseTextToVideo):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def text_to_video(self, prompt: str, resolution: str = '720p', ratio: str = '16:9', duration: int = 5) -> str:
        '''根据提示词生成视频。

        Args:
            prompt (str): 生成视频的提示词
            resolution (str): 生成视频的分辨率：480p、720、1080p
            ratio (str): 生成视频的比例：16:9、4:3、1:1、3:4、9:16、21:9
            duration (int): 生成视频的时长，单位秒，支持 2~12 秒
        
        Returns:
            视频下载的url
        '''
        create_result = self.client.content_generation.tasks.create(
            model=self.model,
            content=[
                {
                    'type': 'text',
                    'text': prompt.strip()
                }
            ],
            extra_body={
                'resolution': resolution,
                'ratio': ratio,
                'duration': duration,
            }
        )
        task_id = create_result.id

        while True:
            get_result = self.client.content_generation.tasks.get(task_id=task_id)
            status = get_result.status
            if status == "succeeded":
                return get_result.content.video_url
            elif status == "failed":
                raise Exception(str(get_result.error))
            else:
                time.sleep(3)
