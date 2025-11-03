#!/usr/bin/env python3
import asyncio
import json
import logging
from typing import Optional, Dict, Any, List

from fastmcp import FastMCP, Tool, MCPError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("mcp-web-automation-server")

app = FastMCP(name="mcp-web-automation-server", version="0.1.0", description="MCP server for browser automation and web control")

# In-memory tab/session manager (placeholder for real browser backend like Playwright)
class TabManager:
    def __init__(self):
        self.tabs: Dict[str, Dict[str, Any]] = {}
        self.counter = 0

    def new_tab(self, url: Optional[str] = None) -> str:
        self.counter += 1
        tab_id = f"tab-{self.counter}"
        self.tabs[tab_id] = {"url": url or "about:blank", "history": [url or "about:blank"], "data": {}}
        logger.info(f"Created tab {tab_id} -> {self.tabs[tab_id]['url']}")
        return tab_id

    def close_tab(self, tab_id: str) -> None:
        if tab_id in self.tabs:
            del self.tabs[tab_id]
            logger.info(f"Closed tab {tab_id}")
        else:
            raise MCPError(f"Unknown tab: {tab_id}")

    def list_tabs(self) -> List[str]:
        return list(self.tabs.keys())

    def get(self, tab_id: str) -> Dict[str, Any]:
        if tab_id not in self.tabs:
            raise MCPError(f"Unknown tab: {tab_id}")
        return self.tabs[tab_id]

TAB_MANAGER = TabManager()

@app.tool(
    name="navigate_page",
    description="Navigate to a URL in a given tab, or create a new tab if not provided",
)
async def navigate_page(url: str, tab_id: Optional[str] = None) -> Dict[str, Any]:
    if not url.startswith("http"):
        raise MCPError("URL must start with http or https")
    if not tab_id:
        tab_id = TAB_MANAGER.new_tab()
    tab = TAB_MANAGER.get(tab_id)
    tab["url"] = url
    tab["history"].append(url)
    logger.info(f"[{tab_id}] Navigated to {url}")
    # Placeholder for real navigation using Playwright
    return {"tab_id": tab_id, "url": url}

@app.tool(name="fill_form", description="Fill input fields on a page")
async def fill_form(selectors_to_values: Dict[str, str], tab_id: str) -> Dict[str, Any]:
    tab = TAB_MANAGER.get(tab_id)
    # Placeholder: store form data
    tab["data"].setdefault("forms", []).append(selectors_to_values)
    logger.info(f"[{tab_id}] Filled form fields: {list(selectors_to_values.keys())}")
    return {"status": "filled", "count": len(selectors_to_values)}

@app.tool(name="click_element", description="Click an element on the page by selector")
async def click_element(selector: str, tab_id: str) -> Dict[str, Any]:
    _ = TAB_MANAGER.get(tab_id)
    logger.info(f"[{tab_id}] Clicked element: {selector}")
    return {"status": "clicked", "selector": selector}

@app.tool(name="extract_data", description="Extract data using CSS selectors")
async def extract_data(selectors: List[str], tab_id: str) -> Dict[str, Any]:
    _ = TAB_MANAGER.get(tab_id)
    # Placeholder: return empty strings for selectors
    data = {sel: "" for sel in selectors}
    logger.info(f"[{tab_id}] Extracted data for {len(selectors)} selectors")
    return {"data": data}

@app.tool(name="capture_screenshot", description="Capture a screenshot of the current page")
async def capture_screenshot(tab_id: str, full_page: bool = True) -> Dict[str, Any]:
    _ = TAB_MANAGER.get(tab_id)
    # Placeholder: return fake path
    path = f"screenshots/{tab_id}.png"
    logger.info(f"[{tab_id}] Captured screenshot -> {path}")
    return {"path": path, "full_page": full_page}

@app.tool(name="generate_pdf", description="Generate a PDF of the current page")
async def generate_pdf(tab_id: str, landscape: bool = False) -> Dict[str, Any]:
    _ = TAB_MANAGER.get(tab_id)
    path = f"pdf/{tab_id}.pdf"
    logger.info(f"[{tab_id}] Generated PDF -> {path}")
    return {"path": path, "landscape": landscape}

@app.tool(name="new_tab", description="Open a new browser tab, optionally to a URL")
async def new_tab(url: Optional[str] = None) -> Dict[str, Any]:
    tab_id = TAB_MANAGER.new_tab(url)
    return {"tab_id": tab_id, "url": TAB_MANAGER.get(tab_id)["url"]}

@app.tool(name="close_tab", description="Close an existing tab")
async def close_tab(tab_id: str) -> Dict[str, Any]:
    TAB_MANAGER.close_tab(tab_id)
    return {"status": "closed", "tab_id": tab_id}

@app.tool(name="list_tabs", description="List open tabs")
async def list_tabs() -> Dict[str, Any]:
    return {"tabs": TAB_MANAGER.list_tabs()}

@app.tool(name="go_back", description="Navigate back in current tab history if possible")
async def go_back(tab_id: str) -> Dict[str, Any]:
    tab = TAB_MANAGER.get(tab_id)
    if len(tab["history"]) < 2:
        raise MCPError("No history to go back to")
    tab["history"].pop()  # current
    tab["url"] = tab["history"][-1]
    logger.info(f"[{tab_id}] Went back to {tab['url']}")
    return {"tab_id": tab_id, "url": tab["url"]}

@app.tool(name="run_workflow", description="Run a multi-step workflow with error handling")
async def run_workflow(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = []
    for idx, step in enumerate(steps, start=1):
        try:
            tool = step.get("tool")
            params = step.get("params", {})
            if not tool:
                raise MCPError("Step missing 'tool'")
            result = await app.run_tool(tool, **params)
            results.append({"step": idx, "tool": tool, "result": result})
        except Exception as e:
            logger.exception("Workflow step failed")
            results.append({"step": idx, "error": str(e)})
            break
    return {"results": results}

if __name__ == "__main__":
    # Run MCP server
    app.run()
