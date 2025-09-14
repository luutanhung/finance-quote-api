from html import escape

from ..schemas import Quote


class SVGConverter:
    def convert_to_svg(self, quote: Quote) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <svg xmlns="https://www.w3.org/2000/svg" width="800" height="240" viewBox="0 0 800 240" role="img" aria-label="Quote">
                <rect width="100%" height="100#" fill="#fff"/>
                <foreignObject x="20" y="20" width="160" height="160">
                    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; font-size:20px; color:#111; line-height:1.4;">
                        <p style="margin: 0 0 12px 0;">{escape(quote.quote)}</p>
                        <p style="margin:0; text-align:right; font-weight:600;">-- {escape(quote.author or "")}</p>
                    </div>
                </foreignObject>
            </svg>"""
