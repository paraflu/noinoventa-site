"""Verify built local URLs/assets and reconciliation without publishing anything."""
from html.parser import HTMLParser
import json
import re
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


PRIVATE_ARTIFACT_MARKERS = (
    'complete-review-inventory.json',
    'editorialStatus',
    'reviewFlags',
    'sourceAccess',
    'sourceState',
)


def verify_private_inventory_is_not_built(root, public_data):
    """Check known structural leakage signals, not full data-loss prevention.

    Reject the exact inventory filename as any output path component, known
    case-sensitive metadata tokens in file/directory names, and literal markers
    in UTF-8-decoded output/public data. Arbitrarily renamed, encoded, compressed
    or otherwise transformed private data can evade this check. Article-ID checks
    here cover the conventional route shape only; main() separately verifies the
    expected article paths and total HTML count. Editorial privacy review remains
    required before any separately authorized publication.
    """
    root = Path(root)
    assert root.is_dir(), f'Build output missing: {root}'
    for candidate in root.rglob('*'):
        for component in candidate.relative_to(root).parts:
            assert component != 'complete-review-inventory.json', f'Private inventory path leaked into build output: {candidate}'
            for token in PRIVATE_ARTIFACT_MARKERS[1:]:
                assert token not in component, f'Private inventory path leaked into build output: {candidate}: {token}'
        if candidate.is_file():
            content = candidate.read_text(encoding='utf-8', errors='replace')
            for marker in PRIVATE_ARTIFACT_MARKERS:
                assert marker not in content, f'Private inventory marker leaked into {candidate}: {marker}'
    serialized_public_data = json.dumps(public_data, ensure_ascii=False)
    for marker in PRIVATE_ARTIFACT_MARKERS:
        assert marker not in serialized_public_data, f'Private inventory marker leaked into public data: {marker}'
    article_ids = {str(article['id']) for article in public_data.get('articles', [])}
    for page in root.rglob('index.html'):
        match = re.search(r'/notizie/(\d+)-[^/]+/index\.html$', page.as_posix())
        if match:
            assert match.group(1) in article_ids, f'Unapproved article page in build: {page}'


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
    verify_private_inventory_is_not_built(root, data)
    print(f'PASS: {len(pages)} pages, {len(paths)} article routes, {checked} local link/asset references; known private-artifact structural checks, reconciliation and noindex verified.')


if __name__ == '__main__':
    main()
