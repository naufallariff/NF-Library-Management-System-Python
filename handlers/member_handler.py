from core.data_manager import get_all_data, save_all_data
from core.utils import generate_member_code, clear_screen
from core.validation import validate_input_str, search_and_select

# Helper untuk Anggota (Cari & Pilih)
def _prompt_and_select_member(data):
    """Membantu pengguna mencari dan memilih anggota berdasarkan kata kunci."""
    
    key_attr = 'nama'
    search_prompt = "Cari Nama Anggota (atau 'X' untuk batal): "
    not_found_msg = "Anggota tidak ditemukan."
    
    # Mengakses data member dari dictionary data
    code = search_and_select(data['member'], key_attr, search_prompt, not_found_msg)
    
    if code is None:
        return None, None
        
    return code, data['member'].get(code)

# --- CREATE ---
def create_member():
    """Menambahkan anggota baru ke sistem."""
    clear_screen()
    print('\n*** PENDAFTARAN ANGGOTA BARU ***')
    
    member_name = validate_input_str('Masukkan Nama: ')
    data = get_all_data()
    
    while True:
        nf_group_input = input('Apakah karyawan NF Group? (Y/T, X untuk batal): ').upper()
        if nf_group_input == 'Y':
            member_type = 1
            break
        elif nf_group_input == 'T':
            member_type = 2
            break
        elif nf_group_input == 'X':
            print('Operasi dibatalkan.')
            return
        else:
            print('Pilihan tidak valid. Gunakan (Y/T), atau (X) untuk batal.')

    member_code = generate_member_code()
    data['member'][member_code] = {'nama': member_name, 'jenis_anggota': member_type}
    
    save_all_data(data)
    print(f'Pendaftaran berhasil: {member_name} dengan kode {member_code}.')

# --- READ ---
def view_member_list():
    """Menampilkan daftar semua anggota."""
    clear_screen()
    print('='*10, 'DAFTAR ANGGOTA', '='*10)
    member_data = get_all_data()['member']
    
    if not member_data:
        print("Tidak ada data anggota ditemukan.")
        return

    for code, member in member_data.items():
        group_info = "NF Group" if member['jenis_anggota'] == 1 else "Anggota Umum"
        print(f"Kode: {code}")
        print(f"Nama: {member['nama']}")
        print(f"Grup: {group_info}")
        print("-" * 30)

# --- UPDATE ---
def update_member():
    """Memperbarui data anggota yang sudah ada."""
    clear_screen()
    print('\n*** EDIT DATA ANGGOTA ***')
    data = get_all_data()

    member_code, member = _prompt_and_select_member(data)
    if not member: return

    print(f"\n--- Mengedit Anggota: {member['nama']} ({member_code}) ---")

    # Edit Nama
    new_name = input(f"Nama Baru (Kosongkan untuk tetap '{member['nama']}'): ").strip()
    if new_name:
        member['nama'] = new_name

    # Edit Jenis Anggota
    while True:
        current_group = 'NF Group' if member['jenis_anggota'] == 1 else 'Anggota Umum'
        group_input = input(f"Grup Baru (1: NF, 2: Umum, Kosongkan untuk tetap '{current_group}'): ").strip()

        if not group_input:
            break
        elif group_input == '1' or group_input == '2':
            member['jenis_anggota'] = int(group_input)
            break
        else:
            print("Pilihan tidak valid. Masukkan 1 atau 2.")

    save_all_data(data)
    print(f"\nData Anggota {member_code} berhasil diperbarui.")

# --- DELETE ---
def delete_member():
    """Menghapus anggota, dengan pengecekan konflik pinjaman aktif."""
    clear_screen()
    print('\n*** HAPUS DATA ANGGOTA ***')
    data = get_all_data()

    member_code, member = _prompt_and_select_member(data)
    if not member: return

    # Cek Konflik: Anggota tidak boleh dihapus jika masih meminjam buku
    is_borrowing = False
    for borrower_list in data['loan_active'].values():
        if member_code in borrower_list:
            is_borrowing = True
            break
            
    if is_borrowing:
        print(f"\n[KONFLIK] Anggota {member['nama']} masih meminjam buku. Tidak dapat dihapus!")
        return

    confirmation = input(f"Konfirmasi penghapusan anggota {member['nama']} ({member_code})? (Y/T): ").upper()
    if confirmation == 'Y':
        del data['member'][member_code]
        save_all_data(data)
        print(f"\nAnggota {member_code} berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")