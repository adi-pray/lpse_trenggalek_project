import streamlit as st
import pandas as pd
import sqlite3
import os
from fpdf import FPDF

st.set_page_config(page_title="Dashboard Tender LPSE Trenggalek", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "lpse_trenggalek.db"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM tender", conn)
    conn.close()
except Exception as e:
    st.error(f"Gagal membuka database: {e}")
    st.stop()

def extract_year(text):
    for part in text.split():
        if part.isdigit() and len(part) == 4 and part.startswith("20"):
            return int(part)
    return None

df['tahun'] = df['nama_paket'].apply(extract_year)

st.title("📊 Dashboard Tender LPSE Trenggalek")
st.markdown("Menampilkan hasil scraping data tender dari situs LPSE Trenggalek.")

st.subheader(f"📄 Total data: {len(df)}")

instansi_list = df['instansi'].dropna().unique().tolist()
selected_instansi = st.multiselect("Filter berdasarkan Instansi:", instansi_list)
if selected_instansi:
    df = df[df['instansi'].isin(selected_instansi)]

year_list = sorted(df['tahun'].dropna().unique())
selected_year = st.multiselect("Filter berdasarkan Tahun:", year_list)
if selected_year:
    df = df[df['tahun'].isin(selected_year)]

st.dataframe(df)

excel_path = os.path.join(OUTPUT_DIR, "tender_trenggalek.xlsx")
if st.button("📥 Ekspor ke Excel"):
    df.to_excel(excel_path, index=False)
    st.success(f"File Excel berhasil dibuat di: {excel_path}")

def export_to_pdf(dataframe, path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for idx, row in dataframe.iterrows():
        baris = f"{row['kode']} | {row['nama_paket']} | {row['instansi']} | {row['nilai_kontrak']}"
        pdf.cell(0, 10, baris, ln=True)

    pdf.output(path)

pdf_path = os.path.join(OUTPUT_DIR, "laporan_tender.pdf")
if st.button("🧾 Ekspor ke PDF"):
    export_to_pdf(df, pdf_path)
    st.success(f"File PDF berhasil dibuat di: {pdf_path}")
