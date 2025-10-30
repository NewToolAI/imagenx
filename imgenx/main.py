from argparse import ArgumentParser


def run():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    server_parser = subparsers.add_parser('server', help='启动 MCP 服务器')
    server_parser.add_argument('--transport', default='stdio', help='stdio|sse|streamable-http')
    server_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to.')
    server_parser.add_argument('--port', default=8000, type=int, help='Port to bind to.')

    gen_parser = subparsers.add_parser('gen', help='生成图片')
    gen_parser.add_argument('prompt', help='生成图片的提示词')
    gen_parser.add_argument('--size', default='2K', help='生成图像的分辨率或宽高像素值')
    gen_parser.add_argument('--output', default='imgenx', help='输出文件或目录路径')

    args = parser.parse_args()

    if args.command == 'server':
        from imgenx.server import mcp
        if args.transport == 'stdio':
            mcp.run(transport='stdio')
        else:
            mcp.run(transport=args.transport, host=args.host, port=args.port)
    elif args.command == 'gen':
        from imgenx import script
        script.run(prompt=args.prompt, size=args.size, output=args.output)


if __name__ == '__main__':
    run()