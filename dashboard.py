import streamlit as st
import pandas as pd
import sqlite3
import os
from fpdf import FPDF

st.set_page_config(page_title="Dashboard Tender LPSE Trenggalek", layout="wide")

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "lpse_trenggalek.db"))
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM tender", conn)
conn.close()

st.title("📊 Dashboard Tender LPSE Trenggalek")

# Tambah kolom tahun dari nama_paket
def extract_year(nama):
    for part in nama.split():
        if part.isdigit() and len(part) == 4 and part.startswith("20"):
            return int(part)
    return None

df['tahun'] = df['nama_paket'].apply(extract_year)

# === Filter ===
instansi_list = df['instansi'].dropna().unique().tolist()
selected_instansi = st.multiselect("Filter berdasarkan instansi:", instansi_list)
if selected_instansi:
    df = df[df['instansi'].isin(selected_instansi)]

available_years = sorted(df['tahun'].dropna().unique().astype(int))
selected_years = st.multiselect("Filter berdasarkan tahun:", available_years)
if selected_years:
    df = df[df['tahun'].isin(selected_years)]

nilai_kontrak_min = st.number_input("Nilai kontrak minimal", min_value=0, value=0)
df['nilai_kontrak_num'] = df['nilai_kontrak'].replace('-', '0').str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float)
df = df[df['nilai_kontrak_num'] >= nilai_kontrak_min]

st.dataframe(df.drop(columns=['nilai_kontrak_num']))

# === Ekspor Excel ===
if st.button("📥 Download Excel"):
    df.to_excel("../output/tender_trenggalek.xlsx", index=False)
    st.success("Excel berhasil dibuat di folder output.")

# === Ekspor PDF ===
def export_to_pdf(dataframe, path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for index, row in dataframe.iterrows():
        line = f"{row['kode']} | {row['nama_paket']} | {row['instansi']} | {row['nilai_kontrak']}"
        pdf.cell(0, 10, line, ln=True)

    pdf.output(path)

if st.button("🧾 Export ke PDF"):
    export_to_pdf(df, "../output/laporan_tender.pdf")
    st.success("PDF berhasil dibuat di folder output.")
