import hashlib
import re
from bs4 import BeautifulSoup

def normalize_text(html_text: str) -> str:
    """
    Normalize HTML/text for fingerprinting:
    - remove scripts/styles
    - extract visible text
    - strip whitespace, collapse spaces, lowercase
    """
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "lxml")
    # Remove script and style tags
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    text = soup.get_text(separator=" ", strip=True)
    # Collapse whitespace and lowercase
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def fingerprint_text(text: str) -> str:
    """
    Return SHA-256 fingerprint for normalized text
    """
    if text is None:
        text = ""
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    return h.hexdigest()
