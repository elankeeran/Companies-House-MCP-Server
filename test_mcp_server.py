import asyncio
import json
from fastmcp import Client

async def main():
    # Connect to the MCP server
    # Make sure the server is running on port 8001!
    async with Client("http://127.0.0.1:30001/mcp") as c:
        print("Connected to MCP server.")
        
        # List available tools
        tools = await c.list_tools()
        print("Available Tools:", [t.name for t in tools])

        # 1. Search Companies
        print("\n--- Testing search_companies ---")
        try:
            resp = await c.call_tool("search_companies", {"q": "Barclays"})
            print(resp)
        except Exception as e:
            print(f"Error calling search_companies: {e}")

        # 2. Get Company Profile
        print("\n--- Testing get_company_profile ---")
        try:
            resp = await c.call_tool("get_company_profile", {"company_number": "00000006"})
            print(resp)
        except Exception as e:
            print(f"Error calling get_company_profile: {e}")

        # 3. Get Company Officers
        print("\n--- Testing get_company_officers ---")
        try:
            resp = await c.call_tool("get_company_officers", {"company_number": "00000006"})
            print(resp)
        except Exception as e:
            print(f"Error calling get_company_officers: {e}")

if __name__ == "__main__":
    asyncio.run(main())
