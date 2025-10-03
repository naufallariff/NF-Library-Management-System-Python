import json
import os

# Mendefinisikan nama dan path file JSON
DATA_DIR = 'data'
MEMBER_FILE = os.path.join(DATA_DIR, 'member.json')
BOOK_FILE = os.path.join(DATA_DIR, 'book.json')
LOAN_ACTIVE_FILE = os.path.join(DATA_DIR, 'loan_active.json')
LOAN_HISTORY_FILE = os.path.join(DATA_DIR, 'loan_history.json') 

def load_data(filename):
    """
    Membaca data dari file JSON.
    Ini juga membuat folder 'data' jika belum ada.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    try:
        with open(filename, 'r') as f:
            # Mengembalikan data jika file ada dan isinya valid
            return json.load(f)
    except FileNotFoundError:
        # Mengembalikan dictionary kosong jika file belum ada
        return {}
    except json.JSONDecodeError:
        # Mengembalikan dictionary kosong jika file rusak/kosong
        print(f"[{os.path.basename(filename)}] File data rusak. Menginisialisasi dengan data kosong.")
        return {}

def save_data(data, filename):
    """Menulis data ke file JSON."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as error:
        print(f"Error: Tidak dapat menyimpan data ke {os.path.basename(filename)}: {error}")

def get_all_data():
    """Mengambil semua data aplikasi dari disk."""
    # Mengubah nama key dictionary sesuai dengan nama file
    return {
        'member': load_data(MEMBER_FILE),
        'book': load_data(BOOK_FILE),
        'loan_active': load_data(LOAN_ACTIVE_FILE),
        'loan_history': load_data(LOAN_HISTORY_FILE) 
    }

def save_all_data(data):
    """Menyimpan semua data aplikasi ke disk."""
    # Menyimpan data berdasarkan key dictionary
    save_data(data['member'], MEMBER_FILE)
    save_data(data['book'], BOOK_FILE)
    save_data(data['loan_active'], LOAN_ACTIVE_FILE)
    save_data(data['loan_history'], LOAN_HISTORY_FILE)