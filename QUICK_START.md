# 🎯 Apollo MCP Server - Quick Command Reference

## ✅ SETUP COMPLETE!

The Apollo MCP server has been added to OpenCode!

**Config Location:** `~/.config/opencode/opencode.json`

---

## 🚀 How to Use (Just Restart OpenCode!)

### After Restarting OpenCode, Try These:

```
"Use apollo to enrich plauti.com - give me company size, tech stack, and department breakdown"
```

```
"Search for engineers at stripe.com using apollo"
```

```
"Find employees of Microsoft with apollo"
```

```
"Create a contact in apollo for John Doe at example.com"
```

---

## 🧪 Test Commands

### Test the API directly (without OpenCode):
```bash
cd ~/apollo-mcp-server
node dist/test.js
```

### Rebuild after making changes:
```bash
cd ~/apollo-mcp-server
npm run build
```

### View your OpenCode config:
```bash
cat ~/.config/opencode/opencode.json
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `~/.config/opencode/opencode.json` | OpenCode configuration (MCP server registered here) |
| `~/apollo-mcp-server/dist/index.js` | MCP server executable |
| `~/apollo-mcp-server/.env` | Your API keys (secure) |
| `~/apollo-mcp-server/README.md` | Full documentation |
| `~/apollo-mcp-server/OPENCODE_SETUP.md` | Setup guide |

---

## 🔧 Troubleshooting

### If Apollo doesn't work in OpenCode:

1. **Verify config exists:**
   ```bash
   cat ~/.config/opencode/opencode.json
   ```

2. **Test API directly:**
   ```bash
   cd ~/apollo-mcp-server && node dist/test.js
   ```

3. **Check server is built:**
   ```bash
   ls -la ~/apollo-mcp-server/dist/index.js
   ```

4. **Restart OpenCode**

---

## 🎯 15 Available Tools

**Enrichment:** `organization_enrichment`, `people_enrichment`

**Search:** `people_search`, `organization_search`

**Contacts:** `search_contacts`, `create_contact`, `update_contact`, `view_contact`, `get_person_email`

**Accounts:** `search_accounts`, `create_account`, `update_account`, `view_account`

**Other:** `organization_job_postings`, `employees_of_company`

---

## ✨ You're All Set!

Just restart OpenCode and start using Apollo with natural language!

**Quick Test:** "Use apollo to enrich plauti.com"

**Expected Result:** Company size (58), department breakdown, tech stack ✅
