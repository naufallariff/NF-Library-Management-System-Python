# NF Library Management System (Modular Python)

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust and modular Command-Line Interface (CLI) application developed in Python to manage essential library operations, including member registration, book management, active loans, and transaction history. The project adheres strictly to **Clean Code** and **Single Responsibility Principles (SRP)**.

---

## ✨ Fitur Utama

* **CRUD Lengkap:** Manajemen (Create, Read, Update, Delete) untuk Anggota dan Buku.
* **Modularitas Tinggi:** Logika bisnis dipisahkan ke dalam modul *handler* (`anggota_handler`, `buku_handler`, `transaction_handler`).
* **Persistent Storage:** Menggunakan file **JSON** (dalam folder `data/`) untuk penyimpanan data yang terstruktur.
* **Robust Transactions:** Mencatat pinjaman aktif (`peminjaman.json`) dan menyimpan riwayat transaksi yang sudah selesai (`history.json`).
* **User Experience (UX):** Proses pinjam/kembali menggunakan fitur **pencarian nama/judul** yang *user-friendly* untuk menghindari input kode acak.
* **Konflik Handling:** Mencegah penghapusan Anggota/Buku yang masih terlibat dalam pinjaman aktif.
* **Graceful Exit:** Menangani interupsi `Ctrl+C` dengan pesan yang rapi.

---

## 🚀 Instalasi dan Menjalankan Proyek

Proyek ini tidak memerlukan *dependency* eksternal (hanya modul bawaan Python).

### 1. Klon Repositori

```bash
git clone [https://github.com/YOUR_USERNAME/NF-Library-Management-System-Python.git](https://github.com/YOUR_USERNAME/NF-Library-Management-System-Python.git)
cd NF-Library-Management-System-Python
