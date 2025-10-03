import random
import string
import os

from .data_manager import get_all_data

def clear_screen():
    """Membersihkan tampilan terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_member_code():
    """Membuat kode anggota unik (ANGXXX)."""
    member_data = get_all_data()['member']
    while True:
        code = "ANG" + ''.join(random.choice(string.digits) for _ in range(3))
        if code not in member_data:
            return code

def generate_book_code(author_name):
    """Membuat kode buku unik berdasarkan inisial penulis (AAAXXX)."""
    book_data = get_all_data()['book']
    # Ambil 3 huruf pertama non-spasi dari nama penulis
    initials = author_name.replace(" ", "")[:3].upper()
    while True:
        code = initials + ''.join(random.choice(string.digits) for _ in range(3))
        if code not in book_data:
            return code