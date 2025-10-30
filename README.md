<div align="center">
  <img src="logo.jpeg" alt="ImgenX MCP Server Logo" width="200" height="200">
  
  # ImgenX MCP Server
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#许可证)
  [![GitHub Stars](https://img.shields.io/github/stars/NewToolAI/imgenx_mcp_server?style=social)](https://github.com/NewToolAI/imgenx_mcp_server)
  
  **一个基于 Model Context Protocol (MCP) 的图片生成服务器，支持通过文本描述生成图片并下载到本地。**
</div>

## 功能特性

- **文本生成图片**: 根据文本描述生成高质量图片
- **图片下载**: 将生成的图片下载并保存到本地
- **多种分辨率支持**: 支持 1K、2K、4K 分辨率以及多种自定义尺寸
- **可扩展架构**: 基于插件化设计，易于添加新的图片生成服务提供商
- **MCP 协议**: 完全兼容 Model Context Protocol 标准

## 当前支持的服务提供商

- **豆包 (Doubao)**: 基于火山引擎的图片生成服务

## 安装

### 环境要求

- Python >= 3.10
- 有效的 API 密钥（如豆包 API 密钥）

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/NewToolAI/imgenx_mcp_server.git
cd imgenx-mcp-server
```

2. 安装依赖
```bash
pip install -e .
```

可选：如果你使用 `uv` 管理环境与依赖（推荐），可以：
```bash
uv venv
uv pip install -e .
```

## 使用方法

### 作为 MCP 服务器运行

#### 标准输入输出模式 (stdio)
```bash
imgenx server --transport stdio
```

#### HTTP 服务器模式
```bash
imgenx server --transport streamable-http --host 0.0.0.0 --port 8000
```

#### Server-Sent Events (SSE) 模式
```bash
imgenx server --transport sse --host 0.0.0.0 --port 8000
```

### 配置

服务器需要以下配置参数：

- `model`: 模型标识符，格式为 `provider:model_name`（如 `doubao:model_name`）
- `api_key`: 对应服务提供商的 API 密钥

这些参数可以通过以下方式提供：
1. HTTP 请求头（推荐）
2. 环境变量

示例（环境变量）：
```bash
export IMGENX_MODEL="doubao:your_model_name"
export IMGENX_API_KEY="your_api_key"
```

### 直接使用命令行生成图片

```bash
export IMGENX_MODEL="doubao:your_model_name"
export IMGENX_API_KEY="your_api_key"
imgenx gen --prompt "一只在云上飞翔的猫" --size 2K --output ./images
```

### 可用工具

#### 1. text_to_image
根据文本描述生成图片。

**参数:**
- `prompt` (str): 图片生成的提示词
- `size` (str): 图片尺寸，支持：
  - 分辨率: `1K`, `2K`, `4K`
  - 像素尺寸: `2048x2048`, `2304x1728`, `1728x2304`, `2560x1440`, `1440x2560`, `2496x1664`, `1664x2496`, `3024x1296`

**返回:** 包含图片 URL 的列表

#### 2. download_image
下载图片到本地。

**参数:**
- `url` (str): 图片 URL
- `path` (str): 本地保存路径

**返回:** 成功状态信息

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

1. 在 `image_generator/generators/` 目录下创建新的生成器文件，命名格式为 `{provider}_image_generator.py`

2. 实现 `BaseImageGenerator` 接口：
```python
from image_generator.base.base_image_generator import BaseImageGenerator

class YourProviderImageGenerator(BaseImageGenerator):
    def __init__(self, model: str, api_key: str):
        # 初始化代码
        pass
    
    def text_to_image(self, prompt: str, size: str) -> List[Dict[str, str]]:
        # 实现图片生成逻辑
        pass
```

3. 工厂类会自动发现并加载新的生成器

## 依赖项

- `fastmcp>=2.12.4`: MCP 协议实现
- `python-dotenv>=1.1.1`: 加载环境变量
- `volcengine-python-sdk[ark]>=4.0.22`: 火山引擎 SDK（用于豆包服务）
- `requests`: HTTP 请求库

## 许可证

本项目的许可证信息请查看项目仓库。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

- 项目仓库: https://github.com/NewToolAI/imgenx_mcp_server