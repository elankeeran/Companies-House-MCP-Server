# Companies House MCP Server

A comprehensive **Know Your Business (KYB)** toolkit via Model Context Protocol (MCP). This server provides 22 production-ready tools that integrate with the UK Companies House API to enable complete due diligence automation, beneficial owner discovery, risk detection, and regulatory compliance.

**Status**: ✅ Production Ready | **Version**: 2.0.0 | **Tools**: 22 (17 new + 5 backward compatible) | **API Endpoints**: 16

## 🎯 The 10 KYB Requirements (All Implemented)

| # | Requirement | Tools | Status |
|---|-------------|-------|--------|
| 1️⃣ | Filing History | `get_filing_history_list()`, `get_filing_history_item()` | ✅ |
| 2️⃣ | Filing Item by Transaction ID | `get_filing_history_item()` | ✅ |
| 3️⃣ | Document Download via MCP | `download_document()`, `download_filing_document()` | ✅ |
| 4️⃣ | PSC (Beneficial Owners) - Full Set | `get_psc_list()`, `get_psc()`, `get_psc_statements()` | ✅ |
| 5️⃣ | Charges (Mortgages/Security) | `get_charges_list()` | ✅ |
| 6️⃣ | Insolvency (MANDATORY KYB) | `get_insolvency()` | ✅ |
| 7️⃣ | Registered Office Address (Direct) | `get_registered_office_address()` | ✅ |
| 8️⃣ | Officer Appointments (Director Network) | `get_officer_appointments()` | ✅ |
| 9️⃣ | Officer Disqualifications (MANDATORY) | `get_disqualification_natural()`, `get_disqualification_corporate()` | ✅ |
| 🔟 | Advanced Company Search | `search_companies_advanced()` | ✅ |

## Features

### Core KYB Capabilities
- ✅ **Company Search & Verification**: Advanced search by name, number, or address with fuzzy matching
- ✅ **Company Profiles**: Complete company details (status, address, incorporation date)
- ✅ **Insolvency Detection** (MANDATORY): Hard-stop risk signal for any credit/partnership decision
- ✅ **Officer Verification**: Directors, secretaries with complete appointment history
- ✅ **Disqualification Checks** (MANDATORY): Screen natural persons and corporate entities
- ✅ **Beneficial Owner Discovery (PSC)**: Identify Persons with Significant Control with ownership %
- ✅ **Officer Network Analysis**: Detect serial directors and company connections
- ✅ **Registered Office Address**: Direct verification without parsing full profile
- ✅ **Filing History & Documents**: Access accounts, confirmations, PSC notifications with PDF download
- ✅ **Charges & Mortgages**: View secured lending exposure and creditor priorities
- ✅ **Comprehensive Reports**: Single-call KYB aggregation (search → verify → risk-check → report)

### Operational Excellence
- **Production Ready**: All 10 requirements implemented, tested, documented
- **Complete API Coverage**: 16 Companies House endpoints fully integrated
- **Pagination Support**: Handle large result sets across all list tools
- **Error Standardization**: Consistent error responses with codes and descriptions
- **Backward Compatible**: 5 legacy tools maintained for existing integrations
- **Stateless Design**: No data stored, secure for public cloud deployment
- **Rate Limiting**: Passes through Companies House rate limits with error codes
- **Base64 Documents**: PDFs returned with metadata for secure transmission

### Use Cases

- **Know Your Business (KYB)**: Complete 10-requirement compliance for company onboarding
- **Risk Assessment**: Insolvency detection, disqualification screening, charge analysis
- **Due Diligence**: Deep research via filing history, document access, officer networks
- **Beneficial Owner Verification**: UBO identification with control percentages
- **Serial Director Detection**: Map director networks across companies
- **Compliance Reporting**: Generate audit trails and risk assessments

## 📚 Documentation

**Getting Started**: Start with one of these based on your needs:

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 5-minute overview of all 10 requirements
- **[INDEX.md](INDEX.md)** - Complete documentation index and navigation hub
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Comprehensive implementation guide
- **[API_ENDPOINT_MAPPING.md](API_ENDPOINT_MAPPING.md)** - Complete API-to-tool reference
- **[REQUIREMENTS_IMPLEMENTATION.md](REQUIREMENTS_IMPLEMENTATION.md)** - Detailed requirement mapping
- **[CHECKLIST.md](CHECKLIST.md)** - Verification checklist

## 🔄 Complete KYB Workflow

This is what a full Know Your Business process looks like using the server:

```
1. Search for company
   → search_companies_advanced("Company Name")
   
2. Verify correct company
   → get_company_profile(company_number)
   
3. ⚠️  CHECK INSOLVENCY (MANDATORY - HARD STOP IF FOUND)
   → get_insolvency(company_number)
   
4. Get company details
   → get_registered_office_address(company_number)
   → get_filing_history_list(company_number)
   
5. Get officers
   → get_company_officers(company_number)
   → For each officer:
      • get_disqualification_natural(officer_id)  [RED FLAG]
      • get_officer_appointments(officer_id)      [NETWORK]
   
6. Get beneficial owners (PSC)
   → get_psc_list(company_number)
   → For each PSC:
      • get_psc(company_number, psc_id)
      • Check disqualifications
   → get_psc_statements(company_number)
   
7. Get financial exposure
   → get_charges_list(company_number)           [MORTGAGES]
   
8. Review documents if needed
   → get_filing_history_list(company_number)
   → download_filing_document(company_number, transaction_id)
   
9. Generate final report
   → generate_company_report(company_number)
```

**Result**: Complete due diligence report with all compliance checks passed ✅

## Architecture

- **Transport**: HTTP (Stateless Streamable) - Ideal for public/cloud deployment.
- **Authentication**: Client-side API Key injection (users provide their own key).
- **Stack**: Python, FastMCP, Docker, Kubernetes.

## Prerequisites

1.  **Companies House API Key**: You must obtain a "Live" API Key from the [Companies House Developer Hub](https://developer.company-information.service.gov.uk/).
2.  **Docker** (for local running).
3.  **Kubernetes** (optional, for deployment).

## Quick Start (Docker)

1.  **Build the Image**:
    ```bash
    docker build -t companies-house-mcp .
    ```

2.  **Run the Container**:
    ```bash
    docker run -p 8001:8001 companies-house-mcp
    ```

3.  **Test with Postman**:
    - Import `mcp_postman_collection.json`.
    - Set the `apiKey` variable to your Companies House API Key.
    - Send a POST request to `http://localhost:8001/mcp`.

## Usage with Claude Desktop (or other MCP Clients)

Configure your MCP client to connect to the server. Since this server uses **HTTP transport**, you might need an adapter or a client that supports HTTP MCP.

**Tool Call Example (JSON-RPC):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_company_report",
    "arguments": {
      "company_number": "00000006",
      "api_key": "YOUR_REAL_API_KEY"
    }
  }
}
```

## Tools Reference

### All 22 Available Tools

#### Company Search & Profile (3 tools)
| Tool | Description | Key Args |
|------|-------------|----------|
| `search_companies_advanced` | Advanced search: name, number, or address | `q`, `items_per_page`, `start_index` |
| `get_company_profile` | Full company details | `company_number` |
| `get_registered_office_address` | Direct office address access | `company_number` |

#### Filing & Documents (4 tools)
| Tool | Description | Key Args |
|------|-------------|----------|
| `get_filing_history_list` | List all filings with pagination | `company_number`, `category`, `items_per_page` |
| `get_filing_history_item` | Get specific filing by transaction ID | `company_number`, `transaction_id` |
| `download_document` | Download document by ID | `document_id` |
| `download_filing_document` | Download filing (lookup + download wrapper) | `company_number`, `transaction_id` |

#### Officers & Management (2 tools)
| Tool | Description | Key Args |
|------|-------------|----------|
| `get_company_officers` | List directors and secretaries | `company_number`, `items_per_page` |
| `get_officer_appointments` | Get all appointments for an officer | `officer_id`, `items_per_page` |

#### Beneficial Owners (PSC) (3 tools)
| Tool | Description | Key Args |
|------|-------------|----------|
| `get_psc_list` | List beneficial owners (Persons with Significant Control) | `company_number`, `items_per_page` |
| `get_psc` | Individual PSC details with ownership info | `company_number`, `psc_id` |
| `get_psc_statements` | PSC statements (e.g., "no PSCs", "unknown") | `company_number`, `items_per_page` |

#### Risk & Compliance (3 tools)
| Tool | Description | Key Args |
|------|-------------|----------|
| `get_insolvency` | ⚠️ MANDATORY: Check insolvency proceedings | `company_number` |
| `get_disqualification_natural` | 🚩 MANDATORY: Check natural person disqualification | `officer_id` |
| `get_disqualification_corporate` | 🚩 MANDATORY: Check corporate disqualification | `officer_id` |

#### Security & Assets (1 tool)
| Tool | Description | Key Args |
|------|-------------|----------|
| `get_charges_list` | List charges/mortgages (secured lending) | `company_number`, `items_per_page` |

#### Comprehensive Reports (1 tool)
| Tool | Description | Key Args |
|------|-------------|----------|
| `generate_company_report` | Full KYB aggregation (Best for agents) | `company_number` |

#### Backward Compatibility (5 deprecated tools)
`search_companies`, `get_filing_history`, `get_company_charges`, `get_persons_with_significant_control`, `get_company_insolvency`
(Still available but use new tools above)

## Deployment (Kubernetes)

1.  **Deploy**:
    ```bash
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    ```
    *(Note: The `secret.yaml` is no longer strictly required if you rely on client-side keys, but can be used for server-side defaults).*

2.  **Access**:
    The service is exposed via NodePort on port `30001` (or LoadBalancer depending on your K8s setup).

## Security Note

This server is designed to be stateless. It does not store your API keys. Keys are passed per-request or configured via environment variables (optional fallback). Ensure you transmit keys over HTTPS in production.

## Companies House API Endpoints Used

### Company Information
- `GET /company/{company_number}` - Full company profile
- `GET /company/{company_number}/registered-office-address` - Office address
- `GET /company/{company_number}/officers` - Officers list
- `GET /company/{company_number}/filing-history` - Filing history with transaction IDs
- `GET /company/{company_number}/filing-history/{transaction_id}` - Individual filing item
- `GET /company/{company_number}/charges` - Charges/mortgages
- `GET /company/{company_number}/insolvency` - Insolvency status

### Persons with Significant Control (PSC)
- `GET /company/{company_number}/persons-with-significant-control` - PSC list
- `GET /company/{company_number}/persons-with-significant-control/{type}/{id}` - Individual PSC
- `GET /company/{company_number}/persons-with-significant-control-statements` - PSC statements

### Officer Management
- `GET /officers/{officer_id}/appointments` - Officer's appointments

### Disqualifications
- `GET /disqualified-officers/natural/{officer_id}` - Natural person disqualifications
- `GET /disqualified-officers/corporate/{officer_id}` - Corporate disqualifications

### Document Access
- `GET /document/{document_id}/content` - Download document content

### Search
- `GET /search/companies` - Company search with filters

## Implementation Notes

### Authentication
All API calls use HTTP Basic Authentication with your Companies House API Key.

### Rate Limiting
The MCP server passes through rate limit errors (HTTP 429). Implement exponential backoff in client applications.

### Error Handling
- **404 NOT_FOUND**: Resource doesn't exist or has been removed.
- **401 UNAUTHORISED**: Invalid or missing API key.
- **429 RATE_LIMIT**: Too many requests. Retry after delay.
- **5xx API_ERROR**: Server error with response body.

### Document Downloads
Document downloads are returned as base64-encoded content with metadata including:
- `document_id`: The document identifier
- `content_type`: MIME type (e.g., application/pdf)
- `content_length`: File size in bytes
- `content_base64`: Base64-encoded file content
