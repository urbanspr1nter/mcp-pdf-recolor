#!/usr/bin/env python3
"""MCP server exposing the PDF recolor tool."""

import os
from mcp.server.fastmcp import FastMCP
from recolor import recolor

mcp = FastMCP("pdf-recolor")


@mcp.tool()
def recolor_pdf(
    input_path: str,
    output_path: str = "",
    hex_color: str = "0a0a2e",
    dpi: int = 300,
    threshold: int = 80,
) -> str:
    """Replace dark/black ink in a PDF with a target color.

    Args:
        input_path: Path to the input PDF file.
        output_path: Path for the output PDF. Defaults to <input>_recolored.pdf.
        hex_color: Target hex color (6 chars, no #). Default "0a0a2e" (dark navy).
        dpi: Render resolution. Default 300.
        threshold: Darkness threshold (0-255). Pixels with all channels below this are recolored. Default 80.
    """
    input_path = os.path.expanduser(input_path)
    if not os.path.isfile(input_path):
        return f"Error: file not found: {input_path}"

    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_recolored{ext}"
    else:
        output_path = os.path.expanduser(output_path)

    if len(hex_color.lstrip("#")) != 6:
        return "Error: hex_color must be exactly 6 hex characters (e.g. '0a0a2e')"
    hex_color = hex_color.lstrip("#")

    recolor(input_path, output_path, hex_color, dpi, threshold)
    return f"Saved recolored PDF to {output_path}"


if __name__ == "__main__":
    mcp.run()
