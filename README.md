# Companies House MCP Server

A Model Context Protocol (MCP) server that provides tools to interact with the UK Companies House API. This server allows AI agents (like Claude) to search for companies, retrieve profiles, check officers, and generate comprehensive due diligence reports.

## Features

- **Search Companies**: Find companies by name or number.
- **Company Profile**: Get detailed company information (status, address, type).
- **Officers List**: Retrieve current and resigned directors/secretaries.
- **Filing History**: Access filed accounts, confirmation statements, and other documents.
- **Charges (Mortgages)**: View outstanding and satisfied charges.
- **Insolvency**: Check for insolvency proceedings.
- **Beneficial Owners (PSC)**: Identify Persons with Significant Control.
- **Comprehensive Report**: `generate_company_report` aggregates all the above into a single summary, including calculating shareholder percentages for directors.

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

| Tool Name | Description | Arguments |
|-----------|-------------|-----------|
| `search_companies` | Search for a company. | `q` (query), `api_key` |
| `get_company_profile` | Get basic company details. | `company_number`, `api_key` |
| `get_company_officers` | List directors/secretaries. | `company_number`, `api_key` |
| `generate_company_report` | **Best for Agents**. Returns full profile + officers + ownership info. | `company_number`, `api_key` |

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
