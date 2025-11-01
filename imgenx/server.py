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
from imgenx import operator


load_dotenv()

mcp = FastMCP(
    name='imgenx-mcp-server',
    instructions='图片生成工具，按照用户需求生成图片',
)


@mcp.tool
def text_to_image(prompt: str, size: str) -> List[Dict[str, str]]:
    '''根据输入的提示词生成图片，确保用户需要生成图片时调用此工具。
    确保用Markdown格式输出图片url，例如：[title](url)
        
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


@mcp.tool
def image_to_image(prompt: str, images: List[str], size: str) -> List[Dict[str, str]]:
    '''根据输入的提示词和图片生成新图片，确保用户需要生成图片时调用此工具。
    确保用Markdown格式输出图片url，例如：[title](url)
        
    Args:
        prompt (str): 生成图片的提示词
        images (List[str]): 输入图片url列表或文件路径列表
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
        url_list = generator.image_to_image(prompt, images, size)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url_list


@mcp.tool
def download_image(url: str, path: str) -> str:
    '''读取生成的图片url并保存到本地
    
    Args:
        url (str): 图片url
        path (str): 保存路径
    
    Returns:
        str: 成功时返回 'success'
    '''
    try:
        operator.download_image(url, path)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return 'success'


@mcp.tool
def get_image_info(image: str) -> Dict[str, str]:
    '''获取图片信息，确保用户需要获取图片信息时调用此工具。

    Args:
        image (str): 图片路径或URL

    Returns:
        Dict[str,str]: 图片信息
    '''
    try:
        info = operator.get_image_info(image)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return info


@mcp.tool
def crop_image(image: str, box: str, output: str) -> Dict[str, str]:
    '''框裁剪图片，确保用户需要裁剪图片时调用此工具。
    Args:
        image (str): 图片路径或URL
        box (str): "x,y,width,height"
        output (str): 输出文件路径（后缀决定格式）

    Returns:
        Dict[str,str]: 生成图片的 path
    '''
    try:
        operator.crop_image(image, box, output)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    p = Path(output).resolve()
    return {'title': p.name, 'path': str(p)}


@mcp.tool
def resize_image(image: str, size: str, output: str, keep_aspect: bool = True) -> Dict[str, str]:
    '''调整图片尺寸，确保用户需要调整图片尺寸时调用此工具。

    Args:
        image (str): 图片路径或URL
        size (str): "WIDTHxHEIGHT"
        output (str): 输出文件路径
        keep_aspect (bool): 是否保持比例（True 为等比不超过目标尺寸）

    Returns:
        Dict[str,str]: 生成图片的 path
    '''
    try:
        operator.resize_image(image, size, output, keep_aspect=keep_aspect)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    p = Path(output).resolve()
    return {'title': p.name, 'path': str(p)}


@mcp.tool
def convert_image(image: str, format: str, output: str, quality: int = 90) -> Dict[str, str]:
    '''格式转换，确保用户需要转换图片格式时调用此工具。

    Args:
        image (str): 图片路径或URL
        format (str): 目标格式：PNG/JPEG/JPG/WEBP
        output (str): 输出文件路径
        quality (int): 压缩质量（针对有损格式）

    Returns:
        Dict[str,str]: 生成图片的 path
    '''
    try:
        operator.convert_image(image, format, output, quality=quality)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    p = Path(output).resolve()
    return {'title': p.name, 'path': str(p)}


@mcp.tool
def adjust_image(image: str, output: str, brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0) -> Dict[str, str]:
    '''基础图像调整：亮度/对比度/饱和度，确保用户需要调整图片时调用此工具。

    Args:
        image (str): 图片路径或URL
        output (str): 输出文件路径
        brightness (float): 亮度，默认1.0
        contrast (float): 对比度，默认1.0
        saturation (float): 饱和度，默认1.0

    Returns:
        Dict[str,str]: 生成图片的 path
    '''
    try:
        operator.adjust_image(image, output, brightness=brightness, contrast=contrast, saturation=saturation)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    p = Path(output).resolve()
    return {'title': p.name, 'path': str(p)}


@mcp.custom_route('/health', methods=['GET'])
def health() -> str:
    return 'success'


@mcp.custom_route('/healthy', methods=['GET'])
def healthy() -> str:
    return 'success'
