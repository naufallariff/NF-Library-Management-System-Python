from data_manager import get_all_data, save_all_data
from utils import generate_kode_anggota, generate_kode_buku, clear_screen
from validation import validate_input_str, validate_input_int, search_and_select
from calculations import calculate_fine

# --- HELPER VALIDASI DATA INTI ---

def _get_entity(data, entity_type, kode):
    """Helper untuk mendapatkan entitas dan menangani kasus tidak ditemukan."""
    entity = data.get(entity_type, {}).get(kode)
    if not entity:
        print(f"Kode {entity_type} '{kode}' tidak ditemukan. Proses gagal.")
    return entity

def _prompt_and_select_entity(data, entity_type):
    """
    Fungsi gabungan untuk menangani UX pencarian dan pemilihan.
    Menghilangkan kesulitan memasukkan kode random.
    """
    if entity_type == 'anggota':
        key_attr = 'nama'
        search_prompt = "Cari Nama Anggota (atau 'X' untuk batal): "
        not_found_msg = "Anggota tidak ditemukan."
    else: # buku
        key_attr = 'judul'
        search_prompt = "Cari Judul Buku (atau 'X' untuk batal): "
        not_found_msg = "Buku tidak ditemukan."
        
    kode = search_and_select(data[entity_type], key_attr, search_prompt, not_found_msg)
    
    if kode is None:
        return None, None
        
    return kode, data[entity_type].get(kode)

# --- FITUR CORE: TAMBAH ---

def tambah_anggota():
    """Fitur 1: Menambahkan anggota baru."""
    clear_screen()
    print('\n*** PENDAFTARAN ANGGOTA BARU ***')
    
    nama = validate_input_str('Masukkan Nama: ')
    data = get_all_data()
    
    while True:
        nf_grup_input = input('Apakah merupakan karyawan NF Group? (Y/T, X untuk batal): ').upper()
        if nf_grup_input == 'Y':
            jenis_anggota = 1
            break
        elif nf_grup_input == 'T':
            jenis_anggota = 2
            break
        elif nf_grup_input == 'X':
            print('Penambahan Anggota Batal.')
            return
        else:
            print('INVALID! Pilih (Y/T) atau (X) untuk batal.')

    kode_anggota = generate_kode_anggota()
    data['anggota'][kode_anggota] = {'nama': nama, 'jenis_anggota': jenis_anggota}
    
    save_all_data(data)
    print(f'Pendaftaran Anggota dengan kode {kode_anggota} atas nama {nama} berhasil!')

def tambah_buku():
    """Fitur 2: Menambahkan buku baru."""
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
        save_all_data(data)
        print(f'Penambahan buku baru dengan kode {kode_buku} dan judul {judul} berhasil.')
    else:
        print('Penambahan buku dibatalkan.')

# --- FITUR CORE: UPDATE (Edit) ---

def edit_anggota():
    clear_screen()
    print('\n*** EDIT DATA ANGGOTA ***')
    data = get_all_data()

    kode_anggota, anggota = _prompt_and_select_entity(data, 'anggota')
    if not anggota: return

    print(f"\n--- Mengedit Anggota: {anggota['nama']} ({kode_anggota}) ---")

    # 1. Edit Nama
    new_nama = input(f"Nama Baru (Kosongkan untuk tetap '{anggota['nama']}'): ").strip()
    if new_nama:
        anggota['nama'] = new_nama

    # 2. Edit Jenis Anggota
    while True:
        current_grup = 'NF Group' if anggota['jenis_anggota'] == 1 else 'Umum'
        grup_input = input(f"Grup Baru (1: NF, 2: Umum, Kosongkan untuk tetap '{current_grup}'): ").strip()

        if not grup_input:
            break
        elif grup_input == '1' or grup_input == '2':
            anggota['jenis_anggota'] = int(grup_input)
            break
        else:
            print("Pilihan tidak valid. Masukkan 1 atau 2.")

    save_all_data(data)
    print(f"\nData Anggota {kode_anggota} berhasil diperbarui.")

def edit_buku():
    clear_screen()
    print('\n*** EDIT DATA BUKU ***')
    data = get_all_data()

    kode_buku, buku = _prompt_and_select_entity(data, 'buku')
    if not buku: return

    print(f"\n--- Mengedit Buku: {buku['judul']} ({kode_buku}) ---")

    # 1. Edit Judul
    new_judul = input(f"Judul Baru (Kosongkan untuk tetap '{buku['judul']}'): ").strip()
    if new_judul:
        buku['judul'] = new_judul

    # 2. Edit Penulis
    new_penulis = input(f"Penulis Baru (Kosongkan untuk tetap '{buku['penulis']}'): ").strip()
    if new_penulis:
        buku['penulis'] = new_penulis

    # 3. Edit Stok (Menggunakan validation.py untuk memastikan integer)
    while True:
        stok_input = input(f"Stok Baru (Kosongkan untuk tetap '{buku['stok']}'): ").strip()
        if not stok_input:
            break
        try:
            new_stok = int(stok_input)
            if new_stok >= 0:
                buku['stok'] = new_stok
                break
            else:
                print("Stok harus berupa angka positif.")
        except ValueError:
            print("Input stok tidak valid.")

    save_all_data(data)
    print(f"\nData Buku {kode_buku} berhasil diperbarui.")

# --- FITUR CORE: DELETE (Hapus) ---

def delete_anggota():
    clear_screen()
    print('\n*** HAPUS DATA ANGGOTA ***')
    data = get_all_data()

    kode_anggota, anggota = _prompt_and_select_entity(data, 'anggota')
    if not anggota: return

    # Konflik Check: Periksa apakah anggota masih meminjam buku
    is_borrowing = False
    for peminjam_list in data['peminjaman'].values():
        if kode_anggota in peminjam_list:
            is_borrowing = True
            break
            
    if is_borrowing:
        print(f"\n[KONFLIK DITEMUKAN] Anggota {anggota['nama']} masih meminjam buku. Tidak dapat dihapus!")
        return

    konfirmasi = input(f"Yakin ingin menghapus anggota {anggota['nama']} ({kode_anggota})? (Y/T): ").upper()
    if konfirmasi == 'Y':
        del data['anggota'][kode_anggota]
        save_all_data(data)
        print(f"\nAnggota {kode_anggota} berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

def delete_buku():
    clear_screen()
    print('\n*** HAPUS DATA BUKU ***')
    data = get_all_data()

    kode_buku, buku = _prompt_and_select_entity(data, 'buku')
    if not buku: return

    # 🚩 KONFLIK CHECK: Penanganan Konflik Penting
    if kode_buku in data['peminjaman'] and data['peminjaman'][kode_buku]:
        num_borrowers = len(data['peminjaman'][kode_buku])
        print(f"\n[KONFLIK DITEMUKAN] Buku '{buku['judul']}' masih dipinjam oleh {num_borrowers} anggota. Tidak dapat dihapus!")
        return

    konfirmasi = input(f"Yakin ingin menghapus buku '{buku['judul']}' ({kode_buku})? (Y/T): ").upper()
    if konfirmasi == 'Y':
        # Jika buku ada di peminjaman.json tetapi list-nya kosong, hapus entri tersebut
        if kode_buku in data['peminjaman']:
            del data['peminjaman'][kode_buku] 
            
        del data['buku'][kode_buku]
        save_all_data(data)
        print(f"\nBuku {kode_buku} berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

# --- FITUR CORE: TRANSAKSI (Dengan UX Baru) ---

def proses_pinjam_kembali(tipe_proses):
    """Fitur 3 & 4: Memproses peminjaman atau pengembalian buku (dengan UX pencarian)."""
    clear_screen()
    data = get_all_data()
    proses_nama = "PEMINJAMAN" if tipe_proses == 'pinjam' else "PENGEMBALIAN"
    print(f'\n*** {proses_nama} BUKU ***')
    
    # 1. Pilih Buku menggunakan UX pencarian
    print("\n[Pilih Buku]")
    kode_buku, buku = _prompt_and_select_entity(data, 'buku')
    if not buku: return

    # 2. Pilih Anggota menggunakan UX pencarian
    print("\n[Pilih Anggota]")
    kode_anggota, anggota = _prompt_and_select_entity(data, 'anggota')
    if not anggota: return
        
    # --- LOGIKA PINJAM --- (Logika internal sama, hanya cara input kode yang berubah)
    if tipe_proses == 'pinjam':
        if buku['stok'] <= 0:
            print(f"Stok buku '{buku['judul']}' kosong. Peminjaman gagal.")
            return
            
        peminjam_list = data['peminjaman'].get(kode_buku, [])
        if kode_anggota in peminjam_list:
            print(f"Anggota {anggota['nama']} sudah meminjam buku ini.")
            return

        buku['stok'] -= 1
        if kode_buku not in data['peminjaman']:
            data['peminjaman'][kode_buku] = []
        data['peminjaman'][kode_buku].append(kode_anggota)
        print(f"\nPeminjaman buku {buku['judul']} oleh {anggota['nama']} berhasil.")
        save_all_data(data)
    
    # --- LOGIKA KEMBALI --- (Logika internal sama)
    elif tipe_proses == 'kembali':
        peminjam_list = data['peminjaman'].get(kode_buku, [])
        if kode_anggota not in peminjam_list:
            print("Buku ini tidak sedang dipinjam oleh anggota tersebut. Pengembalian gagal.")
            return

        terlambat = validate_input_int("Keterlambatan pengembalian (hari, 0 jika tidak terlambat): ")
        
        calculate_fine(anggota['jenis_anggota'], terlambat) 

        buku['stok'] += 1
        data['peminjaman'][kode_buku].remove(kode_anggota)
        
        if not data['peminjaman'][kode_buku]:
            del data['peminjaman'][kode_buku]
            
        print(f"\nPengembalian buku {buku['judul']} oleh {anggota['nama']} berhasil.")
        save_all_data(data)
        
def hapus_transaksi():
    clear_screen()
    print('\n*** HAPUS TRANSAKSI PEMINJAMAN (PENGEMBALIAN PAKSA) ***')
    data = get_all_data()

    # 1. Pilih Buku yang sedang dipinjam
    borrowed_books_data = {
        k: data['buku'][k] for k in data['peminjaman'] if k in data['buku']
    }
    
    if not borrowed_books_data:
        print("Saat ini tidak ada buku yang sedang dipinjam.")
        return
    
    print("\n[Pilih Buku yang akan dikembalikan]")
    kode_buku = search_and_select(borrowed_books_data, 'judul', "Cari Judul Buku (atau 'X' untuk batal): ", "Buku tidak ditemukan.")
    if not kode_buku: return
    
    buku = data['buku'][kode_buku]
    peminjam_list = data['peminjaman'][kode_buku]

    # 2. Pilih Anggota
    current_borrowers = {
        k: data['anggota'][k] for k in peminjam_list if k in data['anggota']
    }
    
    print("\n[Pilih Anggota yang akan mengembalikan]")
    kode_anggota = search_and_select(current_borrowers, 'nama', "Cari Nama Anggota (atau 'X' untuk batal): ", "Anggota tidak ditemukan.")
    if not kode_anggota: return
    
    anggota = data['anggota'][kode_anggota]
    
    # 3. Proses Pengembalian
    terlambat = validate_input_int("Keterlambatan pengembalian (hari, 0 jika tidak terlambat): ")
    calculate_fine(anggota['jenis_anggota'], terlambat) 

    buku['stok'] += 1
    peminjam_list.remove(kode_anggota)
    
    if not peminjam_list:
        del data['peminjaman'][kode_buku]
        
    print(f"\nTransaksi pengembalian {buku['judul']} oleh {anggota['nama']} berhasil dihapus/diselesaikan.")
    save_all_data(data)

# --- FITUR VIEW ---

def lihat_daftar_peminjam():
    """Fitur 5: Menampilkan daftar peminjam."""
    clear_screen()
    print('='*10, 'DAFTAR PEMINJAM', '='*10)
    
    data = get_all_data()
    
    if not data['peminjaman']:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    for kode_buku, list_peminjam in data['peminjaman'].items():
        buku = data['buku'].get(kode_buku, {'judul': '[Judul Tidak Ditemukan]', 'penulis': 'N/A'})
        
        print(f"Judul: {buku['judul']}")
        print(f"Penulis: {buku['penulis']}")
        print("Daftar Peminjam:")
        
        for i, kode_anggota in enumerate(list_peminjam, 1):
            anggota = data['anggota'].get(kode_anggota, {'nama': 'Anggota Tidak Dikenal', 'jenis_anggota': 0})
            grup_label = '(*NF Group)' if anggota['jenis_anggota'] == 1 else ''
            print(f"{i}. {anggota['nama']} {grup_label} (Kode: {kode_anggota})")
        print("-" * 30)

def lihat_daftar_buku():
    """Fitur 6: Menampilkan daftar semua buku."""
    clear_screen()
    print('='*10, 'DAFTAR BUKU', '='*10)
    buku_data = get_all_data()['buku']
    
    if not buku_data:
        print("Tidak ada data buku.")
        return

    for kode, data in buku_data.items():
        print(f"Kode: {kode}")
        print(f"Judul: {data['judul']}")
        print(f"Penulis: {data['penulis']}")
        print(f"Stok: {data['stok']}")
        print("-" * 30)

def lihat_daftar_anggota():
    """Fitur 7: Menampilkan daftar anggota."""
    clear_screen()
    print('='*10, 'DAFTAR ANGGOTA', '='*10)
    anggota_data = get_all_data()['anggota']
    
    if not anggota_data:
        print("Tidak ada data anggota.")
        return

    for kode, data in anggota_data.items():
        grup_info = "NF Group" if data['jenis_anggota'] == 1 else "Masyarakat Umum"
        print(f"Kode Anggota: {kode}")
        print(f"Nama: {data['nama']}")
        print(f"Grup: {grup_info}")
        print("-" * 30)