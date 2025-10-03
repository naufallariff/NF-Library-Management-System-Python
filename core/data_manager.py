# core/data_manager.py (Diperbarui)

import json
import os

# Menentukan jalur file di dalam folder 'data/'
DATA_DIR = 'data'
ANGGOTA_FILE = os.path.join(DATA_DIR, 'anggota.json')
BUKU_FILE = os.path.join(DATA_DIR, 'buku.json')
PEMINJAMAN_FILE = os.path.join(DATA_DIR, 'peminjaman.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json') 

def load_data(filename):
    """Membaca data dari file JSON."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"[{os.path.basename(filename)}] Data file corrupted. Initializing empty dictionary.")
        return {}

def save_data(data, filename):
    """Menulis data ke file JSON."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save data to {os.path.basename(filename)}: {e}")

def get_all_data():
    """Mengambil semua data aplikasi dari disk, termasuk history."""
    return {
        'anggota': load_data(ANGGOTA_FILE),
        'buku': load_data(BUKU_FILE),
        'peminjaman': load_data(PEMINJAMAN_FILE),
        'history': load_data(HISTORY_FILE) 
    }

def save_all_data(data):
    """Menyimpan semua data aplikasi ke disk, termasuk history."""
    save_data(data['anggota'], ANGGOTA_FILE)
    save_data(data['buku'], BUKU_FILE)
    save_data(data['peminjaman'], PEMINJAMAN_FILE)
    save_data(data['history'], HISTORY_FILE)