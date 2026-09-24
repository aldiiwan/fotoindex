import csv
import hashlib
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from fotoindex.cli import run, safe_cell

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root/'photos'
        self.src.mkdir()
        self.out = self.root/'report'

    def photo(self, name='photo.jpg', exif=None):
        p = self.src/name
        Image.new('RGB', (60, 30), 'red').save(p, **({'exif': exif} if exif else {}))
        return p

    def test_duplicates_errors_and_original_unchanged(self):
        p = self.photo()
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        (self.src/'copy.jpg').write_bytes(p.read_bytes())
        (self.src/'broken.jpg').write_bytes(b'not an image')
        report = run(self.src, self.out)
        self.assertEqual((report['files'], report['exact_duplicates'], report['errors']), (3, 1, 1))
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), before)
        with (self.out/'inventory.csv').open(encoding='utf-8-sig') as f:
            self.assertEqual(len(list(csv.DictReader(f))), 3)
        self.assertTrue((self.out/'contact-sheet-001.jpg').exists())

    def test_exif_orientation(self):
        exif = Image.Exif(); exif[274] = 6
        self.photo(exif=exif)
        run(self.src, self.out)
        with (self.out/'inventory.csv').open(encoding='utf-8-sig') as f:
            row = next(csv.DictReader(f))
        self.assertEqual((row['width'], row['height']), ('30', '60'))

    def test_pagination(self):
        for n in range(25): self.photo(f'{n}.jpg')
        self.assertEqual(run(self.src, self.out)['pages'], 2)
        self.assertTrue((self.out/'contact-sheet-002.jpg').exists())

    def test_output_protection(self):
        self.photo()
        self.out.mkdir()
        with self.assertRaises(FileExistsError): run(self.src, self.out)
        with self.assertRaises(ValueError): run(self.src, self.src)
        with self.assertRaises(ValueError): run(self.src, self.root)

    def test_empty_folder(self):
        with self.assertRaises(ValueError): run(self.src, self.out)
        self.assertFalse(self.out.exists())

    def test_formula_safety(self):
        self.assertEqual(safe_cell('=HYPERLINK("bad")')[0], "'")
        self.assertEqual(safe_cell('  +SUM(1)')[0], "'")
        self.assertEqual(safe_cell('image.jpg'), 'image.jpg')

    def test_nested_output_and_unicode(self):
        self.photo('foto 日本.jpg')
        out = self.src/'report'
        self.assertEqual(run(self.src, out)['files'], 1)

if __name__ == '__main__': unittest.main()
