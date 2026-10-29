import unittest
from import_joomla import read_tables, public_text, project


class ImportTests(unittest.TestCase):
    def test_sql_escapes_and_prefix_allowlist(self):
        sql = "INSERT INTO `jos_content` (`id`) VALUES (99); INSERT INTO `jos25_content` (`id`,`title`,`introtext`) VALUES (1,'L\\'articolo','a,b; (c)\\nnext'),(2,'Altro','it''s ok');"
        rows = read_tables(sql)['jos25_content']
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['title'], "L'articolo")
        self.assertEqual(rows[0]['introtext'], 'a,b; (c)\nnext')
        self.assertEqual(rows[1]['introtext'], "it's ok")

    def test_text_is_safe_and_contacts_redacted(self):
        text, media = public_text('<script>secret</script><p>Info info@example.org 338 1234567</p><img src="x" onerror="alert(1)">{loadposition x}')
        self.assertNotIn('secret', text)
        self.assertNotIn('example.org', text)
        self.assertNotIn('1234567', text)
        self.assertNotIn('<', text)
        self.assertNotIn('loadposition', text)
        self.assertEqual(media, 1)

    def test_only_public_in_window_and_no_private_metadata(self):
        category = {'id': '2', 'extension': 'com_content', 'published': '1', 'access': '1', 'title': 'News', 'alias': 'news', 'parent_id': '1'}
        row = {'id': '1', 'catid': '2', 'state': '1', 'access': '1', 'alias': 'news', 'title': 'News', 'created': '2020-01-01 10:00:00', 'created_by': 'secret'}
        tables = {'jos25_content': [row, dict(row, id='2', access='2'), dict(row, id='3', publish_down='2021-01-01 00:00:00'), dict(row, id='4', publish_up='2030-01-01 00:00:00')], 'jos25_categories': [category], 'jos25_menu': []}
        data, report = project(tables, '2026-10-29 00:00:00')
        self.assertEqual([a['id'] for a in data['articles']], [1])
        self.assertNotIn('created_by', data['articles'][0])
        self.assertEqual(report['importedArticles'], 1)
        category['access'] = '2'
        self.assertEqual(project(tables, '2026-10-29 00:00:00')[0]['articles'], [])

    def test_missing_prefix_fails_closed(self):
        with self.assertRaises(ValueError):
            read_tables('INSERT INTO `jos_content` (`id`) VALUES (1);')


if __name__ == '__main__':
    unittest.main()
