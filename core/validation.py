def validate_input_int(prompt, min_val=0):
    """Memastikan input pengguna berupa angka (integer) dan nilainya valid."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                # Menangkap input kosong untuk input angka
                raise ValueError("Input tidak boleh kosong.")
                
            int_value = int(value)
            if int_value < min_val:
                # Memastikan nilai memenuhi batas minimum (misalnya, stok tidak negatif)
                raise ValueError(f"Nilai harus lebih besar atau sama dengan {min_val}.")
            return int_value
        except ValueError as error:
            print(f"Input tidak valid: {error}. Silakan coba lagi.")

def validate_input_str(prompt):
    """Memastikan input pengguna berupa string non-kosong."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input tidak boleh kosong. Silakan coba lagi.")

def search_and_select(data_dict, key_attr, search_prompt, not_found_msg):
    """
    Memungkinkan pengguna mencari item (buku/anggota) berdasarkan string 
    (nama/judul) dan memilih kode unik dari hasil yang difilter. Ini untuk UX yang lebih baik.
    """
    while True:
        # Mengambil input pencarian
        search_term = validate_input_str(search_prompt).lower()
        if search_term.upper() == 'X':
            return None # Batal

        # Filter hasil berdasarkan atribut kunci (nama/judul)
        filtered_results = {
            code: item for code, item in data_dict.items() 
            if search_term in item[key_attr].lower()
        }

        if not filtered_results:
            print(not_found_msg)
            print("Coba kata kunci lain, atau masukkan 'X' untuk batal.")
            continue

        # Menampilkan hasil
        print("\nHasil Pencarian:")
        results_list = list(filtered_results.keys())
        for i, code in enumerate(results_list, 1):
            item = filtered_results[code]
            print(f"[{i}] Kode: {code} | {key_attr.capitalize()}: {item[key_attr]}")
        
        # Opsi pemilihan
        print("\n[X] Batal")
        choice = input("Pilih nomor item atau masukkan Kode (ANGXXX/AAAXXX) langsung: ").strip()

        if choice.upper() == 'X':
            return None
        
        # Opsi 1: Memilih berdasarkan nomor urut
        try:
            index = int(choice) - 1
            if 0 <= index < len(results_list):
                return results_list[index]
        except ValueError:
            # Opsi 2: Memasukkan Kode unik langsung
            if choice.upper() in data_dict:
                return choice.upper()

        print("Pilihan tidak valid. Silakan coba lagi.")