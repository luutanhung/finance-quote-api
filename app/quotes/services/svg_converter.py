from html import escape
import base64

import requests

from app.quotes.types import Theme
from app.quotes.schemas import Quote


class SVGConverter:
    """
    Convert a Quote -> SVG string.
    - Pure SVG (no foreignObject) using <text> & <tspan>.
    - Avatar is referenced by URL with <image href="..."> (not embedded).
    """

    def __init__(self, width: int = 600, height: int = 300, theme: Theme = Theme.light):
        self.width = width
        self.height = height
        self.theme = theme
        # conservative chars-per-line baseline (scaled later)
        self.base_cpl = 28

    def _escape(self, s: str) -> str:
        return escape(s, quote=True)

    def _wrap_text(self, text: str, max_width: int, font_size: int = 16) -> list[str]:
        words = text.split()
        lines, current_line = [], []

        for word in words:
            test_line = " ".join(current_line + [word])
            est_width = len(test_line) * font_size * 0.6
            if est_width <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def convert_to_svg(
        self,
        quote: Quote,
        *,
        padding: int = 40,
        avatar_size: int = 72,
    ) -> str:
        text = self._escape(quote.quote.strip())
        author = self._escape(quote.author.strip()) if quote.author else ""

        # pick a base font size by heuristic
        font_size = int(self.width * 0.025)

        # available width for text (account for avatar + paddings)
        x_text = padding + (avatar_size + 20 if quote.author_avatar_url else 0)
        available_width = self.width - padding - x_text

        # compute chars-per-line based on width + font size
        cpl = int(self.base_cpl * (available_width / self.width) * (44 / font_size))
        max_text_width = self.width - x_text - padding
        lines = self._wrap_text(text, max_text_width, font_size)

        # total block height
        text_block_height = len(lines) * (font_size * 1.3)

        # 🔹 auto-shrink font size if block too tall
        while text_block_height > self.height - 2 * padding and font_size > 14:
            font_size -= 2
            cpl = int(self.base_cpl * (available_width / self.width) * (44 / font_size))
            lines = self._wrap_text(text, cpl)
            text_block_height = len(lines) * (font_size * 1.3)

        # center vertically (but don’t go above top margin)
        top_y = max(padding, (self.height - text_block_height) // 2)

        # theme colors
        if self.theme == Theme.light:
            bg = "#ffffff"
            fg = "#0f1724"
            accent_from = "#7DD3FC"
            accent_to = "#60A5FA"
            author_fg = "#334155"

        if self.theme == Theme.dark:
            bg = "#0f1724"
            fg = "#e6eef8"
            accent_from = "#6EE7B7"
            accent_to = "#3B82F6"
            author_fg = "#c9d6e8"

        # Build svg lines as <tspan> elements
        x_text = padding + (avatar_size + 20 if quote.author_avatar_url else 0)
        tspan_lines = []
        for idx, line in enumerate(lines):
            dy = 0 if idx == 0 else font_size * 1.3
            tspan_lines.append(f'<tspan x="{x_text}" dy="{dy}">{line}</tspan>')

        # author block (aligned right)
        author_svg = ""
        if author:
            author_y = top_y + text_block_height + 24
            author_svg = (
                f'<text x="{self.width - padding}" y="{author_y}" '
                f'font-family="Inter, -apple-system, system-ui, Roboto, Arial" '
                f'font-size="{int(font_size * 0.7)}" fill="{author_fg}" text-anchor="end">'
                f"— {author}"
                f"</text>"
            )

        # avatar svg (optional)
        avatar_svg = ""
        if quote.author_avatar_url:
            resp = requests.get(quote.author_avatar_url, timeout=5)
            if resp.status_code == 200:
                b64_avatar = base64.b64encode(resp.content).decode("utf-8")
                mime_type = resp.headers.get("Content-Type", "image/png")

                avatar_x = padding
                avatar_y = top_y + (text_block_height - avatar_size) // 2
                # href = self._escape(str(quote.author_avatar_url))
                avatar_svg = (
                    f"<defs>"
                    f'  <clipPath id="avatar_clip_{quote.id}">'
                    f'    <circle cx="{avatar_x + avatar_size / 2}" cy="{avatar_y + avatar_size / 2}" r="{avatar_size / 2}" />'
                    f"  </clipPath>"
                    f"</defs>"
                    f'<image href="data:{mime_type};base64,{b64_avatar}" x="{avatar_x}" y="{avatar_y}" width="{avatar_size}" height="{avatar_size}" '
                    f'clip-path="url(#avatar_clip_{quote.id})" preserveAspectRatio="xMidYMid slice" />'
                )

        # assemble SVG
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}"
     viewBox="0 0 {self.width} {self.height}" role="img"
     aria-label="{self._escape(quote.quote)} — {self._escape(quote.author or "")}">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="{accent_from}"/>
      <stop offset="100%" stop-color="{accent_to}"/>
    </linearGradient>

    <filter id="f" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="18" flood-color="#000" flood-opacity="0.12"/>
    </filter>
  </defs>

  <!-- background -->
  <rect width="100%" height="100%" fill="{bg}" />

  <!-- gradient card -->
  <rect x="{padding / 2}" y="{padding / 2}" rx="24" ry="24"
        width="{self.width - padding}" height="{self.height - padding}"
        fill="url(#g)" opacity="0.08" filter="url(#f)" />

  <!-- main content -->
  <g>
    {avatar_svg}
    <text x="{x_text}" y="{top_y + int(font_size)}"
          font-family="Inter, -apple-system, system-ui, Roboto, Arial"
          font-size="{font_size}" fill="{fg}" font-weight="600">
      {"".join(tspan_lines)}
    </text>
    {author_svg}
  </g>
</svg>
'''
        return svg
