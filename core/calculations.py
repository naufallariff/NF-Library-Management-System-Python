def calculate_fine(member_type, days_late):
    """
    Menghitung total denda berdasarkan tipe anggota dan keterlambatan.
    Tipe 1 (NF Group) = Rp 1000/hari, Tipe 2 (Umum) = Rp 2500/hari.
    """
    
    # Menentukan tarif denda
    fine_per_day = 0
    if member_type == 1: # NF Group
        fine_per_day = 1000
    elif member_type == 2: # Umum
        fine_per_day = 2500

    # Menghitung denda (memastikan denda tidak negatif)
    total_fine = fine_per_day * max(0, days_late)
    
    # Menampilkan informasi denda di CLI
    print(f"Total Denda = Rp{total_fine:,} (Rp{fine_per_day}/hari x {days_late} hari)")
    if total_fine > 0:
        print("Silakan membayar denda keterlambatan di kasir.")
        
    return total_fine