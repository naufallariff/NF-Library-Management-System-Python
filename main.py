import sys
import signal 

# Import fungsi dari handlers yang berbeda
from handlers.member_handler import (
    create_member, update_member, delete_member, view_member_list
)
from handlers.book_handler import (
    create_book, update_book, delete_book, view_book_list
)
from handlers.transaction_handler import (
    create_loan, complete_return, delete_loan_entry, view_loan_list
)
from handlers.history_handler import view_history_list 

from core.utils import clear_screen 

def signal_handler(sig, frame):
    """Mengelola penekanan Ctrl+C (SIGINT) untuk keluar dengan rapi."""
    print('\n\n======================================================')
    print('|| APLIKASI DIHENTIKAN. Terima kasih atas kunjungan Anda! ||')
    print('======================================================')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def print_menu_header(title):
    """Mencetak header menu dengan desain CLI yang rapi."""
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
            pilihan_menu = input('>>> Masukkan Pilihan Menu Anda: ').strip().upper()
            
            # Pilihan Angka (Anggota & Buku)
            if pilihan_menu == '1': create_member()
            elif pilihan_menu == '2': update_member()
            elif pilihan_menu == '3': delete_member()
            elif pilihan_menu == '4': view_member_list()
            elif pilihan_menu == '5': create_book()
            elif pilihan_menu == '6': update_book()
            elif pilihan_menu == '7': delete_book()
            elif pilihan_menu == '8': view_book_list()
            
            # Pilihan Huruf (Transaksi & Sistem)
            elif pilihan_menu == 'A': create_loan()
            elif pilihan_menu == 'B': complete_return()
            elif pilihan_menu == 'C': delete_loan_entry()
            elif pilihan_menu == 'D': view_loan_list()
            elif pilihan_menu == 'E': view_history_list()
            elif pilihan_menu == 'S': clear_screen(); continue
            elif pilihan_menu == 'X':
                print('\nSistem dimatikan. Sampai jumpa!')
                break
            else:
                print('\n[WARNING] Pilihan tidak valid. Silakan coba lagi.')
                
            input("\nTekan ENTER untuk kembali ke menu...")
            clear_screen()

        except Exception as error:
            # Penanganan error global untuk menangkap error tak terduga dari modul-modul
            print(f"\n[ERROR FATAL] Terjadi kesalahan aplikasi yang tidak terduga: {error}")
            input("\nTekan ENTER untuk kembali ke menu...")
            clear_screen()

if __name__ == "__main__":
    menu()