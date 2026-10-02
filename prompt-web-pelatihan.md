# Prompt: Web Pelatihan Pemrograman Gratis (Bahasa Indonesia)

Tempel prompt di bawah ini ke AI atau coding agent untuk membuat ulang webnya.

---

```
Buatkan website "Pelatihan Pemrograman Gratis (Bahasa Indonesia)" dalam SATU file HTML
(HTML + CSS + JavaScript inline, tanpa framework, tanpa build tool).

SUMBER DATA
- Repo: github.com/EbookFoundation/free-programming-books (lisensi CC BY 4.0)
- Ambil dua file mentah ini:
  1. https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/books/free-programming-books-id.md
  2. https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/courses/free-courses-id.md
- Jangan scraping halaman pencarian GitHub (diblokir dan dirender JavaScript).

LANGKAH 1 - Script Python parse_fpb.py
- Unduh kedua file dengan urllib (tanpa library tambahan).
- Parse Markdown: heading ### / #### = kategori (abaikan heading "Index"; bersihkan tag
  HTML seperti <a id="..."> dan karakter backslash dari nama kategori).
- Baris item berformat: * [Judul](url) - Keterangan/Penulis
  → ekstrak dengan regex menjadi objek:
  {jenis: "Buku"/"Kursus", kategori, judul, url, ket}
- Simpan ke data.json (ensure_ascii=False). Cetak jumlah entri.
- Beri docstring: sumber, lisensi, cara pakai.

LANGKAH 2 - Halaman web
- Sisipkan isi data.json langsung ke dalam <script> sebagai const D=[...]
  (escape "</" agar aman). Jangan fetch data dari luar saat runtime.
- Fitur:
  • Kolom pencarian (judul + keterangan + kategori, real-time, tidak peka huruf besar)
  • Dropdown filter kategori (otomatis dari data, urut abjad)
  • Tab pill: Semua / Kursus / Buku
  • Teks jumlah hasil: "N materi ditemukan"
  • Grid kartu responsif: badge jenis, judul (link target="_blank" rel="noopener"),
    baris kecil "kategori · keterangan"
  • Escape HTML pada semua teks dari data
- Tampilan: bersih dan minimalis, warna aksen teal, mendukung mode terang dan gelap
  (CSS variables + prefers-color-scheme), font system-ui, max-width 960px,
  mobile-friendly (viewport meta, grid auto-fill minmax(270px,1fr)).
- Footer wajib: atribusi ke EbookFoundation/free-programming-books (CC BY 4.0) dengan link,
  plus catatan bahwa halaman hanya menautkan ke sumber luar dan hak cipta materi milik
  pembuatnya masing-masing.

OUTPUT
- parse_fpb.py, data.json, dan web-pelatihan.html.
- Semua teks antarmuka dalam bahasa Indonesia.
- Setelah selesai, jelaskan singkat cara memperbarui data (jalankan ulang script).
```

---

## Pengembangan lanjutan (opsional)

Tambahkan salah satu kalimat ini di akhir prompt:

- *"Tambahkan jalur belajar Python terurut (dasar → menengah) dan checklist 'sudah dipelajari' yang disimpan di localStorage."*
- *"Tambahkan tampilan khusus untuk materi YouTube dengan thumbnail."*
- *"Tambahkan tombol favorit dan halaman 'Materi Saya'."*
