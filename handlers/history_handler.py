from core.data_manager import get_all_data
from core.utils import clear_screen

def view_history_list():
    """Menampilkan daftar riwayat peminjaman yang sudah selesai."""
    clear_screen()
    
    print("=" * 60)
    print(f"|{'RIWAYAT TRANSAKSI PEMINJAMAN (HISTORY)'.center(58)}|")
    print("=" * 60)
    
    data = get_all_data()
    history_data = data['loan_history']
    
    if not history_data:
        print("\n[INFO] Belum ada catatan riwayat peminjaman yang selesai.")
        return

    # Mengurutkan riwayat berdasarkan ID (yang berbasis timestamp) secara descending untuk menampilkan yang terbaru
    recent_history = list(history_data.items())
    recent_history.sort(key=lambda item: item[0], reverse=True)
    
    # Hanya menampilkan 15 transaksi terakhir untuk kemudahan CLI
    print(f"\nMenampilkan {min(15, len(recent_history))} catatan transaksi terakhir:")
    print("-" * 60)
    
    for history_id, record in recent_history[:15]: 
        book = data['book'].get(record['book_code'], {'judul': '[Buku Hilang]', 'penulis': 'N/A'})
        member = data['member'].get(record['member_code'], {'nama': '[Anggota Nonaktif]'})
        
        # Format tampilan
        print(f"| ID: {history_id.ljust(15)} | Tanggal Selesai: {record.get('completed_date', 'N/A')}")
        print(f"| Buku: {book['judul'][:35].ljust(35)} | Kode: {record['book_code']}")
        print(f"| Anggota: {member['nama'][:30].ljust(30)} | Kode: {record['member_code']}")
        
        # Menggunakan koma untuk format ribuan
        fine_formatted = f"Rp{record['fine_paid']:,}".replace(",", ".") 
        print(f"| Denda Dibayar: {fine_formatted.ljust(20)} (Terlambat: {record['days_late']} hari)")
        
        if record.get('notes'):
            print(f"| Catatan: {record['notes']}")
        print("-" * 60)