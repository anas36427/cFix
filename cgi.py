# Temporary patch for deprecated cgi module (Python 3.13+)
import html
import urllib.parse

def escape(s, quote=True):
    """Replacement for cgi.escape() using html.escape()."""
    return html.escape(s, quote=quote)

def parse_qs(qs, keep_blank_values=False, strict_parsing=False):
    """Replacement for cgi.parse_qs() using urllib.parse.parse_qs()."""
    return urllib.parse.parse_qs(qs, keep_blank_values, strict_parsing)

def parse_header(line):
    """Minimal replacement for cgi.parse_header()."""
    parts = line.split(';')
    key = parts[0].strip().lower()
    pdict = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1)
            pdict[k.strip().lower()] = v.strip()
    return key, pdict
