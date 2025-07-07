import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="Peta Jaringan Alat Iklim", layout="wide")

st.title("🗺️ Peta Jaringan Alat Pengamatan Iklim")
st.markdown("Menampilkan lokasi seluruh alat pengamatan iklim dari berbagai jenis dengan detail lengkap, serta menyediakan unduhan peta PDF.")

# ===============================
# File alat & PDF
# ===============================
alat_files = {
   # "AAWS": "data/Metadata AAWS.csv",
   # "ARG": "data/Metadata ARG.csv",
   # "ASRS": "data/Metadata ASRS.csv",
   # "AWS": "data/Metadata AWS.csv",
    "IKLIM MIKRO": "data/Metadata IKRO.csv"
}

pdf_files = {
    "AAWS": "pdf/peta_jaringan_aaws.pdf",
    "ARG": "pdf/peta_jaringan_arg.pdf",
    "ASRS": "pdf/peta_jaringan_asrs.pdf",
    "AWS": "pdf/peta_jaringan_aws.pdf",
    "IKLIM MIKRO": "pdf/peta_jaringan_iklim_mikro.pdf"
}

color_map = {
   # "AAWS": "red",
   # "ARG": "blue",
   # "ASRS": "green",
   # "AWS": "orange",
    "IKLIM MIKRO": "purple"
}

# ===============================
# Gabungkan semua data alat
# ===============================
all_data = []
for jenis, path in alat_files.items():
    print(f"Mengolah data {jenis} dari {path}...")
    try:
        df = pd.read_csv(path, sep=';')
    except FileNotFoundError:
        st.error(f"❌ File {path} tidak ditemukan.")
        continue
    df['jenis'] = jenis
    df.rename(columns={
        'latt_station': 'lat',
        'long_station': 'lon',
        'nama_propinsi': 'provinsi'
    }, inplace=True)
    all_data.append(df)

df_all = pd.concat(all_data, ignore_index=True)

# ===============================
# Inisialisasi peta
# ===============================
m = folium.Map(location=[-2.5, 118.0], zoom_start=5)
marker_cluster = MarkerCluster().add_to(m)

# ===============================
# Tambahkan marker ke peta
# ===============================
for _, row in df_all.iterrows():
    try:
        lat = float(row['lat'])
        lon = float(row['lon'])
    except:
        continue

    # Buat konten popup dari semua kolom
    popup_html = ""
    for col in row.index:
        popup_html += f"<b>{col}:</b> {row[col]}<br>"

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=350),
        icon=folium.Icon(color=color_map.get(row['jenis'], "gray"))
    ).add_to(marker_cluster)

# ===============================
# Tampilkan peta di Streamlit
# ===============================
st_data = st_folium(m, width=1000, height=600)

# ===============================
# Dropdown untuk download PDF
# ===============================
st.subheader("⬇️ Unduh Peta PDF Berdasarkan Jenis Alat")

alat_pilihan = st.selectbox("Pilih jenis peta alat:", list(pdf_files.keys()))

if alat_pilihan:
    pdf_path = pdf_files[alat_pilihan]
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=f"📄 Download {alat_pilihan}",
                data=f,
                file_name=pdf_path.split("/")[-1],
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.error(f"❌ File PDF {pdf_path} tidak ditemukan.")