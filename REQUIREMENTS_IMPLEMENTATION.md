# Companies House MCP Server - Requirements Implementation

This document details the implementation of 10 core KYB (Know Your Business) requirements for the Companies House MCP Server.

## ✅ Requirement 1: Filing History

**API**: `/company/{company_number}/filing-history`

**Purpose**: Discover which documents exist. Foundation for long search / deep check.

**MCP Tools Implemented**:
- `get_filing_history_list(company_number, category, items_per_page, start_index, api_key)`
  - Lists all filings for a company (accounts, returns, confirmation statements, etc.)
  - Supports pagination
  - Optional category filtering

**Use Cases**:
- Discover all filed documents
- Identify specific filing types (e.g., annual accounts)
- Foundation for document-based research

---

## ✅ Requirement 2: Filing Item by Transaction ID

**API**: `/company/{company_number}/filing-history/{transaction_id}`

**Purpose**: Links filings → document metadata. Needed before downloading PDFs.

**MCP Tools Implemented**:
- `get_filing_history_item(company_number, transaction_id, api_key)`
  - Retrieves specific filing details including document metadata
  - Returns filing date, document type, and document ID

**Use Cases**:
- Retrieve document_id needed for PDF download
- Get detailed metadata about specific filings
- Verify filing authenticity and date

---

## ✅ Requirement 3: Document Download (via MCP)

**API**: `/document/{document_id}/content`

**Purpose**: Fetch accounts, confirmation statements, PSC filings. Hidden behind MCP (auth, redirects, rate-limit).

**MCP Tools Implemented**:
- `download_document(document_id, api_key)`
  - Downloads raw document content
  - Returns base64-encoded content with metadata
  - Handles authentication and rate limiting

- `download_filing_document(company_number, transaction_id, api_key)`
  - Convenience wrapper that:
    1. Retrieves filing item to extract document_id
    2. Downloads the document
    3. Returns complete document with metadata

**Use Cases**:
- Download annual accounts PDFs
- Retrieve confirmation statements
- Access PSC notification documents
- Secure document access with built-in auth

---

## ✅ Requirement 4: PSC (Persons with Significant Control) – Full Set

**APIs**:
- `/persons-with-significant-control`
- `/persons-with-significant-control/{type}/{id}`
- `/persons-with-significant-control-statements`

**Purpose**: Core for ownership / UBO / control. Required for bank KYB.

**MCP Tools Implemented**:
- `get_psc_list(company_number, items_per_page, start_index, api_key)`
  - Lists all beneficial owners (PSCs) with:
    - Name, type, nationality, country of residence
    - Natures of control (ownership %, voting rights, etc.)
  - Supports pagination

- `get_psc(company_number, psc_id, api_key)`
  - Get detailed information for specific beneficial owner
  - Format: `{type}/{id}` (e.g., `individual/12345` or `corporate/54321`)
  - Returns full beneficial ownership details

- `get_psc_statements(company_number, items_per_page, start_index, api_key)`
  - Retrieve PSC statements
  - Examples: "No persons with significant control", "PSC identity unknown", "Persons with significant control ceased"

**Use Cases**:
- Identify Ultimate Beneficial Owners (UBO)
- Verify ownership structure
- KYB beneficial owner verification
- Track ownership changes via statements

---

## ✅ Requirement 5: Charges (Mortgages / Security)

**API**: `/company/{company_number}/charges`

**Purpose**: Shows secured lending exposure. Important for risk + lending decisions.

**MCP Tools Implemented**:
- `get_charges_list(company_number, items_per_page, start_index, api_key)`
  - Lists all charges/mortgages against company
  - Returns status (outstanding/satisfied), amount, creditor, date
  - Supports pagination

**Use Cases**:
- Assess secured lending exposure
- Evaluate company's financial obligations
- Risk assessment for credit decisions
- Identify creditor priorities

---

## ✅ Requirement 6: Insolvency

**API**: `/company/{company_number}/insolvency`

**Purpose**: Immediate hard risk signal. Mandatory KYB check.

**MCP Tools Implemented**:
- `get_insolvency(company_number, api_key)`
  - Check if company is in insolvency proceedings
  - Returns case details, court, dates
  - Status field indicates proceeding type

**Use Cases**:
- **Mandatory risk check** for KYB procedures
- Immediate disqualification for lending/partnerships
- Track insolvency history
- Regulatory compliance verification

---

## ✅ Requirement 7: Registered Office Address (Direct)

**API**: `/company/{company_number}/registered-office-address`

**Purpose**: Often required independently in onboarding. Cleaner than parsing profile.

**MCP Tools Implemented**:
- `get_registered_office_address(company_number, api_key)`
  - Direct access to office address
  - Returns complete address components
  - Cleaner than extracting from full profile

**Use Cases**:
- Onboarding address verification
- Address change detection
- Compliance reporting
- Direct address queries without full profile

---

## ✅ Requirement 8: Officer Appointments (Director Network)

**API**: `/officers/{officer_id}/appointments`

**Purpose**: Detect serial directors. Used for enhanced KYB risk.

**MCP Tools Implemented**:
- `get_officer_appointments(officer_id, items_per_page, start_index, api_key)`
  - Get all company appointments for an officer
  - Shows director connections across companies
  - Includes appointment dates and status
  - Supports pagination

**Use Cases**:
- Detect serial directors (high-risk pattern)
- Map director networks
- Identify company relationships
- Enhanced KYB risk assessment

---

## ✅ Requirement 9: Officer Disqualifications

**APIs**:
- `/disqualified-officers/natural/{officer_id}`
- `/disqualified-officers/corporate/{officer_id}`

**Purpose**: Mandatory red-flag check.

**MCP Tools Implemented**:
- `get_disqualification_natural(officer_id, api_key)`
  - Check if natural person is disqualified from directing
  - Returns disqualification date and reason
  - **Mandatory check** for natural person directors

- `get_disqualification_corporate(officer_id, api_key)`
  - Check if corporate entity is disqualified from directing
  - Returns disqualification details
  - **Mandatory check** for corporate directors

**Use Cases**:
- **Red-flag check** during KYB
- Regulatory compliance
- Risk assessment for directors
- Corporate governance verification

---

## ✅ Requirement 10: Advanced Company Search

**API**: `/search/companies` (with filters)

**Purpose**: Resolve name ambiguity. Reduce wrong-company selection.

**MCP Tools Implemented**:
- `search_companies_advanced(q, items_per_page, start_index, api_key)`
  - Search companies by:
    - Company name (with fuzzy matching)
    - Company number (exact 8-digit match)
    - Address components
  - Returns multiple matches with scores
  - Supports pagination
  - **Prevents selection of wrong company** (critical for KYB)

**Use Cases**:
- Resolve name ambiguity (e.g., multiple "Smith Ltd")
- Verify correct company before fetching details
- Fallback search for partial information
- Address-based company finding

---

## API Tool Summary

### All New MCP Tools (20 total)

#### Company Search & Basic Info
1. ✅ `search_companies_advanced` - Advanced company search
2. ✅ `get_company_profile` - Basic profile (existing, enhanced)
3. ✅ `get_registered_office_address` - Direct office address

#### Filing & Documents
4. ✅ `get_filing_history_list` - List filings
5. ✅ `get_filing_history_item` - Individual filing details
6. ✅ `download_document` - Download by document ID
7. ✅ `download_filing_document` - Download filing wrapper

#### Officers & Management
8. ✅ `get_company_officers` - Officers list (existing, enhanced)
9. ✅ `get_officer_appointments` - Officer's appointments network

#### Ownership & Control (PSC)
10. ✅ `get_psc_list` - PSC list
11. ✅ `get_psc` - Individual PSC details
12. ✅ `get_psc_statements` - PSC statements

#### Risk & Compliance
13. ✅ `get_insolvency` - Insolvency status
14. ✅ `get_disqualification_natural` - Natural person disqualifications
15. ✅ `get_disqualification_corporate` - Corporate disqualifications

#### Security & Assets
16. ✅ `get_charges_list` - Charges/mortgages list

#### Comprehensive Reports
17. ✅ `generate_company_report` - Full KYB report (existing, enhanced)

#### Deprecated (backward compatibility)
18. ✅ `search_companies` - Legacy search
19. ✅ `get_filing_history` - Legacy filing history
20. ✅ `get_company_charges` - Legacy charges
21. ✅ `get_persons_with_significant_control` - Legacy PSC
22. ✅ `get_company_insolvency` - Legacy insolvency

---

## KYB (Know Your Business) Workflow

The tools enable a complete KYB workflow:

```
1. Search for company (search_companies_advanced)
   ↓
2. Get company profile (get_company_profile)
   ↓
3. Check insolvency ⚠️ MANDATORY (get_insolvency)
   ↓
4. Get registered office address (get_registered_office_address)
   ↓
5. Get officers list (get_company_officers)
   ↓
6. For each officer:
   - Check disqualifications (get_disqualification_natural)
   - Get appointments network (get_officer_appointments)
   ↓
7. Get beneficial owners (get_psc_list)
   ↓
8. For each PSC:
   - Get individual details (get_psc)
   - Check disqualifications
   ↓
9. Get charges/mortgages (get_charges_list)
   ↓
10. Get PSC statements (get_psc_statements)
   ↓
11. Review filing history (get_filing_history_list)
   ↓
12. Download key documents (download_filing_document)
   ↓
13. Generate comprehensive report (generate_company_report)
```

---

## Error Handling

All tools implement standardized error handling:

```json
{
  "error": "ERROR_CODE",
  "message": "Human readable message"
}
```

Error codes:
- `NOT_FOUND` - Resource doesn't exist
- `UNAUTHORISED` - Invalid API key
- `RATE_LIMIT` - Too many requests
- `CONFIGURATION_ERROR` - Missing API key
- `EXCEPTION` - Unexpected error

---

## Testing

All tools have been implemented and syntax-verified. Test with:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_filing_history_list",
    "arguments": {
      "company_number": "00000006",
      "api_key": "YOUR_API_KEY"
    }
  }
}
```

---

## Documentation

- **Main README**: Complete tool reference with use cases
- **This Document**: Detailed requirement mapping
- **MCP Postman Collection**: Pre-configured HTTP requests
- **Inline Docstrings**: Tool documentation in Python

---

## Version

- **Implementation Date**: January 2026
- **All 10 Requirements**: ✅ COMPLETE
- **Total New Tools**: 17 (+ 4 deprecated for backward compatibility)
- **Backward Compatibility**: ✅ MAINTAINED
