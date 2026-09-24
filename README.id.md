# FotoIndex — panduan singkat

Alat **command-line lokal** untuk membuat contact sheet dan pendataan foto. Foto tidak diunggah. Versi awal 0.1.0 belum diuji oleh pengguna eksternal.

## Menjalankan di Windows

1. Pasang Python 3.11 atau lebih baru.
2. Ekstrak proyek, buka terminal di folder yang memuat `pyproject.toml`.
3. Jalankan:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\python.exe -m fotoindex "D:\Foto\Proyek" -o "D:\Laporan\Proyek-01"
```

Folder laporan harus baru. Instalasi dependensi membutuhkan internet; pemrosesan foto berjalan offline.

## Hasil

- `contact-sheet-001.jpg`: maksimal 24 thumbnail bernomor per halaman.
- `inventory.csv`: nama file, dimensi, kamera, tanggal EXIF jika ada, duplikat, serta kolom sumber/tanggal akses/peran/catatan untuk kamu isi.
- `summary.json`: jumlah foto, halaman, duplikat, dan error.

Foto asli tidak diubah atau dihapus. Duplikat dideteksi dari isi file identik, bukan kemiripan visual. File rusak tetap tercatat. Metadata tidak membuktikan kebenaran sumber atau kelengkapan populasi penelitian. Periksa laporan sebelum dibagikan karena memuat nama file dan metadata kamera.

Format: JPEG, PNG, TIFF, WebP, BMP. Belum mendukung RAW/HEIC, antarmuka desktop, atau ekspor PDF. Lihat README utama untuk batasan lengkap.
