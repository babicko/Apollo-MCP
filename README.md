# Apollo.io MCP Server

A comprehensive Model Context Protocol (MCP) server for Apollo.io API integration. Enables AI assistants to enrich company data, search for people and organizations, manage contacts and accounts, and more.

## Features

### 🔍 Enrichment Tools
- **People Enrichment** - Enrich person data by name/email/domain
- **Organization Enrichment** - Get company size, tech stack, department breakdown, funding, revenue

### 🌐 Global Search Tools  
- **People Search** - Search Apollo's 275M+ person database
- **Organization Search** - Search Apollo's 70M+ company database

### 👥 Contact Management (Your Apollo Account)
- **Search Contacts** - Find contacts you've saved
- **Create Contact** - Add new contacts
- **Update Contact** - Modify existing contacts
- **View Contact** - Get contact details
- **Get Person Email** - Reveal email addresses

### 🏢 Account Management (Your Apollo Account)
- **Search Accounts** - Find accounts (companies) you've saved
- **Create Account** - Add new accounts (requires master key)
- **Update Account** - Modify existing accounts  
- **View Account** - Get account details

### 💼 Other Tools
- **Organization Job Postings** - Get job listings for a company
- **Employees of Company** - Find employees by company name/URL

## Installation

```bash
# Clone or download the repository
cd apollo-mcp-server

# Install dependencies
npm install

# Build the TypeScript
npm run build
```

## Configuration

### 1. Set up API Keys

Create a `.env` file in the project root:

```bash
APOLLO_API_KEY=your_standard_api_key_here
APOLLO_MASTER_API_KEY=your_master_api_key_here
```

Get your API keys from [Apollo.io Settings → API](https://app.apollo.io/#/settings/integrations/api)

### 2. Configure with OpenCode

Add to your `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "apollo": {
      "type": "local",
      "command": ["node", "/Users/ognjenbabic/apollo-mcp-server/dist/index.js"],
      "environment": {
        "APOLLO_API_KEY": "your_key_here",
        "APOLLO_MASTER_API_KEY": "your_master_key_here"
      },
      "enabled": true
    }
  }
}
```

Or use environment variables:

```json
{
  "mcp": {
    "apollo": {
      "type": "local",
      "command": ["node", "/Users/ognjenbabic/apollo-mcp-server/dist/index.js"],
      "environment": {
        "APOLLO_API_KEY": "{env:APOLLO_API_KEY}",
        "APOLLO_MASTER_API_KEY": "{env:APOLLO_MASTER_API_KEY}"
      },
      "enabled": true
    }
  }
}
```

### 3. Configure with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "apollo": {
      "command": "node",
      "args": ["/Users/ognjenbabic/apollo-mcp-server/dist/index.js"],
      "env": {
        "APOLLO_API_KEY": "your_key_here",
        "APOLLO_MASTER_API_KEY": "your_master_key_here"
      }
    }
  }
}
```

## Usage Examples

### With OpenCode

Once configured, you can interact with Apollo through natural language:

```
"Use apollo to enrich plauti.com - give me company size, tech stack, and department breakdown"
```

```
"Search for marketing managers at apollo.io using apollo"
```

```
"Find employees of Stripe using apollo"
```

```
"Create a contact in apollo for John Doe at example.com"
```

### Direct Tool Usage

#### Organization Enrichment
```json
{
  "tool": "organization_enrichment",
  "arguments": {
    "domain": "plauti.com"
  }
}
```

Returns:
- Company size (employee count)
- Tech stack (technologies used)
- Department breakdown
- Industry, revenue, funding
- Location, phone, social profiles

#### People Search
```json
{
  "tool": "people_search",
  "arguments": {
    "person_titles": ["VP of Marketing", "Marketing Manager"],
    "q_organization_domains_list": ["apollo.io"],
    "per_page": 10
  }
}
```

#### Employees of Company
```json
{
  "tool": "employees_of_company",
  "arguments": {
    "company": "Stripe",
    "website_url": "https://stripe.com",
    "person_titles": ["Engineer", "Developer"]
  }
}
```

## Available Tools (15 Total)

| Tool | Description | Credit Cost |
|------|-------------|-------------|
| `people_enrichment` | Enrich person data | 1 credit |
| `organization_enrichment` | Enrich company data | 1 credit |
| `people_search` | Search global people database | Free |
| `organization_search` | Search global company database | Free |
| `search_contacts` | Search your contacts | Free |
| `create_contact` | Add new contact | 1 credit |
| `update_contact` | Update contact | Free |
| `view_contact` | View contact details | Free |
| `search_accounts` | Search your accounts | Free |
| `create_account` | Add new account | 1 credit |
| `update_account` | Update account | Free |
| `view_account` | View account details | Free |
| `organization_job_postings` | Get job postings | Free |
| `get_person_email` | Reveal email | 1 credit |
| `employees_of_company` | Find employees | Free* |

*Note: Uses search credits if enriching results

## Apollo.io Terminology

- **Person** - Anyone in Apollo's global database (275M+ people)
- **Contact** - A person you've explicitly saved to your Apollo account
- **Organization** - Any company in Apollo's global database (70M+ companies)
- **Account** - A company you've explicitly saved to your Apollo account

## Development

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Watch mode (auto-rebuild on changes)
npm run dev

# Start the server
npm start
```

## API Documentation

Full Apollo.io API documentation: https://docs.apollo.io/reference/

## Troubleshooting

### "APOLLO_API_KEY environment variable is required"
- Ensure `.env` file exists with your API key
- Or pass via command line: `node dist/index.js --api-key=your_key`

### "Master API key required for account creation"
- Account creation requires a master API key
- Get one from Apollo.io Settings → API → Generate Master Key

### Rate Limits
- Apollo uses fixed-window rate limiting
- Check your limits: https://docs.apollo.io/reference/rate-limits
- View usage: https://docs.apollo.io/reference/view-api-usage-stats

## License

MIT

## Support

For Apollo.io API issues:
- Documentation: https://docs.apollo.io
- Support: https://app.apollo.io/support

For MCP server issues:
- Check the MCP documentation: https://modelcontextprotocol.io
- Review OpenCode docs: https://opencode.ai/docs/mcp-servers
