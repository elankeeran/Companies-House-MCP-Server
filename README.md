# Companies House MCP Server

A Model Context Protocol (MCP) server that provides tools to interact with the UK Companies House API. This server allows AI agents (like Claude) to search for companies, retrieve profiles, check officers, and generate comprehensive due diligence reports.

## Features

- **Search Companies**: Find companies by name or number with advanced filtering.
- **Company Profile**: Get detailed company information (status, address, type, incorporation date).
- **Officers List**: Retrieve current and resigned directors/secretaries with full details.
- **Filing History**: Discover filed documents with transaction IDs for deep research.
- **Document Download**: Retrieve PDF accounts, confirmation statements, PSC filings securely.
- **Beneficial Owners (PSC)**: Identify Persons with Significant Control with ownership percentages.
- **Ownership & Control**: Get PSC statements and detailed control structures.
- **Charges (Mortgages)**: View outstanding and satisfied security interests.
- **Insolvency**: Check for insolvency proceedings (mandatory KYB signal).
- **Officer Network**: Get all appointments for directors (detect serial directors).
- **Disqualifications**: Check for disqualified natural persons and corporate entities.
- **Registered Office**: Direct access to office address without parsing profile.
- **Comprehensive Report**: `generate_company_report` aggregates all data into a single KYB summary.

### Use Cases

- **Know Your Business (KYB)**: Verify companies and beneficial owners for onboarding.
- **Risk Assessment**: Detect insolvency, charges, and disqualifications.
- **Due Diligence**: Deep research via filing history and document access.
- **Ownership Verification**: Complete beneficial owner discovery with control percentages.
- **Director Network Analysis**: Identify connected directors and company networks.

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

### Company Search & Profile
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `search_companies_advanced` | Advanced search for companies by name, number, or address. | `q` (query), `items_per_page`, `start_index`, `api_key` |
| `get_company_profile` | Get basic company details (status, address, type). | `company_number`, `api_key` |

### Filing & Documents
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `get_filing_history_list` | Get list of filings (accounts, returns, etc.). | `company_number`, `category`, `items_per_page`, `start_index`, `api_key` |
| `get_filing_history_item` | Get specific filing details by transaction ID. | `company_number`, `transaction_id`, `api_key` |
| `download_document` | Download document content by document ID. | `document_id`, `api_key` |
| `download_filing_document` | Download a filing document (wraps filing item lookup). | `company_number`, `transaction_id`, `api_key` |

### Officers & Management
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `get_company_officers` | List current and resigned officers (directors/secretaries). | `company_number`, `items_per_page`, `api_key` |
| `get_officer_appointments` | Get all appointments for a specific officer. | `officer_id`, `items_per_page`, `start_index`, `api_key` |

### Ownership & Control (PSC)
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `get_psc_list` | Get list of Persons with Significant Control (beneficial owners). | `company_number`, `items_per_page`, `start_index`, `api_key` |
| `get_psc` | Get details of a specific PSC by type and ID. | `company_number`, `psc_id`, `api_key` |
| `get_psc_statements` | Get PSC statements (e.g., no PSCs found, unknown). | `company_number`, `items_per_page`, `start_index`, `api_key` |

### Risk & Compliance
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `get_insolvency` | Get insolvency proceedings (hard risk signal). | `company_number`, `api_key` |
| `get_disqualification_natural` | Check natural person disqualifications. | `officer_id`, `api_key` |
| `get_disqualification_corporate` | Check corporate entity disqualifications. | `officer_id`, `api_key` |

### Security & Assets
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `get_charges_list` | Get charges/mortgages (secured lending). | `company_number`, `items_per_page`, `start_index`, `api_key` |
| `get_registered_office_address` | Get current registered office address. | `company_number`, `api_key` |

### Comprehensive Reports
| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `generate_company_report` | **Best for Agents**. Full profile + officers + PSCs + charges. | `company_number`, `api_key` |

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
