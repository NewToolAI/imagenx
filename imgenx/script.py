import os
from typing import List, Dict
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

from imgenx import factory


def text_to_image(model: str, api_key: str, prompt: str, size: str) -> List[Dict[str, str]]:
    generator = factory.create_image_generator(model, api_key)
    url_list = generator.text_to_image(prompt, size)
    return url_list


def run(prompt: str, size: str, output: str):
    print('Generate images...')

    load_dotenv()
    model = os.getenv('IMGENX_MODEL')
    api_key = os.getenv('IMGENX_API_KEY')

    if model is None:
        raise ValueError('Envrioment variable IMGENX_MODEL is empty.')

    if api_key is None:
        raise ValueError('Envrioment variable IMGENX_API_KEY is empty.')

    output = Path(output)

    if output.exists() and output.is_file():
        raise ValueError(f'Output path {output} already exists.')

    url_list = text_to_image(model, api_key, prompt, size)

    if output.is_dir():
        path_list = [f'{output}/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}_{i + 1}.png' for i in range(len(url_list))]
    else:
        path_list = [f'{output.parent}/{output.stem}_{i + 1}.{output.suffix}' for i in range(len(url_list))]
    
    for url_item, path in zip(url_list, path_list):
        response = requests.get(url_item['url'])
        Path(path).write_bytes(response.content)
        print(f'Save image to {path}')
