# FotoIndex

**Turn a folder of photographs into numbered contact sheets and an editable inventory, entirely on your computer.**

For photographers, visual researchers, and students who need to review a photo collection and record sources without uploading their images.

[Petunjuk Bahasa Indonesia](README.id.md) · [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md)

Generate a synthetic demo with `python examples/make_demo.py`; output is saved in `examples/report/`.

## Status

Working command-line prototype, v0.1.0. Not yet field-tested with external users. No claims of adoption, program eligibility, or institutional endorsement. This is not yet a desktop app. The package name has not been reserved on PyPI.

## Features

- Recursively inventory JPEG, PNG, TIFF, WebP, and BMP images.
- Export numbered 24-image contact sheets, keeping image aspect ratio and applying EXIF orientation.
- Export UTF-8 CSV with relative filename, displayed dimensions, byte size, camera, capture time when present, SHA-256, duplicate reference, and errors.
- Leave source URL, access date, role, and notes blank for your verified annotations.
- Flag byte-identical duplicates; never delete them.
- Continue past unreadable images with a visible placeholder and CSV error.
- Keep originals untouched; refuse to overwrite an existing report directory.
- No network calls, account, telemetry, or API key at runtime.

## Install from this repository

Requires Python 3.11 or newer. Installing Pillow requires internet unless already available.

```sh
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```sh
source .venv/bin/activate
```

Then install from the repository directory:

```sh
python -m pip install .
python -m fotoindex "path/to/photos" -o "reports/session-01"
```

Use a **new output folder** each run. Subfolders are included. If using an output folder inside the input folder, it is excluded from the scan. Avoid mixing old reports into the input photo collection.

## Outputs

| File | Purpose |
| --- | --- |
| `contact-sheet-001.jpg`, etc. | Up to 24 numbered thumbnails per page |
| `inventory.csv` | Full filenames and metadata; editable annotation columns |
| `summary.json` | File, duplicate, error, and page counts |

Numbers map contact-sheet labels to inventory rows. Long labels are shortened on the sheet; CSV retains full relative paths. CSV cells starting with spreadsheet formula prefixes are escaped with an apostrophe. Empty EXIF fields mean unavailable data, not a verified absence. EXIF values are unverified and can be edited by others. No time zone is inferred.

Exit codes: `0` complete; `1` input/output failure; `2` report produced with image errors. On an output failure a partial report can remain; use a new directory after correcting the problem.

## Limitations

RAW/HEIC, visual similarity search, color-managed print proofing, GUI, PDF export, and provenance verification are not implemented. Multi-frame images use the first frame. Very large images may be rejected by Pillow's safety checks. SHA-256 detects identical bytes, not visually equivalent photographs. Contact sheets are review aids, not color proofs. Fonts have limited script coverage. Filenames and camera metadata are included in reports; review them before sharing. GPS metadata is not exported.

## Development

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
python examples/make_demo.py
```

Seven tests cover duplicates, corrupted files, original-file integrity, EXIF orientation, pagination, output protection, formula escaping, and Unicode filenames. Local verification used Python 3.12 and Pillow 12.3. The CI workflow configures Windows/Linux with Python 3.11–3.13; check the Actions tab for current remote results.

## License

MIT for this project's code and generated synthetic demo. Photographs processed by the tool remain subject to their own rights. This project has no affiliation with OpenAI or any eligibility program.
