import base64
from pathlib import Path
import dashscope

from imagenx.predictor.base.base_image_to_video import BaseImageToVideo


class AliyunImageToVideo(BaseImageToVideo):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def image_to_video(self, prompt: str, first_frame: str, last_frame: str|None, 
                       resolution: str, ratio: str, duration: int) -> str:                       
        '''根据提示词和图片生成视频

        Args:
            prompt (str): 视频描述提示词
            first_frame (str): 视频第一帧图片url或文件路径
            last_frame (str|None): 视频最后一帧图片url或文件路径，可选
            resolution (str): 视频分辨率, 480P, 720P, 1080P
            ratio (str): 视频比例
            duration (int): 视频时长，单位秒, 5s, 10s
        
        Returns:
            视频url
        '''

        if not first_frame.startswith('http'):
            first_frame = self._image_to_base64(first_frame)

        if last_frame and not last_frame.startswith('http'):
            last_frame = self._image_to_base64(last_frame)

        response = dashscope.VideoSynthesis.call(
            model=self.model,
            api_key=self.api_key,
            prompt=prompt,
            img_url=first_frame,
            first_frame_url=first_frame,
            last_frame_url=last_frame,
            resolution=resolution.upper(),
            duration=duration,
            watermark=False,
        )
        return response.output.video_url

    def _image_to_base64(self, image_path: str) -> str:
        image_path = Path(image_path)

        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_image = f'data:image/{image_path.suffix.strip(".")};base64,{base64_image}'

        return base64_image