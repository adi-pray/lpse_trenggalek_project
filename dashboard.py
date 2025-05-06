import streamlit as st
import pandas as pd
import sqlite3
import os
from fpdf import FPDF

st.set_page_config(page_title="Dashboard Tender LPSE Trenggalek", layout="wide")

# Path ke database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "lpse_trenggalek.db"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data dari database
try:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM tender", conn)
    conn.close()
except Exception as e:
    st.error(f"Gagal membuka database: {e}")
    st.stop()

# Tambah kolom tahun (jika mungkin)
def extract_year(nama):
    for part in nama.split():
        if part.isdigit() and len(part) == 4 and part.startswith("20"):
            return int(part)
    return None

df['tahun'] = df['nama_paket'].apply(extract_year)

st.title("📊 Dashboard Tender LPSE Trenggalek")

# === Filter ===
instansi_list = df['instansi'].dropna().unique().tolist()
