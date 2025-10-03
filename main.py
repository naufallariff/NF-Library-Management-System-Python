import sys
import signal 

from handlers.anggota_handler import (
    create_anggota, update_anggota, delete_anggota, view_anggota_list
)
from handlers.buku_handler import (
    create_buku, update_buku, delete_buku, view_buku_list
)
from handlers.transaction_handler import (
    create_loan, complete_return, delete_loan_entry, view_loan_list
)
from handlers.history_handler import view_history_list 

from core.utils import clear_screen 

def signal_handler(sig, frame):
    """Cleanly exits the application upon Ctrl+C interrupt."""
    print('\n\n======================================================')
    print('|| APLIKASI DIHENTIKAN. Terima kasih atas kunjungan Anda! ||')
    print('======================================================')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def print_menu_header(title):
    """Mencetak header menu dengan desain yang lebih baik."""
    print('\n' + "="*50)
    print(f"| {title.center(46)} |")
    print("="*50)

def menu():
    clear_screen()
    while True:
        print_menu_header("NF LIBRARY MANAGEMENT SYSTEM (MODULAR)")
        
        print('| --- [ MANAJEMEN ANGGOTA (MEMBER CRUD) ] ---          |')
        print('| [1] Buat Anggota Baru (Create)                       |')
        print('| [2] Edit Data Anggota (Update)                       |')
        print('| [3] Hapus Anggota (Delete)                           |')
        print('| [4] Lihat Daftar Anggota (Read)                      |')
        print('|' + '-'*48 + '|')
        print('| --- [ MANAJEMEN BUKU (BOOK CRUD) ] ---               |')
        print('| [5] Buat Buku Baru (Create)                          |')
        print('| [6] Edit Data Buku (Update)                          |')
        print('| [7] Hapus Buku (Delete)                              |')
        print('| [8] Lihat Daftar Buku (Read)                         |')
        print('|' + '-'*48 + '|')
        print('| --- [ TRANSAKSI & RIWAYAT ] ---                      |')
        print('| [A] Buat Pinjaman (Loan)                             |')
        print('| [B] Selesaikan Pengembalian (Return)                 |')
        print('| [C] Hapus Entri Pinjaman (Forced Return)             |')
        print('| [D] Lihat Pinjaman Aktif                             |')
        print('| [E] Lihat Riwayat Transaksi (History)                |') 
        print('|' + '-'*48 + '|')
        print('| --- [ SISTEM ] ---                                   |')
        print('| [S] Clear Screen                                     |')
        print('| [X] KELUAR APLIKASI                                  |')
        print("="*50)
        
        try:
            pilih_menu = input('>>> Masukkan Pilihan Menu Anda: ').strip().upper()
            
            # Pilihan Angka (Anggota & Buku)
            if pilih_menu == '1': create_anggota()
            elif pilih_menu == '2': update_anggota()
            elif pilih_menu == '3': delete_anggota()
            elif pilih_menu == '4': view_anggota_list()
            elif pilih_menu == '5': create_buku()
            elif pilih_menu == '6': update_buku()
            elif pilih_menu == '7': delete_buku()
            elif pilih_menu == '8': view_buku_list()
            
            # Pilihan Huruf (Transaksi & Sistem)
            elif pilih_menu == 'A': create_loan()
            elif pilih_menu == 'B': complete_return()
            elif pilih_menu == 'C': delete_loan_entry()
            elif pilih_menu == 'D': view_loan_list()
            elif pilih_menu == 'E': view_history_list()
            elif pilih_menu == 'S': clear_screen(); continue
            elif pilih_menu == 'X':
                print('\nSistem sedang dimatikan...')
                break
            else:
                print('\n[WARNING] Pilihan tidak valid. Silakan coba lagi.')
                
            input("\nTekan ENTER untuk kembali ke menu...")
            clear_screen()

        except Exception as e:
            print(f"\n[ERROR FATAL] Terjadi kesalahan aplikasi yang tidak terduga: {e}")
            input("\nTekan ENTER untuk kembali ke menu...")
            clear_screen()

if __name__ == "__main__":
    menu()