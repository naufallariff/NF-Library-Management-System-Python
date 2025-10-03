from core.data_manager import get_all_data, save_all_data
from core.utils import generate_kode_buku, clear_screen
from core.validation import validate_input_str, validate_input_int

# Helper untuk Buku (Cari & Pilih)
def _prompt_and_select_buku(data):
    """Membantu pengguna mencari dan memilih buku berdasarkan kata kunci."""
    from core.validation import search_and_select 
    
    key_attr = 'judul'
    search_prompt = "Cari Judul Buku (atau 'X' untuk batal): "
    not_found_msg = "Buku tidak ditemukan."
        
    kode = search_and_select(data['buku'], key_attr, search_prompt, not_found_msg)
    
    if kode is None:
        return None, None
        
    return kode, data['buku'].get(kode)

# --- CREATE ---
def create_buku():
    """Menambahkan buku baru ke koleksi."""
    clear_screen()
    print('\n*** PENAMBAHAN BUKU BARU ***')
    
    judul = validate_input_str('Judul: ')
    penulis = validate_input_str('Penulis: ')
    stok = validate_input_int('Stok: ')
    
    data = get_all_data()
    kode_buku = generate_kode_buku(penulis)
    
    print(f"\nKonfirmasi Buku (Kode: {kode_buku}, Judul: {judul}, Stok: {stok})?")
    yakin = input("(Y/T): ").upper()
    
    if yakin == "Y":
        data['buku'][kode_buku] = {'judul': judul, 'penulis': penulis, 'stok': stok}
        save_all_data(data) # TYPO DIBENERKAN DI SINI
        print(f'Book added successfully: {judul} with code {kode_buku}.')
    else:
        print('Operation cancelled.')

# --- READ ---
def view_buku_list():
    """Menampilkan daftar semua buku."""
    clear_screen()
    print('='*10, 'DAFTAR BUKU', '='*10)
    buku_data = get_all_data()['buku']
    
    if not buku_data:
        print("No book data found.")
        return

    for kode, data in buku_data.items():
        print(f"Kode: {kode}")
        print(f"Judul: {data['judul']}")
        print(f"Penulis: {data['penulis']}")
        print(f"Stok: {data['stok']}")
        print("-" * 30)

# --- UPDATE ---
def update_buku():
    """Memperbarui data buku yang sudah ada."""
    clear_screen()
    print('\n*** EDIT DATA BUKU ***')
    data = get_all_data()

    kode_buku, buku = _prompt_and_select_buku(data)
    if not buku: return

    print(f"\n--- Editing Book: {buku['judul']} ({kode_buku}) ---")

    # Edit Judul
    new_judul = input(f"New Title (Blank for '{buku['judul']}'): ").strip()
    if new_judul:
        buku['judul'] = new_judul

    # Edit Penulis
    new_penulis = input(f"New Author (Blank for '{buku['penulis']}'): ").strip()
    if new_penulis:
        buku['penulis'] = new_penulis

    # Edit Stok
    while True:
        stok_input = input(f"New Stock (Blank for '{buku['stok']}'): ").strip()
        if not stok_input:
            break
        try:
            new_stok = int(stok_input)
            if new_stok >= 0:
                buku['stok'] = new_stok
                break
            else:
                print("Stock must be a non-negative number.")
        except ValueError:
            print("Invalid stock input.")

    save_all_data(data)
    print(f"\nBook data {kode_buku} successfully updated.")

# --- DELETE ---
def delete_buku():
    """Menghapus buku, dengan cek konflik peminjaman aktif."""
    clear_screen()
    print('\n*** HAPUS DATA BUKU ***')
    data = get_all_data()

    kode_buku, buku = _prompt_and_select_buku(data)
    if not buku: return

    # Cek Konflik: Buku tidak boleh dihapus jika masih dipinjam
    if kode_buku in data['peminjaman'] and data['peminjaman'][kode_buku]:
        num_borrowers = len(data['peminjaman'][kode_buku])
        print(f"\n[CONFLICT] Book '{buku['judul']}' is currently borrowed by {num_borrowers} members. Cannot delete!")
        return

    konfirmasi = input(f"Confirm deletion of '{buku['judul']}' ({kode_buku})? (Y/T): ").upper()
    if konfirmasi == 'Y':
        # Bersihkan entri dari peminjaman.json jika ada tetapi kosong
        if kode_buku in data['peminjaman']:
            del data['peminjaman'][kode_buku] 
            
        del data['buku'][kode_buku]
        save_all_data(data)
        print(f"\nBook {kode_buku} successfully deleted.")
    else:
        print("Deletion cancelled.")