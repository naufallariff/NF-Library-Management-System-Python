def calculate_fine(jenis_anggota, days_late):
    """Menghitung total denda berdasarkan jenis anggota dan keterlambatan."""
    
    # Menentukan tarif berdasarkan jenis anggota
    if jenis_anggota == 1: # NF Group
        denda_per_hari = 1000
    elif jenis_anggota == 2: # Umum
        denda_per_hari = 2500
    else:
        denda_per_hari = 0

    # Menghitung denda (pastikan tidak ada denda negatif)
    total_denda = denda_per_hari * max(0, days_late)
    
    # Menampilkan informasi denda
    print(f"Total Denda = {total_denda} (Rp {denda_per_hari}/hari x {days_late} hari)")
    if total_denda > 0:
        print("Silakan membayar denda keterlambatan di kasir.")
        
    return total_denda