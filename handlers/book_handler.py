from core.data_manager import get_all_data, save_all_data
from core.utils import generate_book_code, clear_screen
from core.validation import validate_input_str, validate_input_int, search_and_select

# Helper untuk Buku (Cari & Pilih)
def _prompt_and_select_book(data):
    """Membantu pengguna mencari dan memilih buku berdasarkan kata kunci."""
    
    key_attr = 'judul'
    search_prompt = "Cari Judul Buku (atau 'X' untuk batal): "
    not_found_msg = "Buku tidak ditemukan."
        
    # Mengakses data book dari dictionary data
    code = search_and_select(data['book'], key_attr, search_prompt, not_found_msg)
    
    if code is None:
        return None, None
        
    return code, data['book'].get(code)

# --- CREATE ---
def create_book():
    """Menambahkan buku baru ke koleksi."""
    clear_screen()
    print('\n*** PENAMBAHAN BUKU BARU ***')
    
    title = validate_input_str('Judul: ')
    author = validate_input_str('Penulis: ')
    stock = validate_input_int('Stok: ')
    
    data = get_all_data()
    book_code = generate_book_code(author)
    
    print(f"\nKonfirmasi Buku (Kode: {book_code}, Judul: {title}, Stok: {stock})?")
    confirmation = input("(Y/T): ").upper()
    
    if confirmation == "Y":
        data['book'][book_code] = {'judul': title, 'penulis': author, 'stok': stock}
        save_all_data(data) 
        print(f'Buku berhasil ditambahkan: {title} dengan kode {book_code}.')
    else:
        print('Operasi dibatalkan.')

# --- READ ---
def view_book_list():
    """Menampilkan daftar semua buku."""
    clear_screen()
    print('='*10, 'DAFTAR BUKU', '='*10)
    book_data = get_all_data()['book']
    
    if not book_data:
        print("Tidak ada data buku ditemukan.")
        return

    for code, book in book_data.items():
        print(f"Kode: {code}")
        print(f"Judul: {book['judul']}")
        print(f"Penulis: {book['penulis']}")
        print(f"Stok: {book['stok']}")
        print("-" * 30)

# --- UPDATE ---
def update_book():
    """Memperbarui data buku yang sudah ada."""
    clear_screen()
    print('\n*** EDIT DATA BUKU ***')
    data = get_all_data()

    book_code, book = _prompt_and_select_book(data)
    if not book: return

    print(f"\n--- Mengedit Buku: {book['judul']} ({book_code}) ---")

    # Edit Judul
    new_title = input(f"Judul Baru (Kosongkan untuk tetap '{book['judul']}'): ").strip()
    if new_title:
        book['judul'] = new_title

    # Edit Penulis
    new_author = input(f"Penulis Baru (Kosongkan untuk tetap '{book['penulis']}'): ").strip()
    if new_author:
        book['penulis'] = new_author

    # Edit Stok
    while True:
        stock_input = input(f"Stok Baru (Kosongkan untuk tetap '{book['stok']}'): ").strip()
        if not stock_input:
            break
        try:
            new_stock = int(stock_input)
            if new_stock >= 0:
                book['stok'] = new_stock
                break
            else:
                print("Stok harus berupa angka non-negatif.")
        except ValueError:
            print("Input stok tidak valid.")

    save_all_data(data)
    print(f"\nData Buku {book_code} berhasil diperbarui.")

# --- DELETE ---
def delete_book():
    """Menghapus buku, dengan pengecekan konflik pinjaman aktif."""
    clear_screen()
    print('\n*** HAPUS DATA BUKU ***')
    data = get_all_data()

    book_code, book = _prompt_and_select_book(data)
    if not book: return

    # Cek Konflik: Buku tidak boleh dihapus jika masih dipinjam
    if book_code in data['loan_active'] and data['loan_active'][book_code]:
        num_borrowers = len(data['loan_active'][book_code])
        print(f"\n[KONFLIK] Buku '{book['judul']}' masih dipinjam oleh {num_borrowers} anggota. Tidak dapat dihapus!")
        return

    confirmation = input(f"Konfirmasi penghapusan '{book['judul']}' ({book_code})? (Y/T): ").upper()
    if confirmation == 'Y':
        # Membersihkan entri buku dari pinjaman aktif jika ada tetapi daftarnya kosong
        if book_code in data['loan_active']:
            del data['loan_active'][book_code] 
            
        del data['book'][book_code]
        save_all_data(data)
        print(f"\nBuku {book_code} berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")