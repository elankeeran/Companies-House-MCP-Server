import asyncio
import json
from fastmcp import Client

async def main():
    # Connect to the MCP server
    # Make sure the server is running on port 8001!
    async with Client("http://127.0.0.1:8001/mcp") as c:
        print("Connected to MCP server.\n")
        
        # List available tools
        tools = await c.list_tools()
        print(f"Available Tools ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool.name}")
        
        # Test company number (Barclays Bank PLC)
        test_company_number = "00000006"
        
        # 1. Search Companies
        print("\n" + "="*60)
        print("TEST 1: search_companies")
        print("="*60)
        try:
            resp = await c.call_tool("search_companies", {"q": "Barclays", "items_per_page": 5})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                print(f"  Found {len(result)} companies")
                if "items" in result:
                    print(f"  First result: {result['items'][0].get('company_name', 'N/A')}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 2. Get Company Profile
        print("\n" + "="*60)
        print("TEST 2: get_company_profile")
        print("="*60)
        try:
            resp = await c.call_tool("get_company_profile", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict) and "company_name" in result:
                    print(f"  Company: {result.get('company_name', 'N/A')}")
                    print(f"  Status: {result.get('company_status', 'N/A')}")
                    print(f"  Type: {result.get('type', 'N/A')}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 3. Get Company Officers
        print("\n" + "="*60)
        print("TEST 3: get_company_officers")
        print("="*60)
        try:
            resp = await c.call_tool("get_company_officers", {
                "company_number": test_company_number,
                "items_per_page": 10
            })
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    items = result.get("items", [])
                    print(f"  Found {len(items)} officers")
                    if items:
                        print(f"  First officer: {items[0].get('name', 'N/A')}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 4. Get Filing History
        print("\n" + "="*60)
        print("TEST 4: get_filing_history")
        print("="*60)
        try:
            resp = await c.call_tool("get_filing_history", {
                "company_number": test_company_number,
                "items_per_page": 10
            })
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    items = result.get("items", [])
                    print(f"  Found {len(items)} filings")
                    if items:
                        print(f"  Latest filing: {items[0].get('type', 'N/A')}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 5. Get Company Charges
        print("\n" + "="*60)
        print("TEST 5: get_company_charges")
        print("="*60)
        try:
            resp = await c.call_tool("get_company_charges", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    items = result.get("items", [])
                    total = result.get("total_count", 0)
                    print(f"  Total charges: {total}")
                    print(f"  Returned: {len(items)} charges")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 6. Get Company Insolvency
        print("\n" + "="*60)
        print("TEST 6: get_company_insolvency")
        print("="*60)
        try:
            resp = await c.call_tool("get_company_insolvency", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 7. Get Persons with Significant Control (PSC)
        print("\n" + "="*60)
        print("TEST 7: get_persons_with_significant_control")
        print("="*60)
        try:
            resp = await c.call_tool("get_persons_with_significant_control", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    items = result.get("items", [])
                    print(f"  Found {len(items)} PSCs (Beneficial Owners)")
                    if items:
                        print(f"  First PSC: {items[0].get('name', 'N/A')}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 8. Get Registered Office Address
        print("\n" + "="*60)
        print("TEST 8: get_registered_office_address")
        print("="*60)
        try:
            resp = await c.call_tool("get_registered_office_address", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    address = result.get("address_line_1", "")
                    city = result.get("locality", "")
                    postcode = result.get("postal_code", "")
                    print(f"  Address: {address}, {city} {postcode}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 9. Generate Comprehensive Company Report
        print("\n" + "="*60)
        print("TEST 9: generate_company_report")
        print("="*60)
        try:
            resp = await c.call_tool("generate_company_report", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    print(f"  Company: {result.get('company_name', 'N/A')}")
                    print(f"  Status: {result.get('status', 'N/A')}")
                    print(f"  Active Directors: {len(result.get('active_directors', []))}")
                    print(f"  Beneficial Owners: {len(result.get('beneficial_owners', []))}")
                    charges = result.get('charges_summary', {})
                    print(f"  Outstanding Charges: {charges.get('outstanding_charges', 0)}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
