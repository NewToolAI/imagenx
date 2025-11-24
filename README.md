<div align="center">
  <img src="logo.jpg" alt="Imagenx MCP Server Logo" width="800" height="400">
  
  [![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)](https://github.com/NewToolAI/imagenx/releases)
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#许可证)

**AI 图片/视频生成与处理套件，支持文本/图生图、文本/图生视频、图片分析与常用编辑（裁剪、缩放、转换、调参），可作为命令行工具或 MCP Server 使用**
</div>

https://github.com/user-attachments/assets/92749d6f-727e-4874-a008-6ded8b4d9e7b

## 功能特性

- **文本生成图片**: 根据文本描述生成图片
 - **图片生成图片**: 基于输入图片和文本描述生成新图片
 - **文本/图片生成视频**: 支持提示词生成视频，或基于首尾帧生成视频
 - **图片下载/视频下载**: 将生成的图片或视频URL下载并保存到本地
- **图片处理工具**: 提供完整的图片处理功能
  - **图片信息获取**: 查看图片格式、尺寸、模式等信息
  - **图片裁剪**: 按指定区域裁剪图片（支持小数比例坐标）
  - **尺寸调整**: 调整图片大小，支持保持宽高比
  - **格式转换**: 支持PNG、JPEG、JPG、WEBP格式转换
  - **图像调整**: 调整亮度、对比度、饱和度
  - **图片粘贴**: 将图片粘贴到背景图片的指定位置
- **图片理解与分析**: 基于视觉模型分析图片内容，输出结构化或文本结果
- **多种分辨率支持**: 支持 1K、2K、4K 分辨率以及多种自定义像素尺寸
- **插件化架构**: 基于工厂模式设计，支持扩展新的图片生成服务提供商
- **MCP 协议支持**: 兼容 Model Context Protocol 标准

## 当前支持的服务提供商

- **豆包 (Doubao)**: 基于火山引擎的图片生成服务
- **阿里云 (Aliyun)**: 基于阿里云通义千问的图片生成服务

## 安装

### 配置环境变量

```
IMAGENX_IMAGE_TO_IMAGE="provider:model"
IMAGENX_TEXT_TO_IMAGE="provider:model"
IMAGENX_IMAGE_TO_VIDEO="provider:model"
IMAGENX_TEXT_TO_VIDEO="provider:model"
IMAGENX_INSPECT_IMAGE="provier:model"
IMAGENX_<provider>_API_KEY="api-key"
```
或写入 .env 文件中

### 安装步骤

#### 方式一：pip 安装（推荐）

```bash
pip install imagenx
```

#### 方式二：从源码安装
```bash
git clone https://github.com/NewToolAI/imagenx.git
cd imagenx
pip install -e .
```

## 使用方法

### 作为命令行运行

```
# 生成图片（文本或图生图）
imagenx image "一只在云上飞翔的猫"

# 生成视频（文本或基于首尾帧）
imagenx video "一个人在运动"
imagenx video "一个人在运动" --first_frame logo.jpg
```

### 作为 MCP 服务器运行

#### 标准输入输出模式 (stdio)
```json
{
  "mcpServers": {
    "imagenx-cli": {
      "command": "uvx",
      "args": [
        "-U",
        "imagenx",
        "server",
        "--diable_tools",
        "text_to_video image_to_video"
      ],
      "env": {
        "IMAGENX_IMAGE_TO_IMAGE": "doubao:doubao-seedream-4-0-250828",
        "IMAGENX_TEXT_TO_IMAGE": "doubao:doubao-seedream-4-0-250828",
        "IMAGENX_IMAGE_TO_VIDEO": "doubao:doubao-seedance-1-0-pro-fast-251015",
        "IMAGENX_TEXT_TO_VIDEO": "doubao:doubao-seedance-1-0-pro-fast-251015",
        "IMAGENX_INSPECT_IMAGE": "aliyun:qwen3-vl-flash",
        "IMAGENX_DOUBAO_API_KEY": "api-key",
        "IMAGENX_ALIYUN_API_KEY": "api-key"
      }
    }
  }
}
```

#### HTTP 服务器模式
```bash
imagenx server --transport streamable-http --host 0.0.0.0 --port 8000
imagenx server --transport streamable-http --disable_tools text_to_video image_to_video  # 禁用视频生成工具
```

```json
{
  "mcpServers": {
    "imagenx-mcp-aliyun": {
      "url": "http://127.0.0.1:8000/mcp",
      "headers": {
        "IMAGENX_IMAGE_TO_IMAGE": "aliyun:qwen-image-edit-plus",
        "IMAGENX_TEXT_TO_IMAGE": "aliyun:qwen-image-plus",
        "IMAGENX_IMAGE_TO_VIDEO": "aliyun:wan2.5-i2v-preview",
        "IMAGENX_TEXT_TO_VIDEO": "aliyun:wan2.5-t2v-preview",
        "IMAGENX_INSPECT_IMAGE": "aliyun:qwen3-vl-flash",
        "IMAGENX_ALIYUN_API_KEY": "api-key"
      }
    }
  }
}
```

#### Cloud 免安装 (没有工具 download)
```
{
  "mcpServers": {
    "imagenx-mcp-cloud": {
      "url": "https://imagenx.fastmcp.app/mcp",
      "headers": {
        "IMAGENX_IMAGE_TO_IMAGE": "aliyun:qwen-image-edit-plus",
        "IMAGENX_TEXT_TO_IMAGE": "aliyun:qwen-image-plus",
        "IMAGENX_IMAGE_TO_VIDEO": "aliyun:wan2.5-i2v-preview",
        "IMAGENX_TEXT_TO_VIDEO": "aliyun:wan2.5-t2v-preview",
        "IMAGENX_INSPECT_IMAGE": "aliyun:qwen3-vl-flash",
        "IMAGENX_ALIYUN_API_KEY": "api-key"
      }
    }
  }
}
```

### 可用工具

#### 1. text_to_image
根据文本描述生成图片。

#### 2. image_to_image
基于输入图片和文本描述生成新图片。

#### 3. download
下载图片或视频到本地。

#### 4. get_image_info
获取图片信息。

#### 5. crop_image
裁剪图片。

#### 6. resize_image
调整图片尺寸。

#### 7. convert_image
转换图片格式。

#### 8. adjust_image
调整图片的亮度、对比度和饱和度。

#### 9. text_to_video
根据文本提示生成视频。

#### 10. image_to_video
基于首帧与可选尾帧生成视频。

#### 11. paste_image
将图片粘贴到背景图片的指定位置。

#### 12. inspect_image
分析图片内容，返回结构化或文本结果。

## 项目结构

```
imagenx/
├── imagenx/
│   ├── server.py                  # MCP 服务器主文件（工具定义与运行）
│   ├── factory.py                 # 预测器工厂（图片/视频/分析）
│   ├── operator.py                # 图片处理操作模块
│   ├── main.py                    # CLI 入口（imagenx）
│   ├── script.py                  # 命令行生成图片/视频脚本
│   ├── utils.py                   # 工具函数模块
│   └── predictor/
│       ├── base/
│       │   ├── base_text_to_image.py      # 文本生成图片接口
│       │   ├── base_image_to_image.py     # 图片生成图片接口
│       │   ├── base_text_to_video.py      # 文本生成视频接口
│       │   ├── base_image_to_video.py     # 图片生成视频接口
│       │   └── base_image_inspector.py    # 图片分析接口
│       └── generators/
│           ├── doubao/                    # 豆包服务提供商
│           │   ├── text_to_image.py
│           │   ├── image_to_image.py
│           │   ├── text_to_video.py
│           │   ├── image_to_video.py
│           │   └── image_inspector.py
│           └── aliyun/                   # 阿里云服务提供商
│               ├── text_to_image.py
│               ├── image_to_image.py
│               ├── text_to_video.py
│               ├── image_to_video.py
│               └── image_inspector.py
├── pyproject.toml                 # 项目配置（入口脚本等）
├── uv.lock                        # 依赖锁（可选）
└── README.md                      # 项目说明
```

## 扩展新的服务提供商

要扩展新的服务提供商：

1. 实现相应的基类接口，例如 `BaseTextToImage`：

```python
from imagenx.predictor.base.base_text_to_image import BaseTextToImage

class ProviderTextToImage(BaseTextToImage):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        # 其他初始化代码
    
    def text_to_image(self, prompt: str, size: str) -> List[Dict[str, str]]:
        # 实现文本生成图片逻辑
        # 返回格式: [{"url": "图片URL"}]
        pass
```

2. 工厂类会自动发现并加载新的实现（基于文件名），模型字符串需为 `provider:model` 格式，例如：`doubao:doubao-seedream-4-0-250828`

## 依赖项

- `fastmcp>=2.12.4`: MCP 协议实现
- `python-dotenv>=1.1.1`: 环境变量加载
- `volcengine-python-sdk[ark]>=4.0.22`: 火山引擎 SDK（豆包服务）
- `dashscope>=1.25.1`: 阿里云通义千问 SDK（阿里云服务）
- `requests>=2.25.0`: HTTP 请求库（用于图片下载）
- `pillow>=12.0.0`: 图片处理库（用于图片编辑操作）

## 更新日志

### v0.3.0 (当前版本)

#### 新增功能
- **阿里云服务提供商**: 新增基于阿里云通义千问的图片生成服务支持
- **图片粘贴**: 新增 `paste_image` 工具，支持将图片粘贴到背景图片的指定位置
- **工具控制**: 新增 `--disable_tools` 参数，支持在运行 MCP 服务器时禁用特定工具

#### 功能优化
- 完善图片处理工具集，增强图片编辑能力
- 重构基类接口，提供更细分的功能模块

### v0.2.0

#### 新增功能
- **视频生成**: 支持 `text_to_video` 与 `image_to_video` 两种方式
- **图片分析**: 新增 `inspect_image` 工具，支持视觉模型分析
- **图片处理工具集完善**: `get_image_info`、`crop_image`（比例坐标）、`resize_image`、`convert_image`、`adjust_image`

#### 技术改进
- 工厂模式统一图片/视频/分析三类预测器的发现与加载
- 环境变量分离为 `IMAGENX_IMAGE_MODEL`、`IMAGENX_VIDEO_MODEL`、`IMAGENX_INSPECT_IMAGE`
- MCP 工具集扩展，HTTP 服务器提供 `/health`、`/healthy` 健康检查路由
- 支持本地文件与 URL 两种图片输入方式；下载工具统一图片/视频

## 许可证

本项目的许可证信息请查看项目仓库。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

- Email: zhangslwork@yeah.net
