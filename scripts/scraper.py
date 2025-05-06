import requests
from bs4 import BeautifulSoup
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "lpse_trenggalek.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tender (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kode TEXT,
        nama_paket TEXT,
        instansi TEXT,
        nilai_hps TEXT,
        jenis_pengadaan TEXT,
        kode_tender TEXT,
        pemenang TEXT,
        npwp TEXT,
        alamat TEXT,
        email TEXT,
        nilai_penawaran TEXT,
        nilai_kontrak TEXT,
        ringkasan_ai TEXT
    )
''')
conn.commit()

def buat_ringkasan(row):
    return f"Paket '{row[1]}' oleh {row[2]} dimenangkan oleh {row[6]} dengan nilai penawaran {row[10]} dari HPS {row[3]}."

sample_data = [
    ("001", "Pengadaan Barang A 2024", "Dinas PU", "1.000.000.000", "Barang", "T-001", "CV. Maju Jaya", "1234567890", "Jl. Contoh No.1", "maju@jaya.com", "900.000.000", "890.000.000")
]

data_with_summary = []
for row in sample_data:
    ringkasan = buat_ringkasan(row)
    data_with_summary.append((*row, ringkasan))

cursor.executemany('''
    INSERT INTO tender (kode, nama_paket, instansi, nilai_hps, jenis_pengadaan, kode_tender, pemenang, npwp, alamat, email, nilai_penawaran, nilai_kontrak, ringkasan_ai)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', data_with_summary)

conn.commit()
conn.close()
print("Database berhasil diisi dengan data contoh dan ringkasan AI.")
