<div align="center">
  <img src="logo.jpeg" alt="ImgenX MCP Server Logo" width="200" height="200">
  
  # ImgenX
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#许可证)
  [![GitHub Stars](https://img.shields.io/github/stars/NewToolAI/imgenx_mcp_server?style=social)](https://github.com/NewToolAI/imgenx)

**一个基于豆包API的图片生成命令行工具和MCP Server**
</div>

## 功能特性

- **文本生成图片**: 根据文本描述生成图片
- **图片生成图片**: 基于输入图片和文本描述生成新图片
- **图片下载**: 将生成的图片URL下载并保存到本地
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
git clone https://github.com/NewToolAI/imgenx_mcp_server.git
cd imgenx-mcp-server
pip install -e .
```

## 使用方法

### 作为命令行运行

```
imgenx gen 一只在云上飞翔的猫
imgenx gen --size 2K 一只在云上飞翔的猫
imgenx gen --size 2048x2048 --output test.jpg 一只在云上飞翔的猫
```

### 作为 MCP 服务器运行

#### 标准输入输出模式 (stdio)
```json
{
  "mcpServers": {
    "imgenx-cli": {
      "command": "uvx",
      "args": [
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

## 项目结构

```
imgenx-mcp-server/
├── imgenx/
│   ├── server.py                  # MCP 服务器主文件（工具定义与运行）
│   ├── factory.py                 # 图片生成器工厂
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

class YourProviderImageGenerator(BaseImageGenerator):
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
- `requests`: HTTP 请求库（用于图片下载）

## 许可证

本项目的许可证信息请查看项目仓库。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

- Email: zhangslwork@yeah.net
