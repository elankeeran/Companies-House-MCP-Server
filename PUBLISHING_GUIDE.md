# MCP Registry Publication Guide

## Your Server is Ready! 🎉

Your `server.json` is properly configured for MCP registry publication. To complete the registration process:

### Option 1: Use mcp-publisher CLI (Local Machine)

On your local machine (macOS/Linux with Go installed):

```bash
# 1. Clone the MCP registry
git clone https://github.com/modelcontextprotocol/registry.git
cd registry

# 2. Build the publisher
make publisher

# 3. Navigate to your Companies House MCP directory
cd /path/to/Companies-House-MCP-Server

# 4. Authenticate with GitHub
/path/to/registry/bin/mcp-publisher login github
# (You'll be prompted to enter a GitHub Personal Access Token)

# 5. Publish your server
/path/to/registry/bin/mcp-publisher publish
```

**GitHub Token Requirements:**
- Visit: https://github.com/settings/tokens
- Create a "Personal access token (classic)"
- Select scopes: `public_repo`
- This proves you control the `io.github.elankeeran` namespace

### Option 2: Direct Registry Submission (Recommended for This Environment)

1. Visit the MCP Registry: https://registry.modelcontextprotocol.io

2. Follow their direct submission process, or

3. Open an issue on the MCP Registry GitHub: https://github.com/modelcontextprotocol/registry/issues
   - Title: "Register Companies House MCP Server"
   - Include your `server.json` content

### Option 3: Pull Request to Registry (Advanced)

1. Fork https://github.com/modelcontextprotocol/registry
2. Add your server.json to the appropriate data directory
3. Submit a PR for maintainer review

---

## Your Server Details

- **Namespace**: `io.github.elankeeran/companies-house-mcp`
- **Live URL**: `https://companies-house-mcp-server.onrender.com`
- **Transport**: SSE (Server-Sent Events)
- **Tools**: 9 comprehensive tools for UK Companies House API integration

---

## Next Steps

Your server is production-ready. Once registered, it will be discoverable by:
- Claude Desktop
- VS Code with MCP extension
- Other MCP-compatible clients
- The public MCP Registry

The registration typically takes 24-48 hours for approval once submitted.
