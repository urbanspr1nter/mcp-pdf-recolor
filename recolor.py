#!/usr/bin/env python3
"""Replace black ink in a PDF with a dark color (default: very dark navy blue).

Usage: python recolor.py input.pdf [output.pdf] [hex_color]

Examples:
    python recolor.py label.pdf
    python recolor.py label.pdf label_navy.pdf
    python recolor.py label.pdf label_brown.pdf 1a0a00
"""

import sys
import os
import fitz

def recolor(input_path, output_path, hex_color="0a0a2e", dpi=300, threshold=80):
    r_t = int(hex_color[0:2], 16)
    g_t = int(hex_color[2:4], 16)
    b_t = int(hex_color[4:6], 16)

    doc = fitz.open(input_path)
    out = fitz.open()

    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        samples = bytearray(pix.samples)
        bpp = pix.n

        for i in range(0, len(samples), bpp):
            r, g, b = samples[i], samples[i + 1], samples[i + 2]
            if r < threshold and g < threshold and b < threshold:
                d = 1.0 - max(r, g, b) / threshold
                samples[i]     = int(r_t * d + r * (1 - d))
                samples[i + 1] = int(g_t * d + g * (1 - d))
                samples[i + 2] = int(b_t * d + b * (1 - d))

        pix2 = fitz.Pixmap(pix.colorspace, pix.irect, pix.alpha)
        pix2.set_origin(pix.x, pix.y)
        pix2.samples_mv[:] = bytes(samples)

        rect = page.rect
        out_page = out.new_page(width=rect.width, height=rect.height)
        out_page.insert_image(rect, pixmap=pix2)

    doc.close()
    out.save(output_path, garbage=4, deflate=True)
    out.close()
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    input_path = sys.argv[1]
    base, ext = os.path.splitext(input_path)
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"{base}_recolored{ext}"
    hex_color = sys.argv[3] if len(sys.argv) > 3 else "0a0a2e"

    recolor(input_path, output_path, hex_color)
