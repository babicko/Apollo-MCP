#!/bin/bash

# ============================================
# Add Apollo MCP Server to OpenCode
# ============================================

echo "🚀 Setting up Apollo MCP Server for OpenCode"
echo ""

# Step 1: Create OpenCode config directory if it doesn't exist
echo "Step 1: Creating OpenCode config directory..."
mkdir -p ~/.config/opencode
echo "✅ Directory created/verified: ~/.config/opencode"
echo ""

# Step 2: Check if opencode.json exists
if [ -f ~/.config/opencode/opencode.json ]; then
    echo "⚠️  opencode.json already exists!"
    echo "   Location: ~/.config/opencode/opencode.json"
    echo ""
    echo "   Please manually add this to your existing config:"
    echo ""
    cat << 'CONFIGJSON'
{
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
CONFIGJSON
    echo ""
else
    # Step 3: Create new opencode.json with Apollo MCP server
    echo "Step 2: Creating opencode.json with Apollo MCP server..."
    cat > ~/.config/opencode/opencode.json << 'CONFIGJSON'
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
CONFIGJSON
    echo "✅ Created: ~/.config/opencode/opencode.json"
    echo ""
fi

# Step 4: Verify the Apollo MCP server is built
echo "Step 3: Verifying Apollo MCP server..."
if [ -f ~/apollo-mcp-server/dist/index.js ]; then
    echo "✅ Apollo MCP server found and ready"
    echo "   Location: ~/apollo-mcp-server/dist/index.js"
else
    echo "❌ Apollo MCP server not found!"
    echo "   Run: cd ~/apollo-mcp-server && npm run build"
    exit 1
fi
echo ""

# Step 5: Display config
echo "Step 4: Current OpenCode config:"
echo "─────────────────────────────────────────────────"
cat ~/.config/opencode/opencode.json
echo "─────────────────────────────────────────────────"
echo ""

# Step 6: Final instructions
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Restart OpenCode"
echo "   2. Test with: 'Use apollo to enrich plauti.com'"
echo ""
echo "🧪 Test Apollo API directly:"
echo "   cd ~/apollo-mcp-server && node dist/test.js"
echo ""
echo "📚 Documentation:"
echo "   - Full guide: ~/apollo-mcp-server/README.md"
echo "   - OpenCode setup: ~/apollo-mcp-server/OPENCODE_SETUP.md"
echo ""
