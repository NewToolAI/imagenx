<div align="center">
  <img src="logo.jpg" alt="ImgenX MCP Server Logo" width="800" height="400">
  
  [![Version](https://img.shields.io/badge/Version-0.1.0-brightgreen.svg)](https://github.com/NewToolAI/imgenx/releases)
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#许可证)

**ImgenX: AI图片生成与图片处理的命令行工具和MCP Server**
</div>

## 功能特性

- **文本生成图片**: 根据文本描述生成图片
- **图片生成图片**: 基于输入图片和文本描述生成新图片
- **图片下载**: 将生成的图片URL下载并保存到本地
- **图片处理工具**: 提供完整的图片处理功能
  - **图片信息获取**: 查看图片格式、尺寸、模式等信息
  - **图片裁剪**: 按指定区域裁剪图片
  - **尺寸调整**: 调整图片大小，支持保持宽高比
  - **格式转换**: 支持PNG、JPEG、JPG、WEBP格式转换
  - **图像调整**: 调整亮度、对比度、饱和度
- **多种分辨率支持**: 支持 1K、2K、4K 分辨率以及多种自定义像素尺寸
- **插件化架构**: 基于工厂模式设计，支持扩展新的图片生成服务提供商
- **MCP 协议支持**: 兼容 Model Context Protocol 标准

## 当前支持的服务提供商

- **豆包 (Doubao)**: 基于火山引擎的图片生成服务

## 安装

### 配置环境变量

```bash
export IMGENX_MODEL="doubao:doubao-seedream-4-0-250828"
export IMGENX_API_KEY="your_api_key"
```
或写入 .env 文件中

### 安装步骤

#### 方式一：pip 安装（推荐）

```bash
pip install imgenx
```

#### 方式二：从源码安装
```bash
git clone https://github.com/NewToolAI/imgenx.git
cd imgenx
pip install -e .
```

## 使用方法

### 作为命令行运行

```
imgenx gen 一只在云上飞翔的猫
imgenx gen --size 2K 一只在云上飞翔的猫
imgenx gen 一只在云上飞翔的猫 --size 2048x2048 --output test.jpg
imgenx gen 一只在云上飞翔的猫 --images test.jpg --size 2048x2048 --output test2.jpg
```

### 作为 MCP 服务器运行

#### 标准输入输出模式 (stdio)
```json
{
  "mcpServers": {
    "imgenx-mcp": {
      "command": "uvx",
      "args": [
        "-U",
        "imgenx",
        "server"
      ],
      "env": {
        "IMGENX_MODEL": "doubao:model-name",
        "IMGENX_API_KEY": "api-key"
      }
    }
  }
}
```

#### HTTP 服务器模式
```bash
imgenx server --transport streamable-http --host 0.0.0.0 --port 8000
```

```json
{
  "mcpServers": {
    "imgenx-mcp": {
      "url": "http://127.0.0.1:8000/mcp",
      "headers": {
        "IMGENX_MODEL": "doubao:model-name",
        "IMGENX_API_KEY": "api-key"
      }
    }
  }
}
```

#### 云服务免安装

```json
{
  "mcpServers": {
    "imgenx-cloud": {
      "url": "https://imgenx.fastmcp.app/mcp",
      "headers": {
        "IMGENX_MODEL": "doubao:model-name",
        "IMGENX_API_KEY": "api-key"
      }
    }
  }
}
```

### 可用工具

#### 1. text_to_image
根据文本描述生成图片。

**参数:**
- `prompt` (str): 图片生成的提示词
- `size` (str): 图片尺寸，支持：
  - 分辨率: `1K`, `2K`, `4K`
  - 像素尺寸: `2048x2048`, `2304x1728`, `1728x2304`, `2560x1440`, `1440x2560`, `2496x1664`, `1664x2496`, `3024x1296`

**返回:** 包含图片 URL 的字典列表

#### 2. image_to_image
基于输入图片和文本描述生成新图片。

**参数:**
- `prompt` (str): 图片生成的提示词
- `images` (List[str]): 输入图片URL列表或本地文件路径列表
- `size` (str): 图片尺寸（同上）

**返回:** 包含图片 URL 的字典列表

#### 3. download_image
下载图片到本地。

**参数:**
- `url` (str): 图片 URL
- `path` (str): 本地保存路径

**返回:** 成功时返回 'success'

#### 4. get_image_info
获取图片信息。

**参数:**
- `image` (str): 图片路径或URL

**返回:** 包含图片信息的字典（格式、尺寸、模式、文件大小）

#### 5. crop_image
裁剪图片。

**参数:**
- `image` (str): 图片路径或URL
- `box` (str): 裁剪区域，格式为 "x,y,width,height"
- `output` (str): 输出文件路径

**返回:** 包含生成图片路径的字典

#### 6. resize_image
调整图片尺寸。

**参数:**
- `image` (str): 图片路径或URL
- `size` (str): 目标尺寸，格式为 "WIDTHxHEIGHT"
- `output` (str): 输出文件路径
- `keep_aspect` (bool): 是否保持宽高比，默认为 True

**返回:** 包含生成图片路径的字典

#### 7. convert_image
转换图片格式。

**参数:**
- `image` (str): 图片路径或URL
- `format` (str): 目标格式（PNG/JPEG/JPG/WEBP）
- `output` (str): 输出文件路径
- `quality` (int): 压缩质量（针对有损格式），默认为 90

**返回:** 包含生成图片路径的字典

#### 8. adjust_image
调整图片的亮度、对比度和饱和度。

**参数:**
- `image` (str): 图片路径或URL
- `output` (str): 输出文件路径
- `brightness` (float): 亮度调整，默认为 1.0
- `contrast` (float): 对比度调整，默认为 1.0
- `saturation` (float): 饱和度调整，默认为 1.0

**返回:** 包含生成图片路径的字典

## 项目结构

```
imgenx-mcp-server/
├── imgenx/
│   ├── server.py                  # MCP 服务器主文件（工具定义与运行）
│   ├── factory.py                 # 图片生成器工厂
│   ├── operator.py                # 图片处理操作模块
│   ├── main.py                    # CLI 入口（imgenx）
│   ├── script.py                  # 命令行生成图片脚本
│   └── image_generator/
│       ├── base/
│       │   └── base_image_generator.py  # 基础生成器接口
│       └── generators/
│           └── doubao_image_generator.py  # 豆包生成器实现
├── pyproject.toml                 # 项目配置（入口脚本等）
├── uv.lock                        # 依赖锁（可选）
└── README.md                      # 项目说明
```

## 扩展新的服务提供商

要添加新的图片生成服务提供商：

1. 在 `imgenx/image_generator/generators/` 目录下创建新的生成器文件，命名格式为 `{provider}_image_generator.py`

2. 实现 `BaseImageGenerator` 接口：
```python
from typing import List, Dict
from imgenx.image_generator.base.base_image_generator import BaseImageGenerator

class ProviderImageGenerator(BaseImageGenerator):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        # 其他初始化代码
    
    def text_to_image(self, prompt: str, size: str) -> List[Dict[str, str]]:
        # 实现文本生成图片逻辑
        # 返回格式: [{"url": "图片URL"}]
        pass
    
    def image_to_image(self, prompt: str, images: List[str], size: str) -> List[Dict[str, str]]:
        # 实现图片生成图片逻辑（可选）
        # 返回格式: [{"url": "图片URL"}]
        pass
```

3. 工厂类会自动发现并加载新的生成器（基于文件名）

## 依赖项

- `fastmcp>=2.12.4`: MCP 协议实现
- `python-dotenv>=1.1.1`: 环境变量加载
- `volcengine-python-sdk[ark]>=4.0.22`: 火山引擎 SDK（豆包服务）
- `requests>=2.25.0`: HTTP 请求库（用于图片下载）
- `pillow>=12.0.0`: 图片处理库（用于图片编辑操作）

## 更新日志

### v0.1.0 (当前版本)

#### 新增功能
- **图片处理工具集**: 新增完整的图片处理功能模块
  - `get_image_info`: 获取图片基本信息（格式、尺寸、模式、文件大小）
  - `crop_image`: 按指定区域裁剪图片
  - `resize_image`: 调整图片尺寸，支持保持宽高比选项
  - `convert_image`: 图片格式转换（PNG/JPEG/JPG/WEBP）
  - `adjust_image`: 图像调整（亮度、对比度、饱和度）

#### 技术改进
- 新增 `operator.py` 模块，集中处理图片操作逻辑
- 新增 `pillow>=12.0.0` 依赖，提供强大的图片处理能力
- 扩展 MCP 工具集从 3 个增加到 8 个
- 支持本地文件和 URL 两种图片输入方式
- 增强错误处理和异常管理

## 许可证

本项目的许可证信息请查看项目仓库。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

- Email: zhangslwork@yeah.net
