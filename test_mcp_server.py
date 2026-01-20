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
        
        # 1. Search Companies Advanced
        print("\n" + "="*60)
        print("TEST 1: search_companies_advanced")
        print("="*60)
        try:
            resp = await c.call_tool("search_companies_advanced", {"q": "Barclays", "items_per_page": 5})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
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

        # 3. Get Registered Office Address
        print("\n" + "="*60)
        print("TEST 3: get_registered_office_address")
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

        # 4. Get Company Officers
        print("\n" + "="*60)
        print("TEST 4: get_company_officers")
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

        # 5. Get Filing History List
        print("\n" + "="*60)
        print("TEST 5: get_filing_history_list")
        print("="*60)
        try:
            resp = await c.call_tool("get_filing_history_list", {
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
                        print(f"  Transaction ID: {items[0].get('transaction_id', 'N/A')}")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 6. Get PSC List
        print("\n" + "="*60)
        print("TEST 6: get_psc_list")
        print("="*60)
        try:
            resp = await c.call_tool("get_psc_list", {"company_number": test_company_number})
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

        # 7. Get PSC Statements
        print("\n" + "="*60)
        print("TEST 7: get_psc_statements")
        print("="*60)
        try:
            resp = await c.call_tool("get_psc_statements", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    statements = result.get("items", [])
                    print(f"  Found {len(statements)} PSC statements")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 8. Get Charges List
        print("\n" + "="*60)
        print("TEST 8: get_charges_list")
        print("="*60)
        try:
            resp = await c.call_tool("get_charges_list", {"company_number": test_company_number})
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

        # 9. Get Insolvency
        print("\n" + "="*60)
        print("TEST 9: get_insolvency")
        print("="*60)
        try:
            resp = await c.call_tool("get_insolvency", {"company_number": test_company_number})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    if "cases" in result and result["cases"]:
                        print(f"  ⚠️  INSOLVENCY FOUND: {len(result['cases'])} case(s)")
                    else:
                        print(f"  ✓ No insolvency found")
                else:
                    print(f"  Response: {result}")
            else:
                print(f"  Response: {resp}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 10. Get Officer Appointments
        print("\n" + "="*60)
        print("TEST 10: get_officer_appointments")
        print("="*60)
        try:
            # First get an officer ID
            resp = await c.call_tool("get_company_officers", {
                "company_number": test_company_number,
                "items_per_page": 1
            })
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict) and "items" in result and len(result["items"]) > 0:
                    officer_id = result["items"][0].get("links", {}).get("officer", "").split("/")[-1]
                    if officer_id:
                        resp = await c.call_tool("get_officer_appointments", {"officer_id": officer_id})
                        print("✓ Success")
                        if isinstance(resp, list) and len(resp) > 0:
                            appt_result = resp[0]
                            if isinstance(appt_result, dict):
                                appointments = appt_result.get("items", [])
                                print(f"  Found {len(appointments)} appointments for officer")
                    else:
                        print("✗ No officer_id found")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 11. Get Disqualification Natural
        print("\n" + "="*60)
        print("TEST 11: get_disqualification_natural")
        print("="*60)
        try:
            # Using a fake officer ID for demo
            resp = await c.call_tool("get_disqualification_natural", {"officer_id": "000000001"})
            print("✓ Success")
            if isinstance(resp, list) and len(resp) > 0:
                result = resp[0]
                if isinstance(result, dict):
                    if "is_disqualified" in result:
                        status = "🚩 DISQUALIFIED" if result["is_disqualified"] else "✓ Not disqualified"
                        print(f"  {status}")
                else:
                    print(f"  Response: {result}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # 12. Generate Comprehensive Report
        print("\n" + "="*60)
        print("TEST 12: generate_company_report")
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
