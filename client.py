from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio

async def run():
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

            if "get_restaurant_menu" not in [tool.name for tool in tools.tools]:
                print("Error: get_restaurant_menu tool not found in available tools")
                return

            # Call the restaurant menu tool
            try:
                result = await session.call_tool(
                    "get_restaurant_menu",
                    arguments={
                        "restaurant_id": 255,
                        "branch_id": 2942,
                        "brand_id": "7c15f9e7-cec4-11ed-8648-129754d6b903"
                    }
                )
                
                if result.content and result.content[0].text:
                    print("\nCategories found:")
                    for category in result.content[0].text:
                        print(f"- {category}")
                else:
                    print("No categories found in response")
                    
            except Exception as e:
                print(f"Error calling tool: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run()) 