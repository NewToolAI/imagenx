import os
import re
from pathlib import Path
from typing import List, Dict

import requests
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers

from imgenx import factory


load_dotenv()
print(os.getenv('IMGENX_MODEL'))
print(os.getenv('IMGENX_API_KEY'))

mcp = FastMCP(
    name='imgenx-mcp-server',
    instructions='图片生成工具，按照用户需求生成图片',
)

headers = get_http_headers(include_all=True)
model = headers.get('IMGENX_MODEL', os.getenv('IMGENX_MODEL'))
api_key = headers.get('IMGENX_API_KEY', os.getenv('IMGENX_API_KEY'))

if model is None:
    raise ValueError('IMGENX_MODEL is None')

if api_key is None:
    raise ValueError('IMGENX_API_KEY is None')

generator = factory.create_image_generator(model, api_key)


@mcp.tool(description=re.sub(r' +', ' ', generator.text_to_image.__doc__))
def text_to_image(prompt: str, size: str) -> List[Dict[str, str]]:
    try:
        url_list = generator.text_to_image(prompt, size)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url_list


@mcp.tool(description='读取生成的图片url并保存到本地\n\nArgs:\nurl (str): 图片url\npath (str): 保存路径')
def download_image(url: str, path: str) -> str:
    path = Path(path)

    if path.exists():
        raise ToolError(f'Path {path} already exists.')

    try:
        response = requests.get(url)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    path.write_bytes(response.content)

    return 'success'
