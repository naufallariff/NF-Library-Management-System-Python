# handlers/transaction_handler.py

from core.data_manager import get_all_data, save_all_data
from core.utils import clear_screen
from core.validation import validate_input_str, validate_input_int, search_and_select
from core.calculations import calculate_fine
import time
import random 

# Import Helper dari modul handler lain untuk UI
from handlers.anggota_handler import _prompt_and_select_anggota
from handlers.buku_handler import _prompt_and_select_buku

# --- CORE LOGIC: PINJAM & KEMBALI ---

def _execute_transaction(tipe_proses):
    """Fungsi inti untuk memproses pinjaman atau pengembalian dengan manajemen stok dan riwayat."""
    clear_screen()
    data = get_all_data()
    proses_nama = "PEMINJAMAN" if tipe_proses == 'pinjam' else "PENGEMBALIAN"
    print(f'\n*** {proses_nama} BUKU ***')
    
    # 1. Pilih Buku (Menggunakan UI Cari/Pilih)
    print("\n[Select Book]")
    kode_buku, buku = _prompt_and_select_buku(data)
    if not buku: return

    # 2. Pilih Anggota (Menggunakan UI Cari/Pilih)
    print("\n[Select Member]")
    kode_anggota, anggota = _prompt_and_select_anggota(data)
    if not anggota: return
        
    # --- LOGIKA PINJAM ---
    if tipe_proses == 'pinjam':
        if buku['stok'] <= 0:
            print(f"Stock for '{buku['judul']}' is zero. Loan failed.")
            return
            
        peminjam_list = data['peminjaman'].get(kode_buku, [])
        if kode_anggota in peminjam_list:
            print(f"Member {anggota['nama']} has already borrowed this book.")
            return

        buku['stok'] -= 1
        
        if kode_buku not in data['peminjaman']:
            data['peminjaman'][kode_buku] = []
        data['peminjaman'][kode_buku].append(kode_anggota)
        print(f"\nLoan successful: '{buku['judul']}' by {anggota['nama']}. Stock remaining: {buku['stok']}.")
    
    # --- LOGIKA KEMBALI (COMPLETE RETURN) ---
    elif tipe_proses == 'kembali':
        peminjam_list = data['peminjaman'].get(kode_buku, [])
        if kode_anggota not in peminjam_list:
            print("This book is not currently loaned by this member. Return failed.")
            return

        terlambat = validate_input_int("Days late (0 if on time): ")
        total_denda = calculate_fine(anggota['jenis_anggota'], terlambat) 
        
        # Log transaksi ke history
        history_id = str(int(time.time())) + str(random.randint(100, 999)) 
        data['history'][history_id] = {
            'book_code': kode_buku,
            'member_code': kode_anggota,
            'fine_paid': total_denda,
            'days_late': terlambat,
            'completed_date': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Update stok dan hapus dari daftar pinjaman aktif
        buku['stok'] += 1
        data['peminjaman'][kode_buku].remove(kode_anggota)
        
        if not data['peminjaman'][kode_buku]:
            del data['peminjaman'][kode_buku]
            
        print(f"\nReturn successful: '{buku['judul']}' by {anggota['nama']}. Transaction logged to history.")

    save_all_data(data)

def create_loan():
    """Memulai proses peminjaman buku."""
    _execute_transaction('pinjam')

def complete_return():
    """Menyelesaikan proses pengembalian buku."""
    _execute_transaction('kembali')

# --- DELETE TRANSAKSI (PENGEMBALIAN PAKSA) ---

def delete_loan_entry():
    """Menghapus entri peminjaman secara paksa dan mencatatnya sebagai riwayat dengan catatan khusus."""
    clear_screen()
    print('\n*** DELETE LOAN ENTRY (FORCED RETURN) ***')
    data = get_all_data()

    # 1. Pilih Buku yang sedang dipinjam
    borrowed_books_data = {
        k: data['buku'][k] for k in data['peminjaman'] if k in data['buku']
    }
    
    if not borrowed_books_data:
        print("No books are currently on loan.")
        return
    
    print("\n[Select Book to Return]")
    kode_buku = search_and_select(borrowed_books_data, 'judul', "Search Book Title (or 'X' to cancel): ", "Book not found.")
    if not kode_buku: return
    
    buku = data['buku'][kode_buku]

    # 2. Pilih Anggota yang meminjam
    current_borrowers = {
        k: data['anggota'][k] for k in data['peminjaman'][kode_buku] if k in data['anggota']
    }
    
    print("\n[Select Member Returning]")
    kode_anggota = search_and_select(current_borrowers, 'nama', "Search Member Name (or 'X' to cancel): ", "Member not found.")
    if not kode_anggota: return
    
    anggota = data['anggota'][kode_anggota]
    
    # 3. Proses Pengembalian/Penghapusan
    terlambat = validate_input_int("Days late (0 if on time): ")
    total_denda = calculate_fine(anggota['jenis_anggota'], terlambat) 

    # LOGGING HISTORY DENGAN CATATAN KHUSUS
    history_id = str(int(time.time())) + str(random.randint(100, 999)) 
    data['history'][history_id] = {
        'book_code': kode_buku,
        'member_code': kode_anggota,
        'fine_paid': total_denda,
        'days_late': terlambat,
        'completed_date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'notes': 'Forced Return/Loan Delete by Admin'
    }

    # 4. Hapus dari peminjaman aktif & update stok
    data['buku'][kode_buku]['stok'] += 1
    data['peminjaman'][kode_buku].remove(kode_anggota)
    
    if not data['peminjaman'][kode_buku]:
        del data['peminjaman'][kode_buku]
        
    print(f"\nLoan entry for '{buku['judul']}' by {anggota['nama']} successfully deleted/resolved and logged to history.")
    save_all_data(data)

# --- READ TRANSAKSI (View Peminjam Aktif) ---

def view_loan_list():
    """Menampilkan daftar semua buku yang sedang dipinjam."""
    clear_screen()
    print('='*10, 'DAFTAR PEMINJAM AKTIF', '='*10)
    
    data = get_all_data()
    
    if not data['peminjaman']:
        print("No books are currently on loan.")
        return

    for kode_buku, list_peminjam in data['peminjaman'].items():
        buku = data['buku'].get(kode_buku, {'judul': '[Title Not Found]', 'penulis': 'N/A'})
        
        print(f"Judul: {buku['judul']}")
        print(f"Penulis: {buku['penulis']}")
        print("Daftar Peminjam:")
        
        for i, kode_anggota in enumerate(list_peminjam, 1):
            anggota = data['anggota'].get(kode_anggota, {'nama': 'Unknown Member', 'jenis_anggota': 0})
            grup_label = '(*NF Group)' if anggota['jenis_anggota'] == 1 else ''
            print(f"{i}. {anggota['nama']} {grup_label} (Code: {kode_anggota})")
        print("-" * 30)