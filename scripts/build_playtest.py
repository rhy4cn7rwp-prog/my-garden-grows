"""Build a self-contained Mac-friendly HTML playtest, with no external dependencies."""
from pathlib import Path
import base64
import re
root = Path(__file__).resolve().parents[1]
source = root / 'development'
html = (source / 'index.html').read_text()
html = re.sub(r'<link\s+rel="stylesheet"\s+href="src/styles.css"\s*/?>',
              lambda _: '<style>' + (source / 'src/styles.css').read_text() + '</style>', html)
def script(match):
    js = (source / match[1]).read_text()
    js = re.sub(r'assets/scene-\d+\.webp', lambda m: 'data:image/webp;base64,' +
                base64.b64encode((source / m[0]).read_bytes()).decode(), js)
    return '<script>' + js.replace('</script', '<\\/script') + '</script>'
html = re.sub(r'<script src="([^"]+)"></script>', script, html)
output = root / 'playtest' / 'My-Garden-Grows-1.0.html'
output.write_text(html)
print(f'Built {output.relative_to(root)} ({output.stat().st_size:,} bytes)')
