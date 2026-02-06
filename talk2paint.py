import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai
from concurrent.futures import TimeoutError
from functools import partial

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

max_iterations = 3
last_response = None
iteration = 0
iteration_response = []

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []

async def main():
    reset_state()  # Reset at the start of main
    print("Starting main execution...")
    try:
        # Create a single MCP server connection
        print("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python",
            args=["example2.py"]
        )

        async with stdio_client(server_params) as (read, write):
            print("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                print("Session created, initializing...")
                await session.initialize()
                
                # Get available tools
                print("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"Successfully retrieved {len(tools)} tools")
                                
                print("\n=== Agent Execution Complete ===")
                result = await session.call_tool(
                "draw_rectangle_excalidraw",
                arguments={"x1": 300, "y1": 300, "x2": 600, "y2": 500}
                )
                print(result.content[0].text)
                str1 = input("enter your name")
                # result = await session.call_tool("open_paint")
                # print(result.content[0].text)

                # # Wait longer for Paint to be fully maximized
                # await asyncio.sleep(1)

                # #Draw a rectangle
                # result = await session.call_tool(
                #     "draw_rectangle",
                #     arguments={
                #         "x1": 100,
                #         "y1": 150,
                #         "x2": 400,
                #         "y2": 450
                #     }
                # )
                # await asyncio.sleep(1)
                # print(result.content[0].text)
                # response_text = "Hello World"
                # # Draw rectangle and add text
                # result = await session.call_tool(
                #     "add_text_in_paint",
                    
                #     arguments={
                #         "text": response_text
                #     }
                # )
                # print(result.content[0].text)
                


    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        reset_state()  # Reset at the end of main

if __name__ == "__main__":
    asyncio.run(main())
    
    
