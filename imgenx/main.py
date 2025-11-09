from argparse import ArgumentParser


def run():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    server_parser = subparsers.add_parser('server', help='启动 MCP 服务器')
    server_parser.add_argument('--transport', default='stdio', help='stdio|sse|streamable-http')
    server_parser.add_argument('--host', default='0.0.0.0', help='主机地址')
    server_parser.add_argument('--port', default=8000, type=int, help='端口')
    server_parser.add_argument('--no_tools', nargs='+', default=None, help='禁用的工具名列表（用空格分隔）')

    image_parser = subparsers.add_parser('image', help='生成图片')
    image_parser.add_argument('prompt', help='生成图片的提示词')
    image_parser.add_argument('--images', nargs='+', default=None, help='输入图片路径列表')
    image_parser.add_argument('--size', default='2K', help='生成图像的分辨率或宽高像素值，分辨率可选值：1K、2K、4K，宽高像素可选值：2048x2048、2304x1728、1728x2304、2560x1440、1440x2560、2496x1664、1664x2496、3024x1296')
    image_parser.add_argument('--output', default='imgenx.jpg', help='输出文件或目录路径')

    video_parser = subparsers.add_parser('video', help='生成视频')
    video_parser.add_argument('prompt', help='生成视频的提示词')
    video_parser.add_argument('--first_frame', default=None, help='输入视频的第一帧路径')
    video_parser.add_argument('--last_frame', default=None, help='输入视频的最后一帧路径')
    video_parser.add_argument('--resolution', default='720p', help='生成视频的分辨率，可选值：480p、720、1080p')
    video_parser.add_argument('--ratio', default='16:9', help='生成视频的宽高比，可选值：16:9、4:3、1:1、3:4、9:16、21:9')
    video_parser.add_argument('--duration', default=5, type=int, help='生成视频的时长，单位秒')
    video_parser.add_argument('--output', default='imgenx.mp4', help='输出文件路径')

    args = parser.parse_args()

    if args.command == 'server':
        from imgenx.server import mcp

        if args.no_tools:
            for tool in args.no_tools:
                mcp.remove_tool(tool)

        if args.transport == 'stdio':
            mcp.run(transport='stdio')
        else:
            mcp.run(transport=args.transport, host=args.host, port=args.port)
    elif args.command == 'image':
        from imgenx import script
        script.gen_image(prompt=args.prompt, size=args.size, output=args.output, images=args.images)
    elif args.command == 'video':
        from imgenx import script
        script.gen_video(prompt=args.prompt, first_frame=args.first_frame, last_frame=args.last_frame,
                   resolution=args.resolution, ratio=args.ratio, duration=args.duration, output=args.output)
    else:
        raise ValueError(f'Unknown command: {args.command}')


if __name__ == '__main__':
    run()