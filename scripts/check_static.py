"""Verify built local URLs/assets and reconciliation without publishing anything."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.local = []
        self.robots = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.robots = attrs.get('content') == 'noindex, nofollow'
        for name in ('href', 'src'):
            value = attrs.get(name) or ''
            if value.startswith('/') and not value.startswith('//'):
                self.local.append(value)


def main():
    root = Path('dist')
    data = json.loads(Path('src/data/joomla.json').read_text())
    report = json.loads(Path('docs/import-report.json').read_text())
    rec = report['reconciliation']
    assert rec['source'] == rec['imported'] + rec['excluded'] + rec['errors']
    assert rec['errors'] == 0
    assert len(data['articles']) == report['importedArticles']
    paths = [a['path'] for a in data['articles']]
    assert len(paths) == len(set(paths))
    assert all((root / path.strip('/') / 'index.html').is_file() for path in paths)
    pages = list(root.rglob('*.html'))
    assert len(pages) == len(paths) + 3
    checked = 0
    for page in pages:
        parser = Links()
        parser.feed(page.read_text())
        assert parser.robots, f'Missing noindex: {page}'
        for url in parser.local:
            target = root / unquote(urlsplit(url).path).lstrip('/')
            assert target.is_file() or (target / 'index.html').is_file(), f'Broken local URL: {page}: {url}'
            checked += 1
    print(f'PASS: {len(pages)} pages, {len(paths)} article routes, {checked} local link/asset references; reconciliation and noindex verified.')


if __name__ == '__main__':
    main()
