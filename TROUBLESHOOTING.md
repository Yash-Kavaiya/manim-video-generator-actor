# Troubleshooting Guide - Manim MCP Server Actor

## Build Issues Fixed ✅

### Issue 1: Dockerfile CMD Syntax Error
**Problem:** The shell-style CMD wasn't working properly in all environments.

**Fix Applied:**
```dockerfile
# OLD (might not work):
CMD if [ "$APIFY_META_ORIGIN" = "STANDBY" ]; then \
        python -u -m src; \
    else \
        python -u main.py; \
    fi

# NEW (fixed):
CMD ["/bin/sh", "-c", "if [ \"$APIFY_META_ORIGIN\" = \"STANDBY\" ]; then python -u -m src; else python -u main.py; fi"]
```

### Issue 2: Actor.is_at_home() Called Outside Async Context
**Problem:** Calling `Actor.is_at_home()` before entering the async context caused initialization issues.

**Fix Applied:**
```python
# OLD:
PORT = (Actor.is_at_home() and int(os.environ.get('ACTOR_STANDBY_PORT') or '5001')) or 5001

# NEW:
PORT = int(os.environ.get('ACTOR_STANDBY_PORT', '5001'))
```

### Issue 3: Missing MCP Configuration in actor.json
**Problem:** The actor.json didn't declare MCP support or pay-per-event configuration.

**Fix Applied:**
```json
{
  ...
  "supportedMcpTransports": ["streamableHttp"],
  "payPerEvent": "./.actor/pay_per_event.json"
}
```

## Common Build Problems

### 1. File Path Errors in actor.json

**Symptoms:**
- `ERROR: File ".actor/.actor/INPUT_SCHEMA.json" does not exist!`
- `ERROR: File ".actor/.actor/pay_per_event.json" does not exist!`
- Actor fails during initialization with file not found errors

**Problem:**
Paths in `actor.json` are relative to the `.actor/` directory, but were incorrectly prefixed with `./.actor/`.

**Solution:**
```json
// WRONG - creates duplicate path .actor/.actor/
{
  "input": "./.actor/INPUT_SCHEMA.json",
  "payPerEvent": "./.actor/pay_per_event.json"
}

// CORRECT - paths relative to actor.json location
{
  "input": "./INPUT_SCHEMA.json",
  "payPerEvent": "./pay_per_event.json"
}
```

**Fixed in commit b50169f**

### 2. Dependencies Not Installing

**Symptoms:**
- Build fails during `pip install`
- ModuleNotFoundError during runtime

**Solution:**
```bash
# Check requirements.txt syntax
python validate_build.py

# Make sure all dependencies are listed:
# - mcp>=1.0.0
# - uvicorn>=0.27.0
# - starlette>=0.36.0
# - httpx>=0.26.0
# - pydantic>=2.0.0
# - apify>=1.6.0
# - manim>=0.18.0
```

### 3. Module Import Errors

**Symptoms:**
- "No module named 'src'"
- Import errors during startup

**Solution:**
Ensure the module structure is correct:
```
src/
├── __init__.py          # Must exist!
├── __main__.py          # Entry point
├── const.py
├── models.py
├── event_store.py
├── mcp_gateway.py
└── server.py
```

### 4. JSON Parsing Errors

**Symptoms:**
- "Unexpected token 'C', 'Create a manin video' is not valid JSON"

**Problem:** Trying to send plain text to the MCP server instead of JSON.

**Solution:** Use proper JSON-RPC format:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_video",
    "arguments": {
      "sceneType": "MathLesson",
      "videoQuality": "medium",
      "actorStyle": "cartoon",
      "actorColorScheme": "blue"
    }
  }
}
```

### 5. Actor Won't Start in STANDBY Mode

**Symptoms:**
- Actor exits immediately with "Not designed to run in NORMAL mode"
- MCP server doesn't respond

**Solution:**
Ensure environment variables are set correctly:
```bash
APIFY_META_ORIGIN=STANDBY
ACTOR_STANDBY_PORT=5001
ACTOR_STANDBY_URL=https://your-actor-url
```

### 6. Port Binding Issues

**Symptoms:**
- "Address already in use"
- "Permission denied" on port 5001

**Solution:**
The port is configured via environment variable:
```bash
# Change port if needed
export ACTOR_STANDBY_PORT=8080
```

### 7. Session Timeout Too Short

**Symptoms:**
- Connections drop frequently
- "Session expired" errors

**Solution:**
Adjust timeout in environment:
```bash
# Default is 300 seconds (5 minutes)
export SESSION_TIMEOUT_SECS=600  # 10 minutes
```

## Validation Before Deployment

Always run the validation script before deploying:

```bash
python validate_build.py
```

This checks:
- ✅ Python syntax in all files
- ✅ JSON validity in configuration files
- ✅ Module structure
- ✅ Requirements file format
- ✅ Dockerfile existence

## Testing Locally

### Test Regular Actor Mode
```bash
python main.py
```

### Test MCP Server Mode
```bash
export APIFY_META_ORIGIN=STANDBY
export ACTOR_STANDBY_PORT=5001
python -m src
```

Then visit: `http://localhost:5001/` in your browser to see the HTML interface.

## Testing MCP Tools

### Using curl

```bash
# Initialize session
curl -X POST http://localhost:5001/mcp/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "test-client",
        "version": "1.0.0"
      }
    }
  }'

# List tools
curl -X POST http://localhost:5001/mcp/ \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
  }'

# Call generate_video tool
curl -X POST http://localhost:5001/mcp/ \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: YOUR_SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "generate_video",
      "arguments": {
        "sceneType": "MathLesson",
        "videoQuality": "medium",
        "actorStyle": "cartoon",
        "actorColorScheme": "blue"
      }
    }
  }'
```

### Using Python Client

```python
import httpx
import json

async def test_mcp_server():
    async with httpx.AsyncClient() as client:
        # Initialize
        response = await client.post(
            "http://localhost:5001/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0"}
                }
            }
        )
        session_id = response.headers.get("mcp-session-id")

        # List tools
        response = await client.post(
            "http://localhost:5001/mcp/",
            headers={"mcp-session-id": session_id},
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
        )
        print(json.dumps(response.json(), indent=2))

# Run test
import asyncio
asyncio.run(test_mcp_server())
```

## Deployment Checklist

Before deploying to Apify:

- [ ] Run `python validate_build.py` - all checks pass
- [ ] Test locally in regular mode: `python main.py`
- [ ] Test locally in MCP mode: `APIFY_META_ORIGIN=STANDBY python -m src`
- [ ] Verify all JSON files are valid
- [ ] Check pay_per_event.json pricing is correct
- [ ] Review actor.json configuration
- [ ] Commit all changes
- [ ] Push to repository

## Getting Help

If issues persist:

1. **Check Logs:** Look at Actor logs in Apify Console
2. **Validate Files:** Run `python validate_build.py`
3. **Test Components:** Test each module individually
4. **Review Changes:** Check git diff for unexpected modifications
5. **Consult Docs:**
   - [Apify Actors](https://docs.apify.com/platform/actors)
   - [MCP Specification](https://spec.modelcontextprotocol.io/)
   - [Streamable HTTP Transport](https://spec.modelcontextprotocol.io/specification/basic/transports/#http-with-sse)

## Known Working Configuration

The following configuration is known to work:

```json
// .actor/actor.json
{
  "actorSpecification": 1,
  "supportedMcpTransports": ["streamableHttp"],
  "payPerEvent": "./.actor/pay_per_event.json"
}
```

```dockerfile
# Dockerfile
CMD ["/bin/sh", "-c", "if [ \"$APIFY_META_ORIGIN\" = \"STANDBY\" ]; then python -u -m src; else python -u main.py; fi"]
```

```python
# src/__main__.py
HOST = '0.0.0.0'
PORT = int(os.environ.get('ACTOR_STANDBY_PORT', '5001'))
```

## Success Indicators

Your Actor is working correctly when:

✅ Build completes without errors
✅ `python validate_build.py` passes all checks
✅ Regular mode runs: `python main.py` works
✅ MCP mode starts: Browser shows HTML interface at `/`
✅ Health check responds: `/` returns JSON status
✅ Tools are listed: `tools/list` returns 4 tools
✅ Tool calls work: `tools/call` executes successfully
✅ Sessions timeout: Inactive sessions clean up after 5 min
✅ Charging works: Events are logged in Apify Console

---

**Status:** All known issues have been fixed and validated ✅
**Last Updated:** 2025-11-09
