from fastmcp import FastMCP
from fastmcp.utilities.types import Image


mcp = FastMCP(
    name='imagix-mcp-server',
    instructions='图片生成工具，按照用户需求生成图片',
)




@mcp.tool(description='')
def text_to_image(prompt: str, size: str) -> List[Image]:
    pass



if __name__ == "__main__":
    main()
