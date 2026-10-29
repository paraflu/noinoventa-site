"""Synthetic fixtures for the local structural leakage guard (not full DLP)."""
import tempfile
import unittest
from pathlib import Path

from check_static import verify_private_inventory_is_not_built


class StaticGuardTests(unittest.TestCase):
    def test_rejects_sensitive_basenames_without_content_markers(self):
        for token in ('editorialStatus', 'reviewFlags', 'sourceAccess', 'sourceState'):
            for name in (token, f'{token}.json', f'export-{token}.js'):
                with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                    candidate = Path(tmp) / 'assets' / name
                    candidate.parent.mkdir()
                    candidate.write_text('{}', encoding='utf-8')
                    with self.assertRaisesRegex(AssertionError, 'Private inventory path'):
                        verify_private_inventory_is_not_built(tmp, {'articles': []})

    def test_rejects_inventory_filename_as_file_or_directory_component(self):
        for kind in ('file', 'empty-directory', 'nested-directory'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                candidate = Path(tmp) / 'assets' / 'complete-review-inventory.json'
                candidate.parent.mkdir()
                if kind == 'file':
                    candidate.write_text('{}', encoding='utf-8')
                else:
                    candidate.mkdir()
                    if kind == 'nested-directory':
                        (candidate / 'index.html').write_text('<html></html>', encoding='utf-8')
                with self.assertRaisesRegex(AssertionError, 'Private inventory path'):
                    verify_private_inventory_is_not_built(tmp, {'articles': []})

    def test_rejects_sensitive_directory_names(self):
        for token in ('editorialStatus', 'reviewFlags', 'sourceAccess', 'sourceState'):
            with self.subTest(token=token), tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / token).mkdir()
                with self.assertRaisesRegex(AssertionError, 'Private inventory path'):
                    verify_private_inventory_is_not_built(tmp, {'articles': []})

    def test_accepts_benign_public_output_and_approved_article(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'notizie' / '1-public-news' / 'index.html'
            page.parent.mkdir(parents=True)
            page.write_text('<html><body>Public news</body></html>', encoding='utf-8')
            (root / 'public.json').write_text('{"title":"Public news"}', encoding='utf-8')
            (root / 'logo.bin').write_bytes(b'\x89PNG\xff\x00')
            verify_private_inventory_is_not_built(root, {'articles': [{'id': 1}]})


if __name__ == '__main__':
    unittest.main()
