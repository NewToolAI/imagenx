import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers

from imagenx import factory, operator, utils


load_dotenv()

mcp = FastMCP(
    name='imagenx-mcp-server',
    instructions='图片视频生成工具，按照用户需求生成图片或视频',
)


@mcp.tool
def analyze_query(plan: str, tool_chains: List[str]) -> Dict[str, str]:
    '''分析用户需求，制定计划。确保用户输入query时首先调用此工具。

    Args:
        plan (str): 工具调用的思考和计划
        tool_chains (List[str]): 工具链列表: text_to_image | image_to_image | image_inspect | text_to_video | image_to_video ...
        
    Returns:
        工具参数更详细的说明
    '''
    headers = get_http_headers(include_all=True)
    env = os.environ
    result = {}

    for tool in tool_chains:
        tool = tool.strip()

        if tool == 'text_to_image':
            model, api_key = utils.get_provider_model_api_key(tool, headers, env)
            generator = factory.create_text_to_image(model, api_key)
            result[tool] = re.sub(r' +', ' ', generator.text_to_image.__doc__)
        elif tool == 'image_to_image':
            model, api_key = utils.get_provider_model_api_key(tool, headers, env)
            generator = factory.create_image_to_image(model, api_key)
            result[tool] = re.sub(r' +', ' ', generator.image_to_image.__doc__)
        elif tool == 'text_to_video':
            model, api_key = utils.get_provider_model_api_key(tool, headers, env)
            generator = factory.create_text_to_video(model, api_key)
            result[tool] = re.sub(r' +', ' ', generator.text_to_video.__doc__)
        elif tool == 'image_to_video':
            model, api_key = utils.get_provider_model_api_key(tool, headers, env)
            generator = factory.create_image_to_video(model, api_key)
            result[tool] = re.sub(r' +', ' ', generator.image_to_video.__doc__)
        else:
            pass

    return result


@mcp.tool
def text_to_image(prompt: str, size: str) -> List:
    '''根据输入的提示词生成图片.
    确保用户需要文生图时先调用`analyze_query`工具，再调用此工具。
    确保用Markdown格式输出图片url，例如：[title](url)
    确保生成图片后用`download`工具下载到本地，如果没有`download`工具，用命令行`curl`命令下载
        
    Args:
        prompt (str): 生成图片的提示词
        size (str): 生成图像的分辨率或宽高像素值
        
    Returns:
        生成的图片url。
    '''
    headers = get_http_headers(include_all=True)
    env = os.environ
    model, api_key = utils.get_provider_model_api_key('text_to_image', headers, env)

    if model is None:
        raise ToolError('IMAGENX_TEXT_TO_IMAGE is None')

    if api_key is None:
        raise ToolError(f'IMAGENX_{model.split(":")[0].upper()}_API_KEY is None')

    try:
        generator = factory.create_text_to_image(model, api_key)
        url_list = generator.text_to_image(prompt, size)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url_list


@mcp.tool
def image_to_image(prompt: str, images: List[str], size: str) -> List:
    '''根据输入的提示词和图片生成新图片。
    确保用户需要图生图时先调用`analyze_query`工具，再调用此工具。
    确保用Markdown格式输出图片url，例如：[title](url)
    确保生成图片后用`download`工具下载到本地，如果没有`download`工具，用命令行`curl`命令下载
        
    Args:
        prompt (str): 生成图片的提示词
        images (List[str]): 输入图片url列表或文件路径列表
        size (str): 生成图像的分辨率或宽高像素值
        
    Returns:
        生成的图片url。
    '''
    headers = get_http_headers(include_all=True)
    env = os.environ
    model, api_key = utils.get_provider_model_api_key('image_to_image', headers, env)

    if model is None:
        raise ToolError('IMAGENX_IMAGE_TO_IMAGE is None')

    if api_key is None:
        raise ToolError(f'IMAGENX_{model.split(":")[0].upper()}_API_KEY is None')

    try:
        generator = factory.create_image_to_image(model, api_key)
        url_list = generator.image_to_image(prompt, images, size)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url_list


@mcp.tool
def text_to_video(prompt: str, resolution: str, ratio: str, duration: int) -> str:
    '''根据输入的提示词生成视频。
    确保用户需要文生视频时先调用`analyze_query`工具，再调用此工具。
    确保用Markdown格式输出视频url，例如：[title](url)
    确保生成视频后用`download`工具下载到本地，如果没有`download`工具，用命令行`curl`命令下载
        
    Args:
        prompt (str): 生成图片的提示词
        resolution (str): 生成视频的分辨率
        ratio (str): 生成视频的比例
        duration (int): 生成视频的时长
        
    Returns:
        视频下载的url
    '''
    headers = get_http_headers(include_all=True)
    env = os.environ
    model, api_key = utils.get_provider_model_api_key('text_to_video', headers, env)

    if model is None:
        raise ToolError('IMAGENX_TEXT_TO_VIDEO is None')

    if api_key is None:
        raise ToolError(f'IMAGENX_{model.split(":")[0].upper()}_API_KEY is None')

    try:
        generator = factory.create_text_to_video(model, api_key)
        url = generator.text_to_video(prompt, resolution, ratio, duration)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url


@mcp.tool
def image_to_video(prompt: str, resolution: str, ratio: str, duration: int, 
                   first_frame: str, last_frame: str|None = None) -> str:
    '''根据输入的提示词和视频首尾帧图片生成视频。
    确保用户需要图生视频时先调用`analyze_query`工具，再调用此工具。
    确保用Markdown格式输出视频url，例如：[title](url)
    确保生成视频后用`download`工具下载到本地，如果没有`download`工具，用命令行`curl`命令下载
        
    Args:
        prompt (str): 生成图片的提示词
        resolution (str): 生成视频的分辨率
        ratio (str): 生成视频的比例
        duration (int): 生成视频的时长
        first_frame (str): 视频的首帧图片url或文件路径
        last_frame (str|None): 视频的尾图片url或文件路径，默认None
        
    Returns:
        视频下载的url
    '''
    headers = get_http_headers(include_all=True)
    env = os.environ
    model, api_key = utils.get_provider_model_api_key('image_to_video', headers, env)

    if model is None:
        raise ToolError('IMAGENX_IMAGE_TO_VIDEO is None')

    if api_key is None:
        raise ToolError(f'IMAGENX_{model.split(":")[0].upper()}_API_KEY is None')

    try:
        generator = factory.create_image_to_video(model, api_key)
        url = generator.image_to_video(prompt, first_frame, last_frame, resolution, ratio, duration)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return url


@mcp.tool
def inspect_image(prompt: str, image: str) -> str:
    '''观察分析图片获取精确的信息，确保用户需要分析，编辑、裁剪图片时先调用此工具。
    确保尽量用精确数字描述图片信息。
    输出图片裁剪区域时，确保给出精确的**小数比例坐标**，坐标为左上角和右下角：x1(left), y1(upper), x2(right), y2(lower)

    Args:
        prompt (str): 分析图片的提示词
        image (str): 图片路径或URL

    Returns:
        str: 图片分析结果
    '''
    headers = get_http_headers(include_all=True)
    env = os.environ
    model, api_key = utils.get_provider_model_api_key('inspect_image', headers, env)

    if model is None:
        raise ToolError('IMAGENX_INSPECT_IMAGE is None')

    if api_key is None:
        raise ToolError(f'IMAGENX_{model.split(":")[0].upper()}_API_KEY is None')

    try:
        info = operator.get_image_info(image)
        prompt = f'image info: {info}\n\n{prompt}'

        inspector = factory.create_image_inspector(model, api_key)
        result = inspector.inspect(prompt, image)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return result


@mcp.tool
def download(url: str, path: str) -> str:
    '''读取生成的图片或视频 url 并保存到本地
    
    Args:
        url (str): 图片或视频 url
        path (str): 保存路径
    
    Returns:
        str: 成功时返回 'success'
    '''
    try:
        operator.download(url, path)
    except Exception as e:
        raise ToolError(f'Error: {e}')

    return 'success'


@mcp.tool
def get_image_info(image: str) -> Dict[str, str]:
    '''获取图片分辨率和类型信息，确保用户需要获取图片分辨率和类型信息时调用此工具。

    Args:
        image (str): 图片路径或URL

    Returns:
        Dict[str,str]: 分辨率和类型信息
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
        box (str): 小数比例坐标，x1(left), y1(upper), x2(right), y2(lower)
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


@mcp.tool
def paste_image(front_image: str, background_image: str, output: str, position: Tuple[int, int]) -> Dict[str, str]:
    '''将图片粘贴到背景图片上，确保用户需要粘贴图片时调用此工具。
    粘贴图片前，需要用`resize_image`工具调整`front_image`到适合的尺寸。
    调用`analyze_image`工具确定粘贴位置。

    Args:
        front_image (str): 图片路径或URL
        background_image (str): 背景图片路径或URL
        output (str): 输出文件路径
        position (Tuple[int, int]): 粘贴位置的(x, y)，背景图片的左上角像素坐标

    Returns:
        Dict[str,str]: 生成图片的 path
    '''
    try:
        operator.paste_image(front_image, background_image, position, output)
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
