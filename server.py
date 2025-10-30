import os
import re
from pathlib import Path
from typing import List, Dict

import requests
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers

import factory


mcp = FastMCP(
    name='imagix-mcp-server',
    instructions='图片生成工具，按照用户需求生成图片',
)


headers = get_http_headers(include_all=True)
model = headers.get('model', os.getenv('model'))
api_key = headers.get('api_key', os.getenv('api_key'))

if model is None:
    raise ToolError('Model header is required.')

if api_key is None:
    raise ToolError('API key header is required.')

generator = factory.create_image_generator(model, api_key)


@mcp.tool(description=re.sub(r' +', ' ', generator.text_to_image.__doc__))
def text_to_image(prompt: str, size: str) -> List[Dict[str, str]]:
    try:
        url_list = generator.text_to_image(prompt, size)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url_list


@mcp.tool
def read_url(url: str, path: str) -> str:
    '''读取生成的图片url并保存到本地。
    
    Args:
        url (str): 图片url。
        path (str): 保存路径。
    '''
    path = Path(path)

    if path.exists():
        raise ToolError(f'Path {path} already exists.')

    try:
        response = requests.get(url)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    path.write_bytes(response.content)

    return 'success'


if __name__ == "__main__":
    mcp.run(transport='streamable-http')
