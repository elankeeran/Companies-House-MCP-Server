from __future__ import annotations

import os
import json
from typing import Dict, List, Optional, Any
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
COMPANIES_HOUSE_API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")
CH_BASE_URL = "https://api.company-information.service.gov.uk"

# Initialize FastMCP Server
mcp = FastMCP("CompaniesHouseTools")

# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------

def _get_client(api_key: str | None = None) -> httpx.Client:
    """
    Creates an HTTP client with the appropriate authentication.
    """
    token = api_key or COMPANIES_HOUSE_API_KEY
    if not token:
        raise ValueError("No Companies House API key provided. Pass it as an argument or set COMPANIES_HOUSE_API_KEY env var.")
        
    return httpx.Client(
        base_url=CH_BASE_URL,
        auth=(token, ""),
        timeout=10.0,
    )

def _handle_response(response: httpx.Response) -> Dict | str:
    """
    Standardizes API responses. Returns a Dict for success, or error dict.
    """
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"error": "NOT_FOUND", "message": "Resource not found."}
    elif response.status_code == 401:
        return {"error": "UNAUTHORISED", "message": "Invalid API Key."}
    elif response.status_code == 429:
        return {"error": "RATE_LIMIT", "message": "Too many requests."}
    else:
        return {
            "error": "API_ERROR",
            "status": response.status_code,
            "message": response.text
        }

def _safe_request(endpoint: str, api_key: str | None = None, params: Dict = None) -> Dict | str:
    """
    Executes a safe GET request and handles errors.
    """
    try:
        with _get_client(api_key) as client:
            response = client.get(endpoint, params=params)
            return _handle_response(response)
    except ValueError as e:
        return {"error": "CONFIGURATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"error": "EXCEPTION", "message": str(e)}

# -------------------------------------------------------------------
# MCP Tools
# -------------------------------------------------------------------

@mcp.tool()
def search_companies(q: str, items_per_page: int = 5, start_index: int = 0, api_key: str | None = None) -> Dict | str:
    """
    Search for companies by name, number, or address.
    
    Args:
        q: The search query (e.g., "Barclays", "00000006").
        items_per_page: Number of results to return (default 5).
        start_index: The index of the first result to return (pagination).
        api_key: Optional API Key.
    """
    return _safe_request("/search/companies", api_key, params={"q": q, "items_per_page": items_per_page, "start_index": start_index})

@mcp.tool()
def get_company_profile(company_number: str, api_key: str | None = None) -> Dict | str:
    """
    Get the basic profile of a company (status, address, type, etc.).
    
    Args:
        company_number: The 8-digit company registration number.
        api_key: Optional API Key.
    """
    return _safe_request(f"/company/{company_number}", api_key)

@mcp.tool()
def get_company_officers(company_number: str, items_per_page: int = 20, api_key: str | None = None) -> Dict | str:
    """
    Get the list of officers (directors, secretaries) for a company.
    
    Args:
        company_number: The 8-digit company registration number.
        items_per_page: Number of officers to return.
        api_key: Optional API Key.
    """
    return _safe_request(f"/company/{company_number}/officers", api_key, params={"items_per_page": items_per_page})

@mcp.tool()
def get_filing_history(company_number: str, category: str | None = None, items_per_page: int = 20, api_key: str | None = None) -> Dict | str:
    """
    Get the filing history of a company (accounts, returns, changes).
    
    Args:
        company_number: The 8-digit company registration number.
        category: Optional filter (e.g., 'accounts', 'annual-return', 'confirmation-statement', 'officers').
        items_per_page: Number of items to return.
        api_key: Optional API Key.
    """
    params = {"items_per_page": items_per_page}
    if category:
        params["category"] = category
    return _safe_request(f"/company/{company_number}/filing-history", api_key, params=params)

@mcp.tool()
def get_company_charges(company_number: str, api_key: str | None = None) -> Dict | str:
    """
    Get details of charges (mortgages) registered against the company.
    
    Args:
        company_number: The 8-digit company registration number.
        api_key: Optional API Key.
    """
    return _safe_request(f"/company/{company_number}/charges", api_key)

@mcp.tool()
def get_company_insolvency(company_number: str, api_key: str | None = None) -> Dict | str:
    """
    Get insolvency proceedings information for a company.
    
    Args:
        company_number: The 8-digit company registration number.
        api_key: Optional API Key.
    """
    return _safe_request(f"/company/{company_number}/insolvency", api_key)

@mcp.tool()
def get_persons_with_significant_control(company_number: str, api_key: str | None = None) -> Dict | str:
    """
    Get the Persons with Significant Control (PSC) of a company (Beneficial Owners).
    
    Args:
        company_number: The 8-digit company registration number.
        api_key: Optional API Key.
    """
    return _safe_request(f"/company/{company_number}/persons-with-significant-control", api_key)

@mcp.tool()
def get_registered_office_address(company_number: str, api_key: str | None = None) -> Dict | str:
    """
    Get the current registered office address of a company.
    
    Args:
        company_number: The 8-digit company registration number.
        api_key: Optional API Key.
    """
    return _safe_request(f"/company/{company_number}/registered-office-address", api_key)

@mcp.tool()
def generate_company_report(company_number: str, api_key: str | None = None) -> Dict | str:
    """
    Generates a comprehensive report for a company, including:
    - Basic Profile
    - Officers (Directors)
    - Beneficial Owners (PSCs) with Ownership Percentage
    - Active Charges (Mortgages)
    
    Args:
        company_number: The 8-digit company registration number.
        api_key: Optional API Key.
    """
    # 1. Fetch Profile
    profile = _safe_request(f"/company/{company_number}", api_key)
    if isinstance(profile, dict) and "error" in profile:
        return profile # Return error immediately if company not found
        
    # 2. Fetch Officers
    officers_data = _safe_request(f"/company/{company_number}/officers", api_key, params={"items_per_page": 100})
    officers = officers_data.get("items", []) if isinstance(officers_data, dict) else []
    
    # 3. Fetch PSCs (Beneficial Owners)
    pscs_data = _safe_request(f"/company/{company_number}/persons-with-significant-control", api_key)
    pscs = pscs_data.get("items", []) if isinstance(pscs_data, dict) else []
    
    # 4. Fetch Charges
    charges_data = _safe_request(f"/company/{company_number}/charges", api_key)
    charges_count = charges_data.get("total_count", 0) if isinstance(charges_data, dict) else 0
    active_charges = [c for c in (charges_data.get("items", []) if isinstance(charges_data, dict) else []) if c.get("status") == "outstanding"]

    # 5. Process Beneficial Owners & Ownership
    beneficial_owners = []
    psc_map = {} # Map name -> ownership string

    for psc in pscs:
        ownership = "Unknown"
        natures = psc.get("natures_of_control", [])
        
        if any("75-to-100-percent" in n for n in natures):
            ownership = "75% - 100%"
        elif any("50-to-75-percent" in n for n in natures):
            ownership = "50% - 75%"
        elif any("25-to-50-percent" in n for n in natures):
            ownership = "25% - 50%"
        
        name = psc.get("name", "").upper()
        psc_map[name] = ownership
            
        beneficial_owners.append({
            "name": psc.get("name"),
            "kind": psc.get("kind"),
            "nationality": psc.get("nationality"),
            "country_of_residence": psc.get("country_of_residence"),
            "ownership_percentage": ownership,
            "natures_of_control": natures
        })

    # 6. Process Directors and Match with PSCs
    active_directors = []
    for o in officers:
        if o.get("resigned_on") is None:
            dir_name = o.get("name", "").upper()
            # Simple exact match on name (Companies House names are usually consistent)
            # In production, you might want fuzzy matching
            ownership = psc_map.get(dir_name, "0% (Not a PSC)")
            
            active_directors.append({
                "name": o.get("name"),
                "role": o.get("officer_role"),
                "appointed": o.get("appointed_on"),
                "nationality": o.get("nationality"),
                "country_of_residence": o.get("country_of_residence"),
                "ownership_percentage": ownership
            })

    # 7. Construct Report
    report = {
        "company_name": profile.get("company_name"),
        "company_number": profile.get("company_number"),
        "status": profile.get("company_status"),
        "type": profile.get("type"),
        "incorporation_date": profile.get("date_of_creation"),
        "registered_address": profile.get("registered_office_address"),
        "officers_count": len(officers),
        "active_directors": active_directors,
        "beneficial_owners": beneficial_owners,
        "charges_summary": {
            "total_charges": charges_count,
            "outstanding_charges": len(active_charges)
        },
        "full_profile_source": profile
    }
    
    return report


if __name__ == "__main__":
    # Run the server
    # Using HTTP (Streamable) transport with stateless_http=True to avoid session ID requirement
    mcp.run(transport="http", host="0.0.0.0", port=8001, path="/mcp", stateless_http=True)
