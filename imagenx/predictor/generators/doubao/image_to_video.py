import base64
import time
from pathlib import Path
from imagenx.predictor.base.base_image_to_video import BaseImageToVideo
from volcenginesdkarkruntime import Ark


class DoubaoImageToVideo(BaseImageToVideo):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def image_to_video(self, prompt: str, first_frame: str, last_frame: str|None = None, 
                       resolution: str = '720p', ratio: str = '16:9', duration: int = 5) -> str:
        '''根据提示词和首尾帧图片生成视频。

        Args:
            prompt (str): 生成视频的提示词
            first_frame (str): 视频的首帧图片url或文件路径
            last_frame (str|None): 视频的尾图片url或文件路径，默认None
            resolution (str): 生成视频的分辨率：480p、720、1080p
            ratio (str): 生成视频的比例：16:9、4:3、1:1、3:4、9:16、21:9
            duration (int): 生成视频的时长，单位秒，支持 2~12 秒
        
        Returns:
            视频下载的url
        '''
        if not first_frame.startswith('http'):
            first_frame = self._image_to_base64(first_frame)

        if last_frame is not None and not last_frame.startswith('http'):
            last_frame = self._image_to_base64(last_frame)

        content = [
            {
                'type': 'text',
                'text': prompt.strip()
            },
            {
                'type': 'image_url',
                'image_url': {
                    'url': first_frame
                },
                'role': 'first_frame'
            }
        ]

        if last_frame is not None:
            content.append({
                'type': 'image_url',
                'image_url': {
                    'url': last_frame
                },
                'role': 'last_frame'
            })

        create_result = self.client.content_generation.tasks.create(
            model=self.model,
            content=content,
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

    def _image_to_base64(self, image_path: str) -> str:
        image_path = Path(image_path)

        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_image = f'data:image/{image_path.suffix.strip(".")};base64,{base64_image}'

        return base64_image