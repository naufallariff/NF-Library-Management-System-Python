from core.data_manager import get_all_data, save_all_data
from core.utils import generate_kode_anggota, clear_screen
from core.validation import validate_input_str, search_and_select

# Helper untuk Anggota (Cari & Pilih)
def _prompt_and_select_anggota(data):
    """Membantu pengguna mencari dan memilih anggota berdasarkan kata kunci."""
    
    key_attr = 'nama'
    search_prompt = "Cari Nama Anggota (atau 'X' untuk batal): "
    not_found_msg = "Anggota tidak ditemukan."
        
    kode = search_and_select(data['anggota'], key_attr, search_prompt, not_found_msg)
    
    if kode is None:
        return None, None
        
    return kode, data['anggota'].get(kode)

# --- CREATE ---
def create_anggota():
    """Menambahkan anggota baru ke sistem."""
    clear_screen()
    print('\n*** PENDAFTARAN ANGGOTA BARU ***')
    
    nama = validate_input_str('Masukkan Nama: ')
    data = get_all_data()
    
    while True:
        nf_grup_input = input('Karyawan NF Group? (Y/T, X untuk batal): ').upper()
        if nf_grup_input == 'Y':
            jenis_anggota = 1
            break
        elif nf_grup_input == 'T':
            jenis_anggota = 2
            break
        elif nf_grup_input == 'X':
            print('Operation cancelled.')
            return
        else:
            print('Invalid choice. Use (Y/T), or (X) to cancel.')

    kode_anggota = generate_kode_anggota()
    data['anggota'][kode_anggota] = {'nama': nama, 'jenis_anggota': jenis_anggota}
    
    save_all_data(data)
    print(f'Registration successful: {nama} with code {kode_anggota}.')

# --- READ ---
def view_anggota_list():
    """Menampilkan daftar semua anggota."""
    clear_screen()
    print('='*10, 'DAFTAR ANGGOTA', '='*10)
    anggota_data = get_all_data()['anggota']
    
    if not anggota_data:
        print("No member data found.")
        return

    for kode, data in anggota_data.items():
        grup_info = "NF Group" if data['jenis_anggota'] == 1 else "Public Member"
        print(f"Kode: {kode}")
        print(f"Nama: {data['nama']}")
        print(f"Grup: {grup_info}")
        print("-" * 30)

# --- UPDATE ---
def update_anggota():
    """Memperbarui data anggota yang sudah ada."""
    clear_screen()
    print('\n*** EDIT DATA ANGGOTA ***')
    data = get_all_data()

    kode_anggota, anggota = _prompt_and_select_anggota(data)
    if not anggota: return

    print(f"\n--- Editing Member: {anggota['nama']} ({kode_anggota}) ---")

    # Edit Nama
    new_nama = input(f"New Name (Leave blank for '{anggota['nama']}'): ").strip()
    if new_nama:
        anggota['nama'] = new_nama

    # Edit Jenis Anggota
    while True:
        current_grup = 'NF Group' if anggota['jenis_anggota'] == 1 else 'Public Member'
        grup_input = input(f"New Group (1: NF, 2: Public, Blank for '{current_grup}'): ").strip()

        if not grup_input:
            break
        elif grup_input == '1' or grup_input == '2':
            anggota['jenis_anggota'] = int(grup_input)
            break
        else:
            print("Invalid choice. Enter 1 or 2.")

    save_all_data(data)
    print(f"\nMember data {kode_anggota} successfully updated.")

# --- DELETE ---
def delete_anggota():
    """Menghapus anggota, dengan cek konflik peminjaman."""
    clear_screen()
    print('\n*** HAPUS DATA ANGGOTA ***')
    data = get_all_data()

    kode_anggota, anggota = _prompt_and_select_anggota(data)
    if not anggota: return

    # Cek Konflik: Anggota tidak boleh dihapus jika masih meminjam buku
    is_borrowing = False
    for peminjam_list in data['peminjaman'].values():
        if kode_anggota in peminjam_list:
            is_borrowing = True
            break
            
    if is_borrowing:
        print(f"\n[CONFLICT] Member {anggota['nama']} masih memiliki pinjaman buku. Tidak bisa dihapus sekarang!")
        return

    konfirmasi = input(f"Confirm deletion of {anggota['nama']} ({kode_anggota})? (Y/T): ").upper()
    if konfirmasi == 'Y':
        del data['anggota'][kode_anggota]
        save_all_data(data)
        print(f"\nMember {kode_anggota} successfully deleted.")
    else:
        print("Deletion cancelled.")