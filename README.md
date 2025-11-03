# mcp-web-automation-server

A comprehensive MCP-based automation system for web control using FastMCP. It provides tools for navigation, form filling, clicks/interactions, data extraction, screenshots, PDF generation, and multi-tab management. Includes configuration presets for social media automation, e-commerce flows, form submissions, data scraping workflows, and report generation.

## Features
- FastMCP-based Python MCP server
- Browser control abstractions (pluggable backend; placeholder in-memory with TabManager)
- Tools: navigate_page, fill_form, click_element, extract_data, capture_screenshot, generate_pdf, new_tab, close_tab, list_tabs, go_back, run_workflow
- Robust logging and structured error handling
- Multi-step workflow runner with intermediate results

## Project structure
```
.
├── server.py
├── configs/
│   ├── social_media.yaml
│   ├── ecommerce.yaml
│   ├── form_submission.yaml
│   ├── scraping.yaml
│   └── reporting.yaml
├── examples/
│   └── sample_workflows.md
├── requirements.txt
├── claude_desktop_config.json
└── README.md
```

## Quick start
1. Python 3.10+
2. Create and activate venv
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows (PowerShell): `py -3 -m venv .venv; .venv\Scripts\Activate.ps1`
3. Install deps: `pip install -r requirements.txt`
4. Run server: `python server.py`

## Usage via MCP client
- Configure your MCP client (e.g., Claude Desktop) to point to this server script.
- Example tool calls (YAML-ish):
```
- tool: new_tab
  params: {url: https://example.com}
- tool: navigate_page
  params: {url: https://news.ycombinator.com, tab_id: tab-1}
- tool: fill_form
  params: {tab_id: tab-1, selectors_to_values: {input[name=q]: "fastmcp"}}
- tool: click_element
  params: {tab_id: tab-1, selector: "button[type=submit]"}
- tool: extract_data
  params: {tab_id: tab-1, selectors: [".result a.title", ".result .snippet"]}
- tool: capture_screenshot
  params: {tab_id: tab-1, full_page: true}
- tool: generate_pdf
  params: {tab_id: tab-1, landscape: false}
- tool: run_workflow
  params:
    steps:
      - {tool: new_tab, params: {url: https://example.com}}
      - {tool: navigate_page, params: {tab_id: tab-1, url: https://github.com}}
      - {tool: extract_data, params: {tab_id: tab-1, selectors: ["a"]}}
```

## Configuration files
See configs/ directory for task-specific presets to seed workflows.

## Logging
Structured logging prints to stdout. Adjust level via `LOGLEVEL` env or edit `logging.basicConfig` in server.py.

## Roadmap
- Swap in Playwright automation backend for real browser control
- Add authentication helpers and cookie jar support
- Add retry/backoff policies and circuit breaker for flaky sites
- Persistent storage for artifacts (screenshots, PDFs, extracted data)

## License
Choose a license (MIT/Apache-2.0) in future commit.
