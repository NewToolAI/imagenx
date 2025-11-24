from imagenx.predictor.base.base_text_to_video import BaseTextToVideo


class AliyunTextToVideo(BaseTextToVideo):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def text_to_video(self, prompt: str, resolution: str, ratio: str, duration: int) -> str:
        '''此工具没有实现，确保不要调用此工具'''
        return '此工具没有实现'
