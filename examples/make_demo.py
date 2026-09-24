"""Reproducible synthetic demo; never touches a user's photos."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fotoindex.cli import run
root = Path(__file__).resolve().parent
photos = root/'synthetic'
photos.mkdir(exist_ok=True)
for i in range(8):
    im = Image.new('RGB', (600, 400), ['#81998f','#d5aa75','#6f8196','#b5887d'][i%4])
    d = ImageDraw.Draw(im)
    d.ellipse((330-i*12, 40, 430-i*12, 140), fill='#f9dfab')
    d.polygon([(0,400),(150,180+i*10),(330,400)], fill='#304943')
    d.polygon([(200,400),(430,200-i*8),(600,400)], fill='#486b60')
    im.save(photos/f'scene-{i+1:02d}.jpg')
report = root/'report'
if report.exists():
    raise SystemExit('Demo report already exists. Choose a new output with the CLI to regenerate.')
print(run(photos, report))
