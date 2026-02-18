import re

def extract_csrf(html: bytes) -> str:
    m = re.search(rb'name="csrf_token" type="hidden" value="([^"]+)"', html)
    if not m:
        raise AssertionError("CSRF token not found in form HTML")
    return m.group(1).decode("utf-8")

def extract_csrf_anywhere(html: bytes) -> str:
    patterns = [
        rb'name="csrf_token"[^>]*value="([^"]+)"',
        rb'value="([^"]+)"[^>]*name="csrf_token"',
    ]
    for p in patterns:
        m = re.search(p, html)
        if m:
            return m.group(1).decode("utf-8")
    raise AssertionError("CSRF token not found")