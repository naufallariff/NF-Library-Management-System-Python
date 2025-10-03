def validate_input_int(prompt, min_val=0):
    """Memvalidasi input pengguna sebagai integer positif."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                # Mengizinkan pengguna untuk membatalkan proses dengan input kosong jika diperlukan
                # Tapi untuk input nilai numerik (stok, hari), kita anggap ini error.
                raise ValueError("Input tidak boleh kosong.")
                
            int_value = int(value)
            if int_value < min_val:
                raise ValueError(f"Nilai harus lebih besar atau sama dengan {min_val}.")
            return int_value
        except ValueError as e:
            print(f"Input tidak valid: {e}. Silakan coba lagi.")

def validate_input_str(prompt):
    """Memvalidasi input pengguna sebagai string non-kosong."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input tidak boleh kosong. Silakan coba lagi.")

def search_and_select(data_dict, key_attr, search_prompt, not_found_msg):
    """
    Memungkinkan pengguna mencari item (buku/anggota) berdasarkan string 
    (nama/judul) dan memilih kode unik dari hasil yang difilter.
    """
    while True:
        search_term = validate_input_str(search_prompt).lower()
        if search_term.upper() == 'X':
            return None # Batal

        filtered_results = {
            kode: item for kode, item in data_dict.items() 
            if search_term in item[key_attr].lower()
        }

        if not filtered_results:
            print(not_found_msg)
            print("Coba kata kunci lain, atau masukkan 'X' untuk batal.")
            continue

        print("\nHasil Pencarian:")
        results_list = list(filtered_results.keys())
        for i, kode in enumerate(results_list, 1):
            item = filtered_results[kode]
            print(f"[{i}] Kode: {kode} | {key_attr.capitalize()}: {item[key_attr]}")
        
        print("\n[X] Batal")
        choice = input("Pilih nomor item atau masukkan Kode (ANGXXX/AAAXXX) langsung: ").strip()

        if choice.upper() == 'X':
            return None
        
        # Opsi 1: Memilih berdasarkan nomor urut hasil filter
        try:
            index = int(choice) - 1
            if 0 <= index < len(results_list):
                return results_list[index]
        except ValueError:
            # Opsi 2: Memasukkan Kode unik langsung
            if choice.upper() in data_dict:
                return choice.upper()

        print("Pilihan tidak valid. Silakan coba lagi.")