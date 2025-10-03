import sys
import signal 

# Import fungsi dari handlers yang berbeda
from handlers.anggota_handler import (
    create_anggota, update_anggota, delete_anggota, view_anggota_list
)
from handlers.buku_handler import (
    create_buku, update_buku, delete_buku, view_buku_list
)
from handlers.transaction_handler import (
    create_loan, complete_return, delete_loan_entry, view_loan_list
)

from core.utils import clear_screen # clear_screen dari core/utils

# Handler untuk interupsi keyboard (Ctrl+C)
def signal_handler(sig, frame):
    """Cleanly exits the application upon Ctrl+C interrupt."""
    print('\n[APPLICATION STOPPED] Ctrl+C detected. Goodbye.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def menu():
    clear_screen()
    while True:
        print('\n***** NF LIBRARY MANAGEMENT SYSTEM (Modular) *****')
        print('MENU:')
        print('--- [ ANGGOTA ] ---')
        print('[1] Create New Member (C)')
        print('[2] Edit Member Data (U)')
        print('[3] Delete Member (D)')
        print('[4] View Member List (R)')
        print('--- [ BUKU ] ---')
        print('[5] Create New Book (C)')
        print('[6] Edit Book Data (U)')
        print('[7] Delete Book (D)')
        print('[8] View Book List (R)')
        print('--- [ TRANSAKSI ] ---')
        print('[A] Create Loan (Pinjam)')
        print('[B] Complete Return (Kembalikan)')
        print('[C] Delete Loan Entry (Forced Return)')
        print('[D] View Active Loans (R)')
        print('--- [ SISTEM ] ---')
        print('[S] Clear Screen')
        print('[X] Exit Application')
        
        try:
            pilih_menu = input('Enter Menu Choice: ').strip().upper()
            
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
            elif pilih_menu == 'S': clear_screen(); continue
            elif pilih_menu == 'X':
                print('Thank you for using the system. Have a good day!')
                break
            else:
                print('Invalid choice. Please try again.')
                
            input("\nPress ENTER to return to the menu...")
            clear_screen()

        except Exception as e:
            # Catching general errors from all handlers
            print(f"An unexpected application error occurred: {e}")
            input("\nPress ENTER to return to the menu...")
            clear_screen()

if __name__ == "__main__":
    menu()