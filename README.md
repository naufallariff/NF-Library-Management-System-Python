
# SISTEM MANAJEMEN PERPUSTAKAAN NF (NF LIBRARY MANAGEMENT SYSTEM)


Aplikasi CLI Berbasis Python dengan Arsitektur Modular dan Clean Code

------------------------------------------------------------------------

## 1. Judul dan Deskripsi



*   **JUDUL PROYEK:** NF Library Management System (Arsitektur Modular)

*   **DESKRIPSI UMUM:**

    Aplikasi ini merupakan sistem manajemen perpustakaan berbasis Command-Line Interface (CLI) yang dibangun menggunakan Python. Kami mengutamakan penerapan prinsip-prinsip rekayasa perangkat lunak profesional, yaitu Modularitas Tingkat Lanjut dan Clean Code. Setiap komponen sistem dirancang untuk memiliki tanggung jawab tunggal (Single Responsibility Principle/SRP), menjamin kode yang kokoh, mudah diuji, dan sangat *maintainable*.

*   **LATAR BELAKANG PROYEK:**

    Sistem ini merupakan hasil pengembangan ekstensif dari tugas kelompok Akhir Semester 1 pada mata kuliah Dasar-Dasar Pemrograman. Tujuan pengembangan lebih lanjut adalah mentransformasi tugas dasar menjadi *codebase* yang profesional dan siap dikembangkan lebih lanjut. Proyek ini dikembangkan di bawah naungan **Sekolah Tinggi Teknologi Terpadu Nurul Fikri (STT Terpadu NF)**.

---

## 2. ✨ Fitur Utama (CRUD & Transaksi)



*   **MANAJEMEN DATA PUSAT (CRUD):**

    *   **CRUD Anggota:** Mendukung operasi Create, Read, Update, dan Delete penuh untuk semua data anggota perpustakaan.
    *   **CRUD Buku:** Mendukung operasi Create, Read, Update, dan Delete penuh untuk koleksi buku, termasuk pembaruan stok secara otomatis.

*   **INTEGRITAS TRANSAKSI:**

    *   **Pinjaman Aktif (loan\_active.json):** Mencatat transaksi pinjaman yang sedang berlangsung secara *real-time*.
    *   **Riwayat Transaksi (loan\_history.json):** Mencatat setiap pengembalian yang diselesaikan secara permanen, berfungsi sebagai log audit dan riwayat transaksi lengkap, termasuk detail denda dan waktu penyelesaian.
    *   **Penanganan Konflik:** Aplikasi memiliki mekanisme validasi yang ketat untuk mencegah penghapusan Anggota atau Buku jika mereka masih terdaftar dalam transaksi pinjaman aktif.

*   **PENINGKATAN USER EXPERIENCE (UX):**

    *   **Pencarian Cerdas:** Proses Pinjam dan Pengembalian menggunakan fungsi Pencarian/Filter berdasarkan nama anggota atau judul buku. Pengguna tidak perlu menghafal kode unik yang dibuat acak.

---

## 3. 🗂️ Struktur Proyek



Struktur proyek mencerminkan pemisahan tanggung jawab yang jelas antara Logika Bisnis dan Utilitas.

```
nf_library/
├── data/                    # Folder penyimpanan data (JSON)
│   ├── member.json          # Data Anggota
│   ├── book.json            # Data Buku
│   ├── loan_active.json     # Pinjaman Aktif
│   └── loan_history.json    # Riwayat Pinjaman Selesai
├── handlers/                # Modul yang berisi Logika Bisnis Inti (CRUD per Entitas)
│   ├── member_handler.py    # Mengelola semua fungsi CRUD Anggota
│   ├── book_handler.py      # Mengelola semua fungsi CRUD Buku
│   └── transaction_handler.py # Mengelola Pinjam, Kembali, dan Penentuan Denda
├── core/                    # Modul Fungsionalitas Umum (Utilitas Global)
│   ├── data_manager.py      # Satu-satunya modul yang bertugas membaca dan menulis file JSON
│   ├── utils.py             # Utilitas umum: clear screen, Generator Kode Unik
│   └── validation.py        # Utilitas validasi input dan fungsi pencarian (Search/Select)
└── main.py                  # Titik Awal (Entry Point) Aplikasi dan Menu Utama
```

---

## 4. 🚀 Instalasi dan Menjalankan Proyek



*   **PRASYARAT:**

    Membutuhkan Python 3.x. Tidak ada *library* eksternal pihak ketiga yang dibutuhkan.

*   **LANGKAH INSTALASI DAN EKSEKUSI:**

    1.  Klon Repositori:

        ```bash
        git clone https://github.com/naufallariff/NF-Library-Management-System-Python.git
        cd NF-Library-Management-System-Python
        ```

    2.  Jalankan Aplikasi:

        ```bash
        python3 main.py
        ```

        (Catatan: Folder 'data/' dan file-file JSON akan dibuat secara otomatis saat aplikasi dijalankan untuk pertama kalinya.)

---

## 5. 📚 Panduan Penggunaan



Aplikasi ini beroperasi melalui input menu di *command line*. Berikut adalah ringkasan opsi yang tersedia:

| KATEGORI        | OPSI | FUNGSI                                                                                                                                                                                                  |
| --------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MANAJEMEN DATA  | 1-4  | **Operasi CRUD Anggota:**                                                                                                                                                                               |
|                 |      | 1: Tambah Anggota, 2: Lihat Detail Anggota, 3: Edit Anggota, 4: Hapus Anggota                                                                                                                           |
|                 | 5-8  | **Operasi CRUD Buku:**                                                                                                                                                                                  |
|                 |      | 5: Tambah Buku, 6: Lihat Detail Buku, 7: Edit Buku, 8: Hapus Buku                                                                                                                                     |
| TRANSAKSI       | A    | Buat Pinjaman (Loan): Memproses peminjaman buku oleh anggota. Sistem akan memvalidasi ketersediaan buku dan status keanggotaan.                                                                          |
|                 | B    | Selesaikan Pengembalian (Return): Mencatat pengembalian buku. Sistem secara otomatis menghitung denda (jika ada) berdasarkan keterlambatan.                                                              |
|                 | C    | Hapus Entri Pinjaman (Pengembalian Paksa): Menghapus catatan pinjaman secara manual (gunakan dengan hati-hati).                                                                                            |
|                 | D    | Lihat Daftar Pinjaman Aktif: Menampilkan daftar buku yang sedang dipinjam.                                                                                                                             |
|                 | E    | Lihat Riwayat Transaksi (History): Menampilkan log lengkap transaksi yang telah selesai.                                                                                                               |
| SISTEM          | X    | Keluar dari aplikasi                                                                                                                                                                                    |

**Detail Manajemen Data (CRUD):**

*   **Tambah (Create):** Anda akan diminta memasukkan informasi yang diperlukan (nama, detail kontak untuk anggota; judul, pengarang, stok untuk buku). Sistem akan melakukan validasi dasar untuk memastikan data yang dimasukkan valid.
*   **Lihat (Read):** Menampilkan detail lengkap entitas yang dipilih. Untuk anggota, ini termasuk informasi pribadi dan riwayat peminjaman (jika ada). Untuk buku, ini termasuk judul, pengarang, dan jumlah stok tersedia.
*   **Edit (Update):** Memungkinkan Anda untuk memodifikasi informasi yang ada. Sistem akan memastikan bahwa perubahan yang dilakukan tidak melanggar aturan validasi (misalnya, stok buku tidak boleh negatif).
*   **Hapus (Delete):** Menghapus entitas dari sistem. Sistem akan memberikan peringatan jika entitas tersebut terkait dengan transaksi yang sedang berlangsung.

---

## 6. 🤝 Kontribusi



Program ini adalah karya pribadi yang dikembangkan dari tugas kelompok STT Terpadu NF.

*   **Atribusi:** Program ini dikembangkan oleh Muhammad Naufal Arif. Mohon berikan kredit yang sesuai jika Anda menggunakan atau mengembangkan *codebase* ini.
*   **Kontak Kontribusi:** Jika Anda tertarik untuk memperluas atau mengkontribusi pada proyek ini, silakan hubungi pengembang utama melalui email: **naufalarif09@gmail.com**.

---

## 7. 📄 Lisensi



Proyek ini dirilis di bawah **MIT License**.