from core.data_manager import get_all_data, save_all_data
from core.utils import clear_screen
from core.validation import validate_input_str, validate_input_int, search_and_select
from core.calculations import calculate_fine
import time
import random 

# Mengimpor Helper dari modul handler lain untuk UI pencarian
from handlers.member_handler import _prompt_and_select_member
from handlers.book_handler import _prompt_and_select_book

# --- CORE LOGIC: PINJAM & KEMBALI ---

def _execute_transaction(transaction_type):
    """Fungsi inti untuk memproses peminjaman atau pengembalian dengan manajemen stok dan riwayat."""
    clear_screen()
    data = get_all_data()
    
    # Menentukan nama proses untuk tampilan CLI
    process_name = "PEMINJAMAN" if transaction_type == 'loan' else "PENGEMBALIAN"
    print(f'\n*** {process_name} BUKU ***')
    
    # 1. Pilih Buku menggunakan UX pencarian
    print("\n[Pilih Buku]")
    book_code, book = _prompt_and_select_book(data)
    if not book: return

    # 2. Pilih Anggota menggunakan UX pencarian
    print("\n[Pilih Anggota]")
    member_code, member = _prompt_and_select_member(data)
    if not member: return
        
    # --- LOGIKA PINJAM (LOAN) ---
    if transaction_type == 'loan':
        if book['stok'] <= 0:
            print(f"Stok untuk '{book['judul']}' kosong. Peminjaman gagal.")
            return
            
        loan_list = data['loan_active'].get(book_code, [])
        if member_code in loan_list:
            print(f"Anggota {member['nama']} sudah meminjam buku ini.")
            return

        # Update Stok dan mencatat ke loan_active
        book['stok'] -= 1
        
        if book_code not in data['loan_active']:
            data['loan_active'][book_code] = []
        data['loan_active'][book_code].append(member_code)
        
        print(f"\nPeminjaman berhasil: '{book['judul']}' oleh {member['nama']}. Sisa Stok: {book['stok']}.")
    
    # --- LOGIKA KEMBALI (RETURN) ---
    elif transaction_type == 'return':
        loan_list = data['loan_active'].get(book_code, [])
        if member_code not in loan_list:
            print("Buku ini tidak sedang dipinjam oleh anggota tersebut. Pengembalian gagal.")
            return

        days_late = validate_input_int("Keterlambatan (hari, 0 jika tepat waktu): ")
        total_fine = calculate_fine(member['jenis_anggota'], days_late) 
        
        # Log transaksi ke history
        history_id = str(int(time.time())) + str(random.randint(100, 999)) 
        data['loan_history'][history_id] = {
            'book_code': book_code,
            'member_code': member_code,
            'fine_paid': total_fine,
            'days_late': days_late,
            'completed_date': time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Update stok dan hapus dari daftar pinjaman aktif
        book['stok'] += 1
        data['loan_active'][book_code].remove(member_code)
        
        if not data['loan_active'][book_code]:
            del data['loan_active'][book_code]
            
        print(f"\nPengembalian berhasil: '{book['judul']}' oleh {member['nama']}. Transaksi dicatat ke riwayat.")

    save_all_data(data)

def create_loan():
    """Memulai proses peminjaman buku."""
    _execute_transaction('loan')

def complete_return():
    """Menyelesaikan proses pengembalian buku."""
    _execute_transaction('return')

# --- DELETE TRANSAKSI (PENGEMBALIAN PAKSA) ---

def delete_loan_entry():
    """Menghapus entri pinjaman secara paksa (pengembalian paksa) dan mencatatnya ke riwayat."""
    clear_screen()
    print('\n*** HAPUS ENTRI PINJAMAN (PENGEMBALIAN PAKSA) ***')
    data = get_all_data()

    # 1. Pilih Buku yang sedang dipinjam
    # Hanya tampilkan buku yang ada di daftar pinjaman aktif
    borrowed_books_data = {
        code: data['book'][code] for code in data['loan_active'] if code in data['book']
    }
    
    if not borrowed_books_data:
        print("Tidak ada buku yang sedang dipinjam.")
        return
    
    print("\n[Pilih Buku yang akan Dikembalikan]")
    book_code = search_and_select(borrowed_books_data, 'judul', "Cari Judul Buku (atau 'X' untuk batal): ", "Buku tidak ditemukan.")
    if not book_code: return
    
    book = data['book'][book_code]

    # 2. Pilih Anggota yang meminjam buku tersebut
    current_borrowers = {
        code: data['member'][code] for code in data['loan_active'][book_code] if code in data['member']
    }
    
    print("\n[Pilih Anggota yang Mengembalikan]")
    member_code = search_and_select(current_borrowers, 'nama', "Cari Nama Anggota (atau 'X' untuk batal): ", "Anggota tidak ditemukan.")
    if not member_code: return
    
    member = data['member'][member_code]
    
    # 3. Proses Pengembalian/Penghapusan
    days_late = validate_input_int("Keterlambatan (hari, 0 jika tepat waktu): ")
    total_fine = calculate_fine(member['jenis_anggota'], days_late) 

    # LOGGING HISTORY DENGAN CATATAN KHUSUS
    history_id = str(int(time.time())) + str(random.randint(100, 999)) 
    data['loan_history'][history_id] = {
        'book_code': book_code,
        'member_code': member_code,
        'fine_paid': total_fine,
        'days_late': days_late,
        'completed_date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'notes': 'Pengembalian Paksa oleh Admin'
    }

    # 4. Hapus dari pinjaman aktif & update stok
    data['book'][book_code]['stok'] += 1
    data['loan_active'][book_code].remove(member_code)
    
    if not data['loan_active'][book_code]:
        del data['loan_active'][book_code]
        
    print(f"\nEntri pinjaman untuk '{book['judul']}' oleh {member['nama']} berhasil dihapus dan dicatat ke riwayat.")
    save_all_data(data)

# --- READ TRANSAKSI (View Peminjam Aktif) ---

def view_loan_list():
    """Menampilkan daftar semua buku yang sedang dipinjam (pinjaman aktif)."""
    clear_screen()
    print('='*10, 'DAFTAR PEMINJAM AKTIF', '='*10)
    
    data = get_all_data()
    
    if not data['loan_active']:
        print("Tidak ada buku yang sedang dipinjam saat ini.")
        return

    for book_code, member_list in data['loan_active'].items():
        book = data['book'].get(book_code, {'judul': '[Judul Tidak Ditemukan]', 'penulis': 'N/A'})
        
        print(f"Judul: {book['judul']}")
        print(f"Penulis: {book['penulis']}")
        print("Daftar Peminjam:")
        
        for i, member_code in enumerate(member_list, 1):
            member = data['member'].get(member_code, {'nama': 'Anggota Tidak Dikenal', 'jenis_anggota': 0})
            group_label = '(*NF Group)' if member['jenis_anggota'] == 1 else ''
            print(f"{i}. {member['nama']} {group_label} (Kode: {member_code})")
        print("-" * 30)