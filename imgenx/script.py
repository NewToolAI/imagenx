import os
from typing import List, Dict
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

from imgenx import factory, utils


load_dotenv()


def text_to_image(model: str, api_key: str, prompt: str, size: str) -> List[Dict[str, str]]:
    generator = factory.create_text_to_image(model, api_key)
    url_list = generator.text_to_image(prompt, size)
    return url_list


def image_to_image(model: str, api_key: str, prompt: str, images: List[str], size: str) -> List[Dict[str, str]]:
    generator = factory.create_image_to_image(model, api_key)
    url_list = generator.image_to_image(prompt, images, size)
    return url_list


def text_to_video(model: str, api_key: str, prompt: str,
                  resolution: str = '720p', ratio: str = '16:9', duration: int = 5) -> str:
    generator = factory.create_text_to_video(model, api_key)
    url = generator.text_to_video(prompt, resolution, ratio, duration)
    return url


def image_to_video(model: str, api_key: str, prompt: str, first_frame: str, last_frame: str|None = None,
                  resolution: str = '720p', ratio: str = '16:9', duration: int = 5) -> str:
    generator = factory.create_image_to_video(model, api_key)
    url = generator.image_to_video(prompt, first_frame, last_frame, resolution, ratio, duration)
    return url


def gen_image(prompt: str, size: str, output: str, images: List[str] = None):
    print('Generate images...')
    output = Path(output)

    if output.exists() and output.is_file():
        raise ValueError(f'Output path {output} already exists.')

    if images is not None and len(images) > 0:
        model, api_key = utils.get_provider_model_api_key('text_to_image', os.environ)

        if model is None:
            raise ValueError('Envrioment variable IMGENX_IMAGE_TO_IMAGE is empty.')

        if api_key is None:
            raise ValueError(f'Envrioment variable IMGENX_{model.split(":")[0].upper()}_API_KEY is empty.')

        url_list = image_to_image(model, api_key, prompt, images, size)
    else:
        model, api_key = utils.get_provider_model_api_key('text_to_image', os.environ)

        if model is None:
            raise ValueError('Envrioment variable IMGENX_TEXT_TO_IMAGE is empty.')

        if api_key is None:
            raise ValueError(f'Envrioment variable IMGENX_{model.split(":")[0].upper()}_API_KEY is empty.')

        url_list = text_to_image(model, api_key, prompt, size)

    if output.is_dir():
        path_list = [f'{output}/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}_{i + 1}.png' for i in range(len(url_list))]
    elif len(url_list) == 1:
        path_list = [output]
    else:
        path_list = [f'{output.parent}/{output.stem}_{i + 1}{output.suffix if output.suffix else ".jpg"}' for i in range(len(url_list))]
    
    for url_item, path in zip(url_list, path_list):
        response = requests.get(url_item['url'])
        Path(path).write_bytes(response.content)
        print(f'Save image to {path}')


def gen_video(prompt: str, first_frame: str|None = None, last_frame: str|None = None,
              resolution: str = '720p', ratio: str = '16:9', duration: int = 5, output: str = None):
    print('Generate video...')

    if output is None:
        output = f'{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.mp4'
    else:
        output = Path(output).with_name(f'{Path(output).stem}_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}{Path(output).suffix}')

    if output.exists() and output.is_file():
        raise ValueError(f'Output path {output} already exists.')

    if first_frame is None and last_frame is None:
        model, api_key = utils.get_provider_model_api_key('text_to_video', os.environ)

        if model is None:
            raise ValueError('Envrioment variable IMGENX_TEXT_TO_VIDEO is empty.')

        if api_key is None:
            raise ValueError(f'Envrioment variable IMGENX_{model.split(":")[0].upper()}_API_KEY is empty.')

        url = text_to_video(model, api_key, prompt, resolution, ratio, duration)
    else:
        model, api_key = utils.get_provider_model_api_key('image_to_video', os.environ)

        if model is None:
            raise ValueError('Envrioment variable IMGENX_IMAGE_TO_VIDEO is empty.')

        if api_key is None:
            raise ValueError(f'Envrioment variable IMGENX_{model.split(":")[0].upper()}_API_KEY is empty.')

        url = image_to_video(model, api_key, prompt, first_frame, last_frame, resolution, ratio, duration)

    response = requests.get(url)
    Path(output).write_bytes(response.content)
    print(f'Save video to {output}')
