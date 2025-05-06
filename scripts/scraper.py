import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import os

# Pastikan folder data/ tersedia
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "lpse_trenggalek.db")

BASE_URL = 'https://lpse.trenggalekkab.go.id'

def scrape():
    url = BASE_URL + '/eproc4/lelang'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    rows = soup.select('table.table tbody tr')

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
            nilai_kontrak TEXT
        )
    ''')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            kode = cols[0].text.strip()
            nama_paket = cols[1].text.strip()
            instansi = cols[2].text.strip()
            nilai_hps = cols[3].text.strip()

            # Placeholder
            jenis_pengadaan = "Belum Diambil"
            kode_tender = kode
            pemenang = npwp = alamat = email = nilai_penawaran = nilai_kontrak = "-"

            cursor.execute('''
                INSERT INTO tender (
                    kode, nama_paket, instansi, nilai_hps,
                    jenis_pengadaan, kode_tender, pemenang, npwp,
                    alamat, email, nilai_penawaran, nilai_kontrak
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                kode, nama_paket, instansi, nilai_hps,
                jenis_pengadaan, kode_tender, pemenang, npwp,
                alamat, email, nilai_penawaran, nilai_kontrak
            ))
            conn.commit()
            time.sleep(0.5)

    conn.close()

if __name__ == "__main__":
    scrape()
