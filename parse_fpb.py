#!/usr/bin/env python3
"""
parse_fpb.py - Parser Data Free Programming Books & Courses (Bahasa Indonesia)

================================================================================
SUMBER DATA & LISENSI
================================================================================
Sumber Data:
  Repositori resmi EbookFoundation/free-programming-books:
  1. Buku:
     https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/books/free-programming-books-id.md
  2. Kursus:
     https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/courses/free-courses-id.md

Lisensi Sumber:
  Creative Commons Attribution 4.0 International (CC BY 4.0)
  https://creativecommons.org/licenses/by/4.0/

Hak Cipta:
  Setiap materi (buku, kursus, video, tutorial) merupakan hak cipta penuh dari
  masing-masing penulis, instruktur, institusi, atau penerbit aslinya.

================================================================================
CARA PENGGUNAAN
================================================================================
Jalankan script ini menggunakan Python 3 (tanpa perlu install library tambahan):

  python parse_fpb.py

Script ini akan:
  1. Mengunduh data terbaru dari repositori GitHub EbookFoundation.
  2. Mem-parse data buku dan kursus berbahasa Indonesia.
  3. Menyimpan hasil terstruktur ke 'data.json' (format UTF-8, ensure_ascii=False).
  4. Menghasilkan atau memperbarui file 'web-pelatihan.html' (aplikasi web mandiri
     dengan data tersemat langsung di const D = [...]).
"""

import os
import re
import json
import urllib.request

# URL Sumber Data Mentah (Raw GitHub)
BOOKS_URL = "https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/books/free-programming-books-id.md"
COURSES_URL = "https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/courses/free-courses-id.md"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_JSON_PATH = os.path.join(BASE_DIR, "data.json")
HTML_PATH = os.path.join(BASE_DIR, "web-pelatihan.html")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Katalog buku dan kursus pemrograman gratis berbahasa Indonesia. Bersumber dari EbookFoundation/free-programming-books." />
  <title>Pelatihan Pemrograman Gratis (Bahasa Indonesia)</title>
  <style>
    :root {
      --font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --card-hover-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --input-bg: #ffffff;

      /* Aksen Teal */
      --primary: #0d9488;
      --primary-hover: #0f766e;
      --primary-light: #f0fdfa;
      --primary-border: #99f6e4;

      /* Badges */
      --badge-course-bg: #ccfbf1;
      --badge-course-text: #0f766e;
      --badge-course-border: #99f6e4;

      --badge-book-bg: #e0f2fe;
      --badge-book-text: #0369a1;
      --badge-book-border: #bae6fd;

      --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
      --card-shadow-hover: 0 10px 18px -3px rgba(13, 148, 136, 0.12), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --bg: #0b1120;
        --card-bg: #1e293b;
        --card-hover-bg: #243248;
        --text: #f8fafc;
        --text-muted: #94a3b8;
        --border: #334155;
        --input-bg: #1e293b;

        --primary: #14b8a6;
        --primary-hover: #2dd4bf;
        --primary-light: #134e4a33;
        --primary-border: #115e59;

        --badge-course-bg: #134e4a;
        --badge-course-text: #5eead4;
        --badge-course-border: #115e59;

        --badge-book-bg: #0c4a6e;
        --badge-book-text: #7dd3fc;
        --badge-book-border: #0369a1;

        --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
        --card-shadow-hover: 0 10px 20px -3px rgba(20, 184, 166, 0.22), 0 4px 8px -2px rgba(0, 0, 0, 0.25);
      }
    }

    [data-theme="dark"] {
      --bg: #0b1120;
      --card-bg: #1e293b;
      --card-hover-bg: #243248;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --border: #334155;
      --input-bg: #1e293b;

      --primary: #14b8a6;
      --primary-hover: #2dd4bf;
      --primary-light: #134e4a33;
      --primary-border: #115e59;

      --badge-course-bg: #134e4a;
      --badge-course-text: #5eead4;
      --badge-course-border: #115e59;

      --badge-book-bg: #0c4a6e;
      --badge-book-text: #7dd3fc;
      --badge-book-border: #0369a1;

      --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
      --card-shadow-hover: 0 10px 20px -3px rgba(20, 184, 166, 0.22), 0 4px 8px -2px rgba(0, 0, 0, 0.25);
    }

    [data-theme="light"] {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --card-hover-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --input-bg: #ffffff;

      --primary: #0d9488;
      --primary-hover: #0f766e;
      --primary-light: #f0fdfa;
      --primary-border: #99f6e4;

      --badge-course-bg: #ccfbf1;
      --badge-course-text: #0f766e;
      --badge-course-border: #99f6e4;

      --badge-book-bg: #e0f2fe;
      --badge-book-text: #0369a1;
      --badge-book-border: #bae6fd;

      --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
      --card-shadow-hover: 0 10px 18px -3px rgba(13, 148, 136, 0.12), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-family);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.2s ease, color 0.2s ease;
    }

    .container {
      width: 100%;
      max-width: 960px;
      margin: 0 auto;
      padding: 2rem 1.25rem 3rem;
      flex: 1;
    }

    /* HEADER */
    header {
      margin-bottom: 2rem;
    }

    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 0.75rem;
    }

    .title-group h1 {
      font-size: 1.85rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .title-group h1 .accent {
      color: var(--primary);
    }

    .tagline {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-top: 0.35rem;
      line-height: 1.45;
    }

    /* Theme Toggle */
    .theme-toggle-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 0.45rem 0.8rem;
      border-radius: 9999px;
      font-size: 0.825rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }

    .theme-toggle-btn:hover {
      color: var(--primary);
      border-color: var(--primary);
    }

    .theme-toggle-btn svg {
      width: 16px;
      height: 16px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    /* CONTROLS (SEARCH & FILTERS) */
    .controls-wrapper {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--card-shadow);
    }

    .controls-row-top {
      display: flex;
      gap: 0.75rem;
      flex-direction: column;
    }

    @media (min-width: 640px) {
      .controls-row-top {
        flex-direction: row;
      }
    }

    .search-box {
      position: relative;
      flex: 1;
    }

    .search-icon {
      position: absolute;
      left: 0.875rem;
      top: 50%;
      transform: translateY(-50%);
      width: 18px;
      height: 18px;
      color: var(--text-muted);
      pointer-events: none;
    }

    .search-input {
      width: 100%;
      padding: 0.65rem 2.25rem 0.65rem 2.5rem;
      font-size: 0.925rem;
      font-family: inherit;
      border: 1px solid var(--border);
      border-radius: 8px;
      background-color: var(--input-bg);
      color: var(--text);
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-light);
    }

    .search-clear-btn {
      position: absolute;
      right: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 1.25rem;
      line-height: 1;
      padding: 0.2rem;
      display: none;
    }

    .search-clear-btn:hover {
      color: var(--text);
    }

    .category-select-wrapper {
      min-width: 220px;
    }

    .category-select {
      width: 100%;
      padding: 0.65rem 2rem 0.65rem 0.875rem;
      font-size: 0.925rem;
      font-family: inherit;
      border: 1px solid var(--border);
      border-radius: 8px;
      background-color: var(--input-bg);
      color: var(--text);
      cursor: pointer;
      outline: none;
      appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 0.75rem center;
      background-size: 16px;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .category-select:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-light);
    }

    /* TABS & META ROW */
    .controls-row-bottom {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
    }

    .tab-pills {
      display: inline-flex;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.25rem;
      gap: 0.25rem;
    }

    .tab-pill {
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 500;
      padding: 0.4rem 0.875rem;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .tab-pill:hover:not(.active) {
      color: var(--text);
    }

    .tab-pill.active {
      background: var(--primary);
      color: #ffffff;
      font-weight: 600;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    .results-count-wrap {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .results-count {
      font-size: 0.875rem;
      font-weight: 600;
      color: var(--text-muted);
    }

    .reset-filters-link {
      font-size: 0.825rem;
      color: var(--primary);
      text-decoration: underline;
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
      font-family: inherit;
      display: none;
    }

    .reset-filters-link:hover {
      color: var(--primary-hover);
    }

    /* GRID OF CARDS */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 1rem;
    }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.125rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: var(--card-shadow);
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background-color 0.18s ease;
      position: relative;
    }

    .card:hover {
      transform: translateY(-2px);
      box-shadow: var(--card-shadow-hover);
      border-color: var(--primary);
      background-color: var(--card-hover-bg);
    }

    .card-top {
      margin-bottom: 0.65rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.725rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      border: 1px solid transparent;
      user-select: none;
    }

    .badge-kursus {
      background-color: var(--badge-course-bg);
      color: var(--badge-course-text);
      border-color: var(--badge-course-border);
    }

    .badge-buku {
      background-color: var(--badge-book-bg);
      color: var(--badge-book-text);
      border-color: var(--badge-book-border);
    }

    .external-icon {
      width: 14px;
      height: 14px;
      color: var(--text-muted);
      opacity: 0.6;
      transition: opacity 0.15s ease, transform 0.15s ease, color 0.15s ease;
      flex-shrink: 0;
    }

    .card:hover .external-icon {
      opacity: 1;
      color: var(--primary);
      transform: translate(1px, -1px);
    }

    .card-body {
      flex: 1;
      margin-bottom: 0.75rem;
    }

    .card-title {
      color: var(--text);
      font-size: 0.975rem;
      font-weight: 600;
      line-height: 1.45;
      text-decoration: none;
      display: inline-block;
      transition: color 0.15s ease;
    }

    .card:hover .card-title {
      color: var(--primary);
    }

    .card-meta {
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.4;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.35rem;
      border-top: 1px solid var(--border);
      padding-top: 0.6rem;
    }

    .meta-cat {
      font-weight: 600;
      color: var(--text);
    }

    .meta-separator {
      color: var(--text-muted);
      opacity: 0.5;
    }

    .meta-ket {
      color: var(--text-muted);
      word-break: break-word;
    }

    /* EMPTY STATE */
    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 4rem 1rem;
      background: var(--card-bg);
      border: 1px dashed var(--border);
      border-radius: 14px;
    }

    .empty-icon {
      width: 48px;
      height: 48px;
      margin: 0 auto 1rem;
      color: var(--text-muted);
      opacity: 0.5;
    }

    .empty-title {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
      color: var(--text);
    }

    .empty-desc {
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-bottom: 1.25rem;
    }

    .btn-reset {
      background: var(--primary);
      color: #ffffff;
      border: none;
      font-family: inherit;
      font-size: 0.875rem;
      font-weight: 600;
      padding: 0.5rem 1.25rem;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.15s ease;
    }

    .btn-reset:hover {
      background: var(--primary-hover);
    }

    /* FOOTER */
    footer {
      border-top: 1px solid var(--border);
      background-color: var(--card-bg);
      margin-top: auto;
      padding: 2rem 1rem;
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    .footer-inner {
      max-width: 960px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    footer a {
      color: var(--primary);
      text-decoration: underline;
      text-underline-offset: 2px;
      transition: color 0.15s ease;
    }

    footer a:hover {
      color: var(--primary-hover);
    }

    .footer-disclaimer {
      font-size: 0.8rem;
      opacity: 0.9;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- HEADER -->
    <header>
      <div class="header-top">
        <div class="title-group">
          <h1>
            <span>Pelatihan Pemrograman</span>
            <span class="accent">Gratis</span>
          </h1>
          <p class="tagline">
            Katalog materi belajar pemrograman gratis berbahasa Indonesia. Dikurasi dari buku dan video kursus terbuka.
          </p>
        </div>
        <button id="themeToggle" class="theme-toggle-btn" type="button" aria-label="Ganti Tema" title="Ganti tema gelap/terang">
          <svg id="themeIconSun" viewBox="0 0 24 24" style="display:none;">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
          <svg id="themeIconMoon" viewBox="0 0 24 24">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
          <span id="themeLabel">Tema</span>
        </button>
      </div>
    </header>

    <!-- KONTROL PENCARIAN & FILTER -->
    <section class="controls-wrapper" aria-label="Pencarian dan Filter Materi">
      <div class="controls-row-top">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="search"
            id="searchInput"
            class="search-input"
            placeholder="Cari judul, keterangan, kategori... (misal: Python, Sandhika, Web)"
            autocomplete="off"
            spellcheck="false"
          />
          <button id="searchClearBtn" class="search-clear-btn" type="button" title="Hapus pencarian">&times;</button>
        </div>

        <div class="category-select-wrapper">
          <select id="categorySelect" class="category-select" aria-label="Filter Kategori">
            <option value="">Semua Kategori</option>
          </select>
        </div>
      </div>

      <div class="controls-row-bottom">
        <div class="tab-pills" role="tablist" aria-label="Pilih Jenis Materi">
          <button type="button" class="tab-pill active" data-type="Semua" role="tab" aria-selected="true">Semua</button>
          <button type="button" class="tab-pill" data-type="Kursus" role="tab" aria-selected="false">Kursus</button>
          <button type="button" class="tab-pill" data-type="Buku" role="tab" aria-selected="false">Buku</button>
        </div>

        <div class="results-count-wrap">
          <span id="resultCount" class="results-count">Memuat...</span>
          <button id="resetFiltersBtn" type="button" class="reset-filters-link">Reset Filter</button>
        </div>
      </div>
    </section>

    <!-- GRID DAFTAR MATERI -->
    <main>
      <div id="cardsGrid" class="cards-grid" aria-live="polite">
        <!-- Kartu materi akan dirender dengan JavaScript -->
      </div>
    </main>
  </div>

  <!-- FOOTER ATRIBUSI WAJIB -->
  <footer>
    <div class="footer-inner">
      <div>
        <strong>Sumber Data &amp; Lisensi:</strong><br />
        Data dikurasi dari repositori
        <a href="https://github.com/EbookFoundation/free-programming-books" target="_blank" rel="noopener noreferrer">EbookFoundation/free-programming-books</a>
        di bawah lisensi
        <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">Creative Commons Attribution 4.0 International (CC BY 4.0)</a>.
      </div>
      <div class="footer-disclaimer">
        <strong>Catatan Hak Cipta:</strong> Halaman ini hanya menyediakan ringkasan katalog dan tautan langsung ke sumber materi pembelajaran eksternal. Seluruh hak cipta materi, video, buku, dan merek dagang sepenuhnya merupakan milik dari pencipta, instruktur, atau penerbit masing-masing.
      </div>
    </div>
  </footer>

  <script>
    // DATA MATERI TERSEMAT (Buku & Kursus)
    const D = __EMBEDDED_DATA__;

    // FUNGSI ESCAPE HTML UNTUK KEAMANAN XSS
    function escapeHtml(text) {
      if (text === null || text === undefined) return '';
      return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    // STATE APLIKASI
    let currentJenis = 'Semua';
    let searchQuery = '';
    let selectedCategory = '';

    // ELEMEN DOM
    const searchInput = document.getElementById('searchInput');
    const searchClearBtn = document.getElementById('searchClearBtn');
    const categorySelect = document.getElementById('categorySelect');
    const tabPills = document.querySelectorAll('.tab-pill');
    const resultCount = document.getElementById('resultCount');
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    const cardsGrid = document.getElementById('cardsGrid');
    const themeToggle = document.getElementById('themeToggle');
    const themeIconSun = document.getElementById('themeIconSun');
    const themeIconMoon = document.getElementById('themeIconMoon');
    const themeLabel = document.getElementById('themeLabel');

    // INISIALISASI DROPDOWN KATEGORI
    function initCategoryDropdown() {
      // Ambil seluruh kategori unik dari data dan urutkan sesuai abjad
      const categories = [...new Set(D.map(item => item.kategori).filter(Boolean))].sort((a, b) =>
        a.localeCompare(b, 'id', { sensitivity: 'base' })
      );

      categorySelect.innerHTML = `<option value="">Semua Kategori (${categories.length})</option>`;
      categories.forEach(cat => {
        const count = D.filter(item => item.kategori === cat).length;
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = `${cat} (${count})`;
        categorySelect.appendChild(opt);
      });
    }

    // INISIALISASI LABEL TAB PILLS DENGAN JUMLAH
    function initTabPillsCount() {
      const countSemua = D.length;
      const countKursus = D.filter(item => item.jenis === 'Kursus').length;
      const countBuku = D.filter(item => item.jenis === 'Buku').length;

      tabPills.forEach(pill => {
        const type = pill.getAttribute('data-type');
        if (type === 'Semua') pill.textContent = `Semua (${countSemua})`;
        if (type === 'Kursus') pill.textContent = `Kursus (${countKursus})`;
        if (type === 'Buku') pill.textContent = `Buku (${countBuku})`;
      });
    }

    // RENDER KARTU MATERI
    function render() {
      const q = searchQuery.trim().toLowerCase();

      const filtered = D.filter(item => {
        // Filter Jenis (Tab: Semua / Kursus / Buku)
        if (currentJenis !== 'Semua' && item.jenis !== currentJenis) {
          return false;
        }

        // Filter Dropdown Kategori
        if (selectedCategory && item.kategori !== selectedCategory) {
          return false;
        }

        // Filter Pencarian (Judul + Keterangan + Kategori, tidak peka huruf besar)
        if (q) {
          const matchJudul = item.judul.toLowerCase().includes(q);
          const matchKet = (item.ket || '').toLowerCase().includes(q);
          const matchKategori = (item.kategori || '').toLowerCase().includes(q);
          if (!matchJudul && !matchKet && !matchKategori) {
            return false;
          }
        }

        return true;
      });

      // Update Teks Jumlah Hasil: "N materi ditemukan"
      resultCount.textContent = `${filtered.length} materi ditemukan`;

      // Tampilkan / Sembunyikan Tombol Reset
      const isFiltered = Boolean(q || selectedCategory || currentJenis !== 'Semua');
      resetFiltersBtn.style.display = isFiltered ? 'inline' : 'none';
      searchClearBtn.style.display = q ? 'block' : 'none';

      // Render Grid atau Tampilan Kosong
      if (filtered.length === 0) {
        cardsGrid.innerHTML = `
          <div class="empty-state">
            <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              <line x1="8" y1="11" x2="14" y2="11"></line>
            </svg>
            <div class="empty-title">Tidak ada materi yang ditemukan</div>
            <p class="empty-desc">Coba ubah kata kunci pencarian atau sesuaikan pilihan filter kategori dan jenis.</p>
            <button type="button" class="btn-reset" onclick="resetFilters()">Reset Semua Filter</button>
          </div>
        `;
        return;
      }

      // Bangun HTML Kartu dengan perlindungan escapeHtml
      let cardsHtml = '';
      for (let i = 0; i < filtered.length; i++) {
        const item = filtered[i];
        const isBuku = item.jenis === 'Buku';
        const badgeClass = isBuku ? 'badge-buku' : 'badge-kursus';
        const safeJudul = escapeHtml(item.judul);
        const safeUrl = escapeHtml(item.url);
        const safeKategori = escapeHtml(item.kategori);
        const safeKet = escapeHtml(item.ket);
        const safeJenis = escapeHtml(item.jenis);

        cardsHtml += `
          <article class="card">
            <div class="card-top">
              <span class="badge ${badgeClass}">
                ${isBuku ? '📖' : '🎓'} ${safeJenis}
              </span>
              <svg class="external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
            </div>
            <div class="card-body">
              <a href="${safeUrl}" target="_blank" rel="noopener noreferrer" class="card-title">
                ${safeJudul}
              </a>
            </div>
            <div class="card-meta">
              <span class="meta-cat">${safeKategori}</span>
              ${safeKet ? `<span class="meta-separator">·</span><span class="meta-ket">${safeKet}</span>` : ''}
            </div>
          </article>
        `;
      }

      cardsGrid.innerHTML = cardsHtml;
    }

    // RESET FILTER
    function resetFilters() {
      searchInput.value = '';
      searchQuery = '';
      selectedCategory = '';
      categorySelect.value = '';
      currentJenis = 'Semua';

      tabPills.forEach(pill => {
        const isSemua = pill.getAttribute('data-type') === 'Semua';
        pill.classList.toggle('active', isSemua);
        pill.setAttribute('aria-selected', isSemua ? 'true' : 'false');
      });

      render();
      searchInput.focus();
    }

    // EVENT LISTENERS
    searchInput.addEventListener('input', e => {
      searchQuery = e.target.value;
      render();
    });

    searchClearBtn.addEventListener('click', () => {
      searchInput.value = '';
      searchQuery = '';
      render();
      searchInput.focus();
    });

    categorySelect.addEventListener('change', e => {
      selectedCategory = e.target.value;
      render();
    });

    tabPills.forEach(pill => {
      pill.addEventListener('click', () => {
        tabPills.forEach(p => {
          p.classList.remove('active');
          p.setAttribute('aria-selected', 'false');
        });
        pill.classList.add('active');
        pill.setAttribute('aria-selected', 'true');
        currentJenis = pill.getAttribute('data-type');
        render();
      });
    });

    resetFiltersBtn.addEventListener('click', resetFilters);

    // MODE TERANG / GELAP (CSS Variables + prefers-color-scheme + Toggle manual)
    const THEME_STORAGE_KEY = 'web_pelatihan_theme';

    function getSystemTheme() {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeIconSun.style.display = 'block';
        themeIconMoon.style.display = 'none';
        themeLabel.textContent = 'Terang';
      } else if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIconSun.style.display = 'none';
        themeIconMoon.style.display = 'block';
        themeLabel.textContent = 'Gelap';
      } else {
        document.documentElement.removeAttribute('data-theme');
        const sys = getSystemTheme();
        if (sys === 'dark') {
          themeIconSun.style.display = 'block';
          themeIconMoon.style.display = 'none';
          themeLabel.textContent = 'Terang';
        } else {
          themeIconSun.style.display = 'none';
          themeIconMoon.style.display = 'block';
          themeLabel.textContent = 'Gelap';
        }
      }
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || getSystemTheme();
      const next = current === 'dark' ? 'light' : 'dark';
      localStorage.setItem(THEME_STORAGE_KEY, next);
      applyTheme(next);
    }

    themeToggle.addEventListener('click', toggleTheme);

    // Dengar perubahan preferensi sistem jika pengguna belum memilih manual
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem(THEME_STORAGE_KEY)) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });

    // INISIALISASI SAAT HALAMAN DIBUKA
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    applyTheme(savedTheme || getSystemTheme());

    initCategoryDropdown();
    initTabPillsCount();
    render();
  </script>
</body>
</html>
'''


def download_markdown(url: str) -> str:
    """Mengunduh file Markdown mentah dari GitHub menggunakan urllib standar."""
    print(f"Mengunduh: {url} ...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def clean_category_name(raw_name: str) -> str:
    """
    Membersihkan nama kategori dari heading:
    - Menghapus tag HTML (misal <a id="...">)
    - Menghapus karakter backslash (\)
    - Merapikan spasi di awal dan akhir
    """
    cleaned = re.sub(r"<[^>]+>", "", raw_name)
    cleaned = cleaned.replace("\\", "")
    return cleaned.strip()


def clean_text(raw_text: str) -> str:
    """Membersihkan escape markdown seperti \\| menjadi |."""
    if not raw_text:
        return ""
    return raw_text.replace(r"\|", "|").strip()


def parse_markdown_content(content: str, jenis: str) -> list:
    """
    Mem-parse teks Markdown:
    - Heading ### / #### menjadi nama kategori (abaikan heading Index).
    - Item berformat * [Judul](url) - Keterangan diekstrak menjadi objek:
      {jenis, kategori, judul, url, ket}
    """
    items = []
    current_category = ""
    in_index = True

    # Regex untuk item baris: * [Judul](url) [- Keterangan opsional]
    item_pattern = re.compile(r"^\s*\*\s*\[(.*?)\]\((.*?)\)(?:\s*(?:[-–—]\s*)?(.*))?$")

    for line in content.splitlines():
        trimmed = line.strip()

        # Deteksi heading kategori (### atau ####)
        if line.startswith("### ") or line.startswith("#### "):
            raw_title = line.lstrip("#").strip()
            cat_name = clean_category_name(raw_title)

            # Abaikan bagian daftar isi (Index)
            if cat_name.lower() == "index":
                in_index = True
            else:
                in_index = False
                current_category = cat_name
            continue

        # Abaikan bila masih berada di bagian Index
        if in_index:
            continue

        # Deteksi baris item materi diawali tanda *
        if trimmed.startswith("*"):
            match = item_pattern.match(trimmed)
            if match:
                judul = clean_text(match.group(1))
                url = match.group(2).strip()
                ket = clean_text(match.group(3) or "")
                # Bersihkan tanda hubung sisa di awal keterangan
                ket = re.sub(r"^[-–—]\s*", "", ket).strip()

                items.append({
                    "jenis": jenis,
                    "kategori": current_category,
                    "judul": judul,
                    "url": url,
                    "ket": ket
                })

    return items


def save_or_update_html(html_file: str, data: list):
    """
    Menulis atau memperbarui file web-pelatihan.html.
    Karakter '</' di-escape menjadi '<\\/' agar aman di dalam tag <script>.
    """
    safe_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        pattern = re.compile(r"const\s+D\s*=\s*\[.*?\];", re.DOTALL)
        if pattern.search(html_content):
            # Gunakan callable (lambda) agar backslash pada safe_json tidak diproses sebagai backreference regex
            updated_html = pattern.sub(lambda _: f"const D = {safe_json};", html_content, count=1)
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(updated_html)
            return True

    # Jika file belum ada atau pola tidak ditemukan, buat dari template
    final_html = HTML_TEMPLATE.replace("__EMBEDDED_DATA__", safe_json)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    return True


def main():
    print("=" * 60)
    print("  Parser Free Programming Books & Courses (Bahasa Indonesia)")
    print("=" * 60)

    # 1. Unduh kedua file mentah
    books_md = download_markdown(BOOKS_URL)
    courses_md = download_markdown(COURSES_URL)

    # 2. Parse Markdown
    books_data = parse_markdown_content(books_md, "Buku")
    courses_data = parse_markdown_content(courses_md, "Kursus")

    total_data = books_data + courses_data

    # 3. Simpan ke data.json (ensure_ascii=False)
    json_output = json.dumps(total_data, ensure_ascii=False, indent=2)
    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        f.write(json_output)

    # 4. Tulis / Perbarui web-pelatihan.html
    save_or_update_html(HTML_PATH, total_data)

    # 5. Cetak ringkasan
    print("-" * 60)
    print(f"Sukses! Total {len(total_data)} materi berhasil diparse dan disimpan:")
    print(f"  • Buku   : {len(books_data)} entri")
    print(f"  • Kursus : {len(courses_data)} entri")
    print(f"File JSON: {DATA_JSON_PATH}")
    print(f"File Web : {HTML_PATH}")
    print("-" * 60)


if __name__ == "__main__":
    main()
