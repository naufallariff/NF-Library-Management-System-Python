import random
import string
import os

from .data_manager import get_all_data 

def clear_screen():
    """Membersihkan layar terminal. Ditempatkan di sini karena ini adalah utilitas umum."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_kode_anggota():
    """Menghasilkan kode anggota unik (ANGXXX)."""
    anggota_data = get_all_data()['anggota']
    while True:
        kode = "ANG" + ''.join(random.choice(string.digits) for _ in range(3))
        if kode not in anggota_data:
            return kode

def generate_kode_buku(penulis):
    """Menghasilkan kode buku unik berdasarkan inisial penulis (AAAXXX)."""
    buku_data = get_all_data()['buku']
    inisial = penulis.replace(" ", "")[:3].upper()
    while True:
        kode = inisial + ''.join(random.choice(string.digits) for _ in range(3))
        if kode not in buku_data:
            return kode