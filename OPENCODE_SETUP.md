# OpenCode Integration Guide

## Quick Setup

### 1. Add to OpenCode Configuration

Edit your `~/.config/opencode/opencode.json` (or wherever your OpenCode config is):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "apollo": {
      "type": "local",
      "command": ["node", "/Users/ognjenbabic/apollo-mcp-server/dist/index.js"],
      "environment": {
        "APOLLO_API_KEY": "dgTX61rERjy9tgeu6kmFPg",
        "APOLLO_MASTER_API_KEY": "eLEg-jZ7kMltX0Rrvmbexg"
      },
      "enabled": true
    }
  }
}
```

### 2. Restart OpenCode

After updating the config, restart OpenCode for changes to take effect.

### 3. Verify Integration

In OpenCode, you should now be able to use prompts like:

```
"Use apollo to enrich plauti.com - give me company size, tech stack, and department breakdown"
```

Expected response will include:
- Company size: 58 employees
- Department breakdown with counts
- Tech stack (if available)
- Industry, founding year, location

### 4. Example Prompts

#### Organization Enrichment
```
"Use apollo to get details about stripe.com"
"Enrich microsoft.com using apollo - show me their employee count and tech stack"
```

#### People Search (if your API key supports it)
```
"Search for marketing managers at apollo.io using apollo"
"Find VPs at salesforce.com with apollo"
```

#### Contact Management
```
"Create a contact in apollo for Jane Smith at example.com"
"Search my apollo contacts for anyone at Microsoft"
```

#### Employees Lookup
```
"Find all employees at Stripe using apollo"
"Get a list of engineers at GitHub with apollo"
```

## Available Tools

All 15 tools are available:

**Enrichment:**
- people_enrichment
- organization_enrichment

**Global Search:**
- people_search
- organization_search

**Contact Management:**
- search_contacts
- create_contact
- update_contact
- view_contact
- get_person_email

**Account Management:**
- search_accounts
- create_account (requires master key)
- update_account
- view_account

**Other:**
- organization_job_postings
- employees_of_company

## Troubleshooting

### MCP Server Not Found
- Verify the path in your opencode.json matches: `/Users/ognjenbabic/apollo-mcp-server/dist/index.js`
- Ensure the server was built: `cd ~/apollo-mcp-server && npm run build`

### API Key Issues
- Check `.env` file exists in `~/apollo-mcp-server/`
- Verify keys are correct in opencode.json environment section

### 403 Errors
- Some endpoints require higher-tier API access
- Organization enrichment works with standard keys
- People search may require paid plan

## Testing Without OpenCode

You can test the API directly:

```bash
cd ~/apollo-mcp-server
node dist/test.js
```

This will enrich plauti.com and show you the full response.
