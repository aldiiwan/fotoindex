"""Offline image catalog; originals are opened read-only."""
import argparse
import csv
import hashlib
import json
import sys
import warnings
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp', '.bmp'}
FIELDS = ['number', 'file', 'width', 'height', 'bytes', 'sha256', 'duplicate_of',
          'captured_at', 'camera', 'source_url', 'access_date', 'role', 'notes', 'error']


def safe_cell(value):
    """Keep filenames and EXIF strings from becoming spreadsheet formulas."""
    value = str(value)
    return "'" + value if value.lstrip().startswith(('=', '+', '-', '@')) else value


def inspect_photo(path, root, number, seen):
    row = dict.fromkeys(FIELDS, '')
    row.update(number=number, file=path.relative_to(root).as_posix())
    try:
        row['bytes'] = path.stat().st_size
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        row['sha256'] = digest
        row['duplicate_of'] = seen.get(digest, '')
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(path) as im:
                exif = im.getexif()
                row['camera'] = ' '.join(str(exif.get(k, '')).strip() for k in (271, 272)).strip()
                row['captured_at'] = exif.get(306, '')
                try:
                    row['captured_at'] = exif.get_ifd(34665).get(36867, row['captured_at'])
                except (KeyError, TypeError, ValueError):
                    pass
                im = ImageOps.exif_transpose(im)
                row['width'], row['height'] = im.size
                im.thumbnail((280, 190))
                thumb = im.convert('RGBA')
        seen.setdefault(digest, row['file'])
        return row, thumb
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError,
            Image.DecompressionBombWarning) as exc:
        row['error'] = f'{type(exc).__name__}: {exc}'
        return row, None


def make_page():
    page = Image.new('RGB', (1280, 1600), '#f5f2eb')
    draw = ImageDraw.Draw(page)
    draw.text((40, 25), 'FOTOINDEX / PHOTO INVENTORY', fill='#23332c', font=ImageFont.load_default(size=26))
    return page


def run(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_dir():
        raise ValueError('Input must be an existing photo folder.')
    if output == source or source.is_relative_to(output):
        raise ValueError('Output cannot equal or contain the input folder.')
    # Exclusive directory creation prevents silent replacement of an earlier report.
    output.mkdir(parents=True, exist_ok=False)
    paths = sorted((p for p in source.rglob('*') if p.is_file() and not p.is_symlink()
                    and not p.resolve().is_relative_to(output)
                    and p.suffix.lower() in EXTENSIONS), key=lambda p: p.relative_to(source).as_posix())
    if not paths:
        output.rmdir()
        raise ValueError('No supported images found.')
    seen, rows, page, pages = {}, [], None, 0
    font = ImageFont.load_default(size=15)
    for index, path in enumerate(paths):
        row, thumb = inspect_photo(path, source, index + 1, seen)
        rows.append(row)
        slot = index % 24
        if slot == 0:
            page = make_page()
        x, y = 40 + (slot % 4) * 310, 90 + (slot // 4) * 245
        draw = ImageDraw.Draw(page)
        draw.rectangle((x, y, x + 280, y + 190), fill='#dfdfd8')
        if thumb:
            page.paste(thumb, (x + (280 - thumb.width)//2, y + (190 - thumb.height)//2), thumb)
        else:
            draw.text((x+12, y+75), 'UNREADABLE IMAGE', font=font, fill='#9f2d21')
        # Number maps unambiguously to the full relative path in CSV.
        label = f"{index+1:04d}  {path.name}"
        while draw.textlength(label, font=font) > 275:
            label = label[:-4] + '...'
        draw.text((x, y+197), label, fill='#23332c', font=font)
        status = 'ERROR' if row['error'] else f"{row['width']} x {row['height']}"
        if row['duplicate_of']:
            status += ' / DUPLICATE'
        draw.text((x, y+217), status, fill='#666666', font=font)
        if slot == 23 or index == len(paths)-1:
            pages += 1
            draw.text((40, 1560), f'Page {pages} | Source metadata is not independently verified.', font=font, fill='#666666')
            page.save(output / f'contact-sheet-{pages:03d}.jpg', quality=92)
    with (output/'inventory.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({k: safe_cell(v) for k, v in row.items()} for row in rows)
    summary = {'version': '0.1.0', 'files': len(rows), 'errors': sum(bool(r['error']) for r in rows),
               'exact_duplicates': sum(bool(r['duplicate_of']) for r in rows), 'pages': pages}
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description='Create local contact sheets and a photo inventory. No uploads.')
    parser.add_argument('source', type=Path, help='Photo folder; subfolders included')
    parser.add_argument('-o', '--output', type=Path, required=True, help='New output directory (must not exist)')
    args = parser.parse_args(argv)
    try:
        result = run(args.source, args.output)
    except (ValueError, OSError) as exc:
        print(f'FotoIndex: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 2 if result['errors'] else 0
