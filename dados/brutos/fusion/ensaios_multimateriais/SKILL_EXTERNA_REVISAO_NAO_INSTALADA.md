---
name: autodesk-fusion
description: Create and modify Autodesk Fusion designs in real time through the local Fusion Desktop MCP server (fusion_* tools). Use when the user asks to model parts, create sketches, extrude, edit features, or otherwise manipulate a live Fusion session ("create a 10mm cube in Fusion", "modify this design", "add a fillet").
---

# Autodesk Fusion (Desktop MCP)

This skill uses the `fusion_*` tools (provided by the `pi-autodesk-fusion` extension), backed by the Autodesk Fusion MCP server running inside the local Fusion desktop app. Tool calls execute against the user's **live Fusion session** — changes appear in Fusion immediately.

## Connection workflow

1. If `fusion_*` modeling tools are already registered, use them directly.
2. If only `fusion_connect` is available (or calls fail with connection errors), call `fusion_connect` first. It connects to `http://127.0.0.1:27182/mcp` (override via `FUSION_MCP_URL`) and registers the live tool set.
3. If `fusion_connect` fails, tell the user to:
   - start Fusion on this machine (desktop app, not web),
   - enable **Preferences > General > API > "Fusion MCP Server (runs locally on this device)"**,
   - then retry (or run `/fusion reconnect`).

## Working guidelines

- **Tools are dynamic.** The Fusion tool set is discovered at connection time and may change between Fusion versions. After connecting, prefer the most specific tool for the job and follow each tool's own description and schema exactly.
- **Edits are real.** Operations modify the user's open design. For destructive or ambiguous operations (deleting bodies, overwriting features), confirm intent before executing.
- **Work stepwise.** Break modeling requests into small operations (sketch → profile → extrude → modify) and verify intermediate results from tool output before continuing.
- **Verify visually.** After creating or modifying geometry, call `fusion_screenshot` to capture the viewport and confirm the result looks correct — don't rely only on numeric read-backs.
- **Units matter.** State units explicitly in tool arguments when schemas allow (e.g. mm vs inch); don't assume.
- **Errors:** if a tool call reports the connection dropped (e.g. Fusion restarted), call `fusion_connect` again and retry once.

## Status / recovery

- `/fusion` — show endpoint, connection state, registered tools.
- `/fusion reconnect` — force reconnect and re-discover tools.
- Destructive scripts (delete/save/close) trigger a user confirmation dialog by default; if the user declines, do not retry the same operation — ask what they want instead. (`FUSION_CONFIRM=off` disables the gate.)
