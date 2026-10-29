#!/usr/bin/env python3
"""Offline, allowlisted Joomla SQL reader. Never executes SQL or connects to Joomla."""
import argparse
from collections import Counter
from datetime import datetime
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

TABLES = ('jos25_content', 'jos25_categories', 'jos25_menu')


def read_tables(sql):
    tables = {name: [] for name in TABLES}
    pattern = r'INSERT INTO `(jos25_content|jos25_categories|jos25_menu)`\s*\(([^)]+)\)\s*VALUES\s*'
    for match in re.finditer(pattern, sql):
        columns = re.findall(r'`([^`]+)`', match[2])
        i = match.end()
        while i < len(sql):
            while sql[i].isspace() or sql[i] == ',':
                i += 1
            if sql[i] == ';':
                break
            if sql[i] != '(':
                raise ValueError('Unexpected SQL tuple')
            i += 1
            values = []
            while True:
                while sql[i].isspace():
                    i += 1
                if sql[i] == "'":
                    i += 1
                    value = ''
                    while True:
                        ch = sql[i]
                        i += 1
                        if ch == '\\':
                            esc = sql[i]
                            i += 1
                            value += {'n': '\n', 'r': '\r', 't': '\t', '0': '\0', 'Z': '\x1a'}.get(esc, esc)
                        elif ch == "'":
                            if sql[i] == "'":
                                value += "'"
                                i += 1
                            else:
                                break
                        else:
                            value += ch
                else:
                    start = i
                    while sql[i] not in ',)':
                        i += 1
                    value = sql[start:i].strip()
                    value = None if value == 'NULL' else value
                values.append(value)
                while sql[i].isspace():
                    i += 1
                delimiter = sql[i]
                i += 1
                if delimiter == ')':
                    break
                if delimiter != ',':
                    raise ValueError('Unexpected SQL delimiter')
            if len(values) != len(columns):
                raise ValueError('SQL column count mismatch')
            tables[match[1]].append(dict(zip(columns, values)))
    if not tables['jos25_content']:
        raise ValueError('No jos25_content rows found; no other prefix is accepted')
    return tables


class PublicText(HTMLParser):
    """Text-only projection: no executable HTML, embeds, attributes or form data."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0
        self.media = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'object', 'form'):
            self.hidden += 1
        if tag in ('img', 'iframe', 'object', 'video', 'audio'):
            self.media += 1
        if tag in ('p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'tr'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'object', 'form'):
            self.hidden = max(0, self.hidden - 1)
        if tag in ('p', 'div', 'li', 'h1', 'h2', 'h3', 'tr'):
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def public_text(value):
    parser = PublicText()
    parser.feed(value or '')
    text = html.unescape(''.join(parser.parts)).replace('\xa0', ' ')
    text = re.sub(r'\{[^{}]*\}', '', text)  # Joomla plugin directives
    substitutions = [
        (r'(?i)\bhttps?://\S+', '[link omesso]'),
        (r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', '[email omessa]'),
        (r'(?i)\bIT\d{2}[A-Z0-9 ]{15,30}\b', '[IBAN omesso]'),
        (r'(?i)\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b', '[codice fiscale omesso]'),
        (r'(?<!\w)(?:\+39[ .-]?)?(?:0\d{2,4}|3\d{2})[ .-]?\d[\d .-]{4,10}\d(?!\w)', '[recapito omesso]'),
    ]
    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text)
    text = '\n'.join(re.sub(r'[ \t]+', ' ', line).strip() for line in text.splitlines())
    return re.sub(r'\n{3,}', '\n\n', text).strip(), parser.media


def date_value(value):
    if not value or value.startswith('0000-'):
        return None
    datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value  # preserve source wall time; Joomla timezone is unknown


def project(tables, as_of):
    categories = {r['id']: r for r in tables['jos25_categories'] if r.get('extension') == 'com_content'}
    excluded = Counter()
    articles = []
    for row in tables['jos25_content']:
        category = categories.get(row['catid'])
        if row.get('state') != '1' or row.get('access') != '1':
            excluded['non_public_article'] += 1
            continue
        lineage, seen = category, set()
        category_public = True
        while lineage and lineage['id'] not in seen:
            seen.add(lineage['id'])
            if lineage.get('published') != '1' or lineage.get('access') != '1':
                category_public = False
            parent = lineage.get('parent_id')
            if parent not in (None, '0', '1') and parent not in categories:
                category_public = False
            lineage = categories.get(parent)
        if lineage and lineage['id'] in seen:
            category_public = False
        if not category or not category_public:
            excluded['non_public_or_missing_category'] += 1
            continue
        up, down = date_value(row.get('publish_up')), date_value(row.get('publish_down'))
        if (up and up > as_of) or (down and down <= as_of):
            excluded['outside_publication_window'] += 1
            continue
        alias = row.get('alias') or ''
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', alias):
            excluded['unsafe_or_missing_alias'] += 1
            continue
        body, media = public_text((row.get('introtext') or '') + '\n' + (row.get('fulltext') or ''))
        title, _ = public_text(row['title'])
        cat_title, _ = public_text(category['title'])
        articles.append({
            'id': int(row['id']), 'title': title, 'alias': alias,
            'path': f"/notizie/{row['id']}-{alias}/",
            'category': cat_title, 'categoryAlias': category['alias'],
            'created': date_value(row.get('created')), 'modified': date_value(row.get('modified')),
            'publishUp': up, 'publishDown': down,
            'paragraphs': [p for p in body.split('\n') if p],
            'mediaOmitted': media,
            'reviewRequired': media > 0 or not body or '[recapito omesso]' in body or '[email omessa]' in body,
        })
    articles.sort(key=lambda a: (a['created'] or '', a['id']), reverse=True)
    ids = {a['id'] for a in articles}
    menus = []
    for row in tables['jos25_menu']:
        if row.get('published') != '1' or row.get('access') != '1' or row.get('client_id') != '0':
            continue
        query = parse_qs(urlsplit(row.get('link') or '').query)
        if query.get('option') != ['com_content'] or query.get('view') != ['article']:
            continue
        article_id = (query.get('id') or [''])[0].split(':')[0]
        path = row.get('path') or ''
        if article_id.isdigit() and int(article_id) in ids and re.fullmatch(r'[A-Za-z0-9_/-]+', path):
            menus.append({'path': '/' + path.strip('/') + '/', 'articleId': int(article_id)})
    report = {
        'reconciliation': {'source': len(tables['jos25_content']), 'imported': len(articles), 'excluded': sum(excluded.values()), 'errors': 0},
        'sourceStates': dict(Counter(r['state'] for r in tables['jos25_content'])),
        'articlesWithoutCategory': sum(r['catid'] == '0' for r in tables['jos25_content']),
        'contentCategories': len(categories),
        'sourcePrefix': 'jos25_', 'tables': list(TABLES), 'asOf': as_of,
        'sourceRows': {table: len(rows) for table, rows in tables.items()},
        'importedArticles': len(articles), 'excluded': dict(excluded),
        'mappedArticleMenus': len(menus),
        'articlesNeedingReview': sum(a['reviewRequired'] for a in articles),
        'mediaReferencesOmitted': sum(a['mediaOmitted'] for a in articles),
        'limitations': ['Text-only public projection; media, attachments, HTML links and Joomla plugins require editorial review.',
                       'Original aliases and wall-time dates retained; source timezone is not inferred.',
                       'Only direct public article menu paths mapped; no inferred Joomla SEF routes.',
                       'Authors, users, sessions, ACL, credentials and private metadata are not exported.',
                       'Automated contact redaction is not a substitute for editorial privacy review.'],
    }
    assert len(tables['jos25_content']) == len(articles) + sum(excluded.values()), 'Unreconciled source rows'
    return {'articles': articles, 'menus': menus}, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dump', type=Path)
    parser.add_argument('--as-of', required=True, help='Publication cutoff, YYYY-MM-DD HH:MM:SS (source wall time)')
    parser.add_argument('--output', type=Path, default=Path('src/data/joomla.json'))
    parser.add_argument('--report', type=Path, default=Path('docs/import-report.json'))
    args = parser.parse_args()
    date_value(args.as_of)
    data, report = project(read_tables(args.dump.read_text(encoding='utf-8')), args.as_of)
    for path, value in ((args.output, data), (args.report, report)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
