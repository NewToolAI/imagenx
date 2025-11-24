from argparse import ArgumentParser


def get_version():
    return '1.0.5'


def run():
    parser = ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=get_version(), help='Show version number')
    subparsers = parser.add_subparsers(dest='command', required=True)

    server_parser = subparsers.add_parser('server', help='Start MCP server')
    server_parser.add_argument('--transport', default='stdio', help='Transport type: stdio, sse, or streamable-http')
    server_parser.add_argument('--host', default='0.0.0.0', help='Host address')
    server_parser.add_argument('--port', default=8000, type=int, help='Port number')
    server_parser.add_argument('--disable_tools', nargs='+', default=None, help='List of disabled tool names (space-separated)')

    image_parser = subparsers.add_parser('image', help='Generate image')
    image_parser.add_argument('prompt', help='Prompt for image generation')
    image_parser.add_argument('--images', nargs='+', default=None, help='Input image path list')
    image_parser.add_argument('--size', default=None, help='Image resolution or pixel dimensions.')
    image_parser.add_argument('--output', default='imagenx.jpg', help='Output file or directory path')

    video_parser = subparsers.add_parser('video', help='Generate video')
    video_parser.add_argument('prompt', help='Prompt for video generation')
    video_parser.add_argument('--first_frame', default=None, help='Path to the first frame of input video')
    video_parser.add_argument('--last_frame', default=None, help='Path to the last frame of input video')
    video_parser.add_argument('--resolution', default='720p', help='Video resolution. Options: 480p, 720p, 1080p')
    video_parser.add_argument('--ratio', default='16:9', help='Video aspect ratio. Options: 16:9, 4:3, 1:1, 3:4, 9:16, 21:9')
    video_parser.add_argument('--duration', default=5, type=int, help='Video duration in seconds')
    video_parser.add_argument('--output', default='imagenx.mp4', help='Output file path')

    args = parser.parse_args()

    if args.command == 'server':
        from imagenx.server import mcp

        if args.disable_tools:
            for tool in args.disable_tools:
                mcp.remove_tool(tool)

        if args.transport == 'stdio':
            mcp.run(transport='stdio')
        else:
            mcp.run(transport=args.transport, host=args.host, port=args.port)
    elif args.command == 'image':
        from imagenx import script
        script.gen_image(prompt=args.prompt, size=args.size, output=args.output, images=args.images)
    elif args.command == 'video':
        from imagenx import script
        script.gen_video(prompt=args.prompt, first_frame=args.first_frame, last_frame=args.last_frame,
                   resolution=args.resolution, ratio=args.ratio, duration=args.duration, output=args.output)
    else:
        raise ValueError(f'Unknown command: {args.command}')


if __name__ == '__main__':
    run()