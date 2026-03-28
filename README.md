# mcp-pdf-recolor
Save some ink. Recolor PDFs so that you can use every bit of that pesky color ink cartridge that seems to never run out but your black one always does.


# Installation

```sh
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Then add the MCP entry to `mcp.json`. Replace `/path/to/mcp-pdf-recolor` with your path to the repo.

```json
{
    "mcpServers": {
        "pdf-recolor": {
            "command": "/path/to/mcp-pdf-recolor/.venv/bin/python",
            "args": [
                "/path/to/mcp-pdf-recolor/mcp_server.py"
            ]
        }
    }
}
```


Test:

```
Recolor the PDF: /path/to/pdf_file.pdf to have dark navy blue text.
```
