"""Streamlit entry point for the V. P. Jha mathematics website.

The site was designed as a static HTML/CSS/JavaScript project. This wrapper
embeds those pages in Streamlit, inlines the local assets, and rewrites local
links so navigation continues to work after deployment.
"""

from __future__ import annotations

import json
import posixpath
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit

import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).resolve().parent

PAGES = {
    "home": "index.html",
    "index": "index.html",
    "books": "books.html",
    "blog": "blog.html",
    "about": "about.html",
    "posts/borel-sigma-algebra": "posts/borel-sigma-algebra.html",
    "posts/outer-measure": "posts/outer-measure.html",
    "posts/pdf-vs-cdf": "posts/pdf-vs-cdf.html",
    "posts/open-balls": "posts/open-balls.html",
}

HTML_TO_PAGE = {html_file: page for page, html_file in PAGES.items()}
HTML_TO_PAGE["index.html"] = "home"


def query_value(name: str, default: str = "") -> str:
    """Return one query-string value across supported Streamlit versions."""
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return str(value[0]) if value else default
    return str(value)


def add_target(tag: str, target: str) -> str:
    """Add or replace the target attribute on an anchor start tag."""
    if re.search(r"\btarget\s*=", tag, flags=re.IGNORECASE):
        return re.sub(
            r"\btarget\s*=\s*(['\"]).*?\1",
            f'target="{target}"',
            tag,
            flags=re.IGNORECASE,
        )
    return tag[:-1] + f' target="{target}">'


def rewrite_anchor(tag: str, current_html: str) -> str:
    """Rewrite one local anchor to a Streamlit query-parameter route."""
    match = re.search(r"\bhref\s*=\s*(['\"])(.*?)\1", tag, flags=re.IGNORECASE)
    if not match:
        return tag

    href = match.group(2).strip()
    lowered = href.lower()

    if not href or href.startswith("#") or lowered.startswith(("mailto:", "tel:", "javascript:")):
        return tag

    if lowered.startswith(("http://", "https://", "//")):
        return add_target(tag, "_blank")

    parsed = urlsplit(href)
    current_dir = posixpath.dirname(current_html)
    resolved = posixpath.normpath(posixpath.join(current_dir, parsed.path))

    # RSS remains available from the canonical GitHub Pages address.
    if resolved == "feed.xml":
        replacement = "https://vp-jha.github.io/Website_book/feed.xml"
        tag = tag[: match.start(2)] + replacement + tag[match.end(2) :]
        return add_target(tag, "_blank")

    page = HTML_TO_PAGE.get(resolved)
    if page is None:
        return tag

    params = [("page", page)]
    params.extend(parse_qsl(parsed.query, keep_blank_values=True))
    replacement = "/?" + urlencode(params)
    if parsed.fragment:
        replacement += "#" + parsed.fragment

    tag = tag[: match.start(2)] + replacement + tag[match.end(2) :]
    return add_target(tag, "_top")


def prepare_page(html_file: str, topic: str) -> str:
    """Load a static page and make it self-contained for the Streamlit iframe."""
    html_path = APP_DIR / html_file
    html_text = html_path.read_text(encoding="utf-8")
    css_text = (APP_DIR / "styles.css").read_text(encoding="utf-8")
    js_text = (APP_DIR / "script.js").read_text(encoding="utf-8")
    page_json = json.dumps(html_file).replace("<", "\\u003c").replace(">", "\\u003e")
    topic_json = json.dumps(topic).replace("<", "\\u003c").replace(">", "\\u003e")

    # The iframe URL is Streamlit-generated, so use the actual selected page to
    # identify the home page and use Streamlit's topic parameter for filtering.
    js_text = js_text.replace(
        "document.body.classList.toggle('home',location.pathname.endsWith('/')||location.pathname.endsWith('index.html'));",
        "document.body.classList.toggle('home',window.__VPJ_PAGE__==='index.html');",
    )
    js_text = js_text.replace(
        "new URLSearchParams(location.search).get('topic')",
        "new URLSearchParams(location.search).get('topic')||window.__VPJ_TOPIC__",
    )

    # Replace the two local asset tags. Google Fonts and canonical metadata stay
    # intact and continue to load normally.
    html_text = re.sub(
        r'<link\s+rel=["\']stylesheet["\']\s+href=["\'](?:\.\./)?styles\.css["\']\s*/?>',
        f"<style>{css_text}</style>",
        html_text,
        count=1,
        flags=re.IGNORECASE,
    )
    html_text = re.sub(
        r'<script\s+src=["\'](?:\.\./)?script\.js["\']\s+defer></script>',
        (
            "<script>"
            f"window.__VPJ_PAGE__={page_json};"
            f"window.__VPJ_TOPIC__={topic_json};"
            f"{js_text}"
            "</script>"
        ),
        html_text,
        count=1,
        flags=re.IGNORECASE,
    )

    html_text = re.sub(
        r"<a\b[^>]*>",
        lambda match: rewrite_anchor(match.group(0), html_file),
        html_text,
        flags=re.IGNORECASE,
    )

    # Match the component to the browser viewport. The website scrolls inside
    # the component, preserving its fixed header and reading-progress behaviour.
    frame_script = """
<script>
(() => {
  const setFrameHeight = () => {
    let height = 900;
    try {
      height = Math.max(600, Math.min(1200, window.parent.innerHeight));
    } catch (_) {}
    window.parent.postMessage({
      isStreamlitMessage: true,
      type: "streamlit:setFrameHeight",
      height
    }, "*");
  };
  setFrameHeight();
  window.addEventListener("resize", setFrameHeight, {passive: true});
})();
</script>
"""
    return html_text.replace("</body>", frame_script + "</body>", 1)


st.set_page_config(
    page_title="Dr. V. P. Jha — Mathematics, Books & Notes",
    page_icon="∫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove Streamlit's application chrome so the original website fills the page.
st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        margin: 0 !important;
        padding: 0 !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      footer { display: none !important; }
      .stMainBlockContainer, .block-container {
        width: 100% !important;
        max-width: none !important;
        padding: 0 !important;
      }
      [data-testid="stVerticalBlock"] { gap: 0 !important; }
      iframe[title="streamlit.components.v1.html"] {
        display: block;
        width: 100%;
        border: 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

requested_page = query_value("page", "home").strip("/") or "home"
html_file = PAGES.get(requested_page, "404.html")
topic = query_value("topic", "")

components.html(
    prepare_page(html_file, topic),
    height=900,
    scrolling=True,
)
