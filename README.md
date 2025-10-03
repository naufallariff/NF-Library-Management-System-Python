
-----

# NF Library Management System (Modular Python)

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

Aplikasi Command-Line Interface (CLI) yang dikembangkan dengan Python, berfokus pada **Modularitas Tingkat Lanjut** dan **Clean Code** untuk mengelola operasi dasar perpustakaan (Anggota, Buku, Transaksi, dan Riwayat).

Proyek ini menggunakan pemisahan tanggung jawab yang ketat, di mana setiap fitur CRUD ditangani oleh modul *handler* tersendiri.

-----

## ✨ Fitur Utama (CRUD & Transaksi)

### Fungsionalitas Inti

  * **CRUD Lengkap:** Mendukung **C**reate, **R**ead, **U**pdate, **D**elete untuk entitas **Anggota** dan **Buku**.
  * **Persistent Storage:** Menggunakan file **JSON** (disimpan di folder `data/`) untuk menyimpan data secara terstruktur.
  * **Riwayat Transaksi:** Mencatat semua pengembalian yang berhasil ke file **`history.json`** untuk tujuan audit dan pelaporan.
  * **Arsitektur Modular:** Pemisahan fungsionalitas ke dalam modul `core/` dan `handlers/` untuk pemeliharaan yang mudah.

### Peningkatan UX & Robustness

  * **User-Friendly Input:** Proses Peminjaman dan Pengembalian menggunakan fitur **Pencarian/Filter** nama anggota atau judul buku, menghilangkan kebutuhan untuk mengingat Kode Unik (`ANGXXX`, `AAAXXX`).
  * **Penanganan Konflik:** Mencegah penghapusan **Anggota** atau **Buku** jika mereka masih terdaftar dalam transaksi pinjaman aktif (`peminjaman.json`).
  * **Perhitungan Denda:** Logika perhitungan denda diisolasi di modul `calculations.py`.
  * **Graceful Exit:** Menangani interupsi `Ctrl+C` dengan pesan yang rapi.

-----

## 🗂️ Struktur Proyek

Struktur folder mencerminkan fokus pada **Single Responsibility Principle (SRP)**:

```
nf_library/
├── data/                    # Penyimpanan data JSON
│   ├── anggota.json
│   ├── buku.json
│   ├── peminjaman.json      # Pinjaman aktif (On Loan)
│   └── history.json         # Riwayat pinjaman yang sudah selesai
├── handlers/                # Modul yang berisi Logika CRUD per Entitas
│   ├── anggota_handler.py   # CRUD Anggota
│   ├── buku_handler.py      # CRUD Buku
│   └── transaction_handler.py # Logika Pinjam, Kembali, Riwayat
├── core/                    # Modul Fungsionalitas Umum
│   ├── data_manager.py      # Tugas I/O file (Read/Write JSON)
│   ├── utils.py             # Clear screen, Generator Kode
│   ├── calculations.py      # calculate_fine
│   └── validation.py        # Input aman, Search/Select UX
└── main.py                  # Aplikasi Entry Point & Menu Utama
```

-----

## 🚀 Instalasi dan Menjalankan Proyek

### Prasyarat

  * Python 3.x (Proyek ini hanya menggunakan modul standar Python).

### Langkah-Langkah

1.  **Klon Repositori:**

    ```bash
    git clone https://github.com/naufallariff/NF-Library-Management-System-Python.git
    cd NF-Library-Management-System-Python
    ```

2.  **Jalankan Aplikasi:**

    ```bash
    python3 main.py
    ```

    *(Folder `data/` dan file JSON akan dibuat secara otomatis jika belum ada).*

-----

## 📚 Panduan Penggunaan

Aplikasi ini berbasis menu. Berikut adalah daftar menu utama untuk referensi cepat:

| Kategori | Opsi | Keterangan |
| :--- | :--- | :--- |
| **ANGGOTA** | `1` - `4` | Membuat, Mengedit, Menghapus, dan Melihat daftar Anggota. |
| **BUKU** | `5` - `8` | Membuat, Mengedit, Menghapus, dan Melihat daftar Buku. |
| **TRANSAKSI** | `A` | **Pinjam Buku:** Mencatat pinjaman baru (membutuhkan input nama/judul). |
| | `B` | **Kembalikan Buku:** Mencatat pengembalian, menghitung denda, dan memindahkan entri ke `history.json`. |
| | `C` | **Hapus Transaksi:** Pengembalian paksa (untuk menyelesaikan transaksi yang bermasalah). |
| | `D` | **Lihat Pinjaman Aktif:** Menampilkan isi dari `peminjaman.json`. |
| | `E` | **Lihat Riwayat Pinjaman:** Menampilkan catatan transaksi dari `history.json`. |
| **SISTEM** | `X` | Keluar dari aplikasi. |

-----

## 🤝 Kontribusi

Proyek ini terbuka untuk perbaikan dan penambahan fitur. Jika Anda ingin berkontribusi:

1.  *Fork* repositori ini.
2.  Buat *branch* fitur (`git checkout -b feature/nama-fitur`).
3.  Lakukan *commit* perubahan Anda dengan pesan yang deskriptif.
4.  *Push* ke *branch* Anda (`git push origin feature/nama-fitur`).
5.  Buat *Pull Request* baru.

-----

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

```
```