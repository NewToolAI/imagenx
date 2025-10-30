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

mcp = FastMCP(
    name='imgenx-mcp-server',
    instructions='图片生成工具，按照用户需求生成图片',
)


@mcp.tool
def text_to_image(prompt: str, size: str) -> List[Dict[str, str]]:
    '''根据用户要求生成图片。确保用户需要生成图片时调用此工具。
        
    Args:
        prompt (str): 生成图片的提示词
        size (str): 生成图像的分辨率或宽高像素值
                    分辨率可选值：'1K'、'2K', '4K'
                    宽高像素可选值：2048x2048、2304x1728、1728x2304、2560x1440、1440x2560、2496x1664、1664x2496、3024x1296
        
    Returns:
        List[Dict[str: str]]: 图片url列表。
    '''
    headers = get_http_headers(include_all=True)
    model = headers.get('imgenx_model', os.getenv('IMGENX_MODEL'))
    api_key = headers.get('imgenx_api_key', os.getenv('IMGENX_API_KEY'))

    if model is None:
        raise ToolError('IMGENX_MODEL is None')

    if api_key is None:
        raise ToolError('IMGENX_API_KEY is None')

    try:
        generator = factory.create_image_generator(model, api_key)
        url_list = generator.text_to_image(prompt, size)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url_list


@mcp.tool(description='')
def download_image(url: str, path: str) -> str:
    '''读取生成的图片url并保存到本地
    
    Args:
        url (str): 图片url
        path (str): 保存路径
    
    Returns:
        str: 成功时返回 'success'
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
