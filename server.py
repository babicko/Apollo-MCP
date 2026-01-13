#!/usr/bin/env python3
"""
Apollo.io MCP Server for OpenCode
Provides prospect enrichment and search capabilities
"""

import asyncio
import json
import os
import sys
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Apollo API Configuration
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY", "")
APOLLO_BASE_URL = "https://api.apollo.io/v1"

app = Server("apollo-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Apollo tools"""
    return [
        Tool(
            name="apollo_enrich_person",
            description="Enrich a person's data using Apollo.io. Finds job title, seniority, company info, and contact details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_name": {
                        "type": "string",
                        "description": "Person's first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Person's last name"
                    },
                    "company_name": {
                        "type": "string",
                        "description": "Company name where person works"
                    },
                    "domain": {
                        "type": "string",
                        "description": "Company domain (optional)"
                    }
                },
                "required": ["first_name", "last_name", "company_name"]
            }
        ),
        Tool(
            name="apollo_enrich_organization",
            description="Enrich an organization's data using Apollo.io. Gets company size, industry, funding, tech stack.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Company domain (e.g., plauti.com)"
                    },
                    "company_name": {
                        "type": "string",
                        "description": "Company name (if domain not available)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="apollo_search_people",
            description="Search for people/prospects in Apollo's database using filters like job title, location, company size.",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_titles": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Job titles to search for (e.g., ['VP Sales', 'Director Marketing'])"
                    },
                    "person_locations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Locations (e.g., ['Netherlands', 'Belgium'])"
                    },
                    "organization_num_employees_ranges": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Company size ranges (e.g., ['11-50', '51-200'])"
                    },
                    "q_keywords": {
                        "type": "string",
                        "description": "Keywords to search for"
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="apollo_get_contact_info",
            description="Reveal contact information (email/phone) for a person. Uses Apollo credits.",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "Apollo person ID (from search or enrich results)"
                    }
                },
                "required": ["person_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if not APOLLO_API_KEY:
        return [TextContent(
            type="text",
            text="Error: APOLLO_API_KEY environment variable not set"
        )]
    
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            
            if name == "apollo_enrich_person":
                url = f"{APOLLO_BASE_URL}/people/match"
                data = {
                    "first_name": arguments.get("first_name"),
                    "last_name": arguments.get("last_name"),
                    "organization_name": arguments.get("company_name")
                }
                if arguments.get("domain"):
                    data["domain"] = arguments["domain"]
                
                response = await client.post(url, headers=headers, json=data)
                result = response.json()
                
                if response.status_code == 200 and result.get("person"):
                    person = result["person"]
                    org = person.get("organization", {})
                    
                    formatted = {
                        "name": person.get("name"),
                        "title": person.get("title"),
                        "seniority": person.get("seniority"),
                        "departments": person.get("departments", []),
                        "email": person.get("email"),
                        "linkedin_url": person.get("linkedin_url"),
                        "company": {
                            "name": org.get("name"),
                            "domain": org.get("website_url"),
                            "industry": org.get("industry"),
                            "size": org.get("estimated_num_employees"),
                            "founded_year": org.get("founded_year")
                        }
                    }
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(formatted, indent=2)
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Person not found or error: {result.get('message', 'Unknown error')}"
                    )]
            
            elif name == "apollo_enrich_organization":
                url = f"{APOLLO_BASE_URL}/organizations/enrich"
                data = {}
                if arguments.get("domain"):
                    data["domain"] = arguments["domain"]
                elif arguments.get("company_name"):
                    data["name"] = arguments["company_name"]
                
                response = await client.post(url, headers=headers, json=data)
                result = response.json()
                
                if response.status_code == 200 and result.get("organization"):
                    org = result["organization"]
                    
                    formatted = {
                        "name": org.get("name"),
                        "domain": org.get("website_url"),
                        "industry": org.get("industry"),
                        "size": org.get("estimated_num_employees"),
                        "founded_year": org.get("founded_year"),
                        "city": org.get("city"),
                        "country": org.get("country"),
                        "linkedin_url": org.get("linkedin_url"),
                        "technologies": [t.get("name") for t in org.get("current_technologies", [])[:10]],
                        "description": org.get("short_description")
                    }
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(formatted, indent=2)
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Organization not found or error: {result.get('message', 'Unknown error')}"
                    )]
            
            elif name == "apollo_search_people":
                url = f"{APOLLO_BASE_URL}/mixed_people/search"
                data = {
                    "page": arguments.get("page", 1),
                    "per_page": 10
                }
                
                if arguments.get("person_titles"):
                    data["person_titles"] = arguments["person_titles"]
                if arguments.get("person_locations"):
                    data["person_locations"] = arguments["person_locations"]
                if arguments.get("organization_num_employees_ranges"):
                    data["organization_num_employees_ranges"] = arguments["organization_num_employees_ranges"]
                if arguments.get("q_keywords"):
                    data["q_keywords"] = arguments["q_keywords"]
                
                response = await client.post(url, headers=headers, json=data)
                result = response.json()
                
                if response.status_code == 200:
                    people = result.get("people", [])
                    
                    formatted_people = []
                    for person in people[:10]:
                        formatted_people.append({
                            "id": person.get("id"),
                            "name": person.get("name"),
                            "title": person.get("title"),
                            "company": person.get("organization_name"),
                            "location": person.get("city"),
                            "linkedin": person.get("linkedin_url")
                        })
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "total_results": result.get("total_entries", 0),
                            "page": result.get("page", 1),
                            "people": formatted_people
                        }, indent=2)
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Search error: {result.get('message', 'Unknown error')}"
                    )]
            
            elif name == "apollo_get_contact_info":
                url = f"{APOLLO_BASE_URL}/people/{arguments['person_id']}"
                
                response = await client.get(url, headers=headers)
                result = response.json()
                
                if response.status_code == 200 and result.get("person"):
                    person = result["person"]
                    
                    formatted = {
                        "name": person.get("name"),
                        "email": person.get("email"),
                        "phone_numbers": person.get("phone_numbers", []),
                        "linkedin_url": person.get("linkedin_url"),
                        "title": person.get("title"),
                        "company": person.get("organization_name")
                    }
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(formatted, indent=2)
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Could not retrieve contact info: {result.get('message', 'Unknown error')}"
                    )]
            
            else:
                return [TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
                
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error calling Apollo API: {str(e)}"
        )]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
