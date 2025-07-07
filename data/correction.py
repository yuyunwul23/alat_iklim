# file_path = r"C:\Users\yuuyu\Documents\Folder Yuyun\BMKG\Tugas CPNS Direktorat Perubahan Iklim - Manop\Peta_Interaktif\data\Metadata_AAWS.csv"
file_path = 'Metadata AAWS.csv'
def cek_csv(file_path):
    try:
        # Baca file CSV
        df = pd.read_csv(file_path, sep=';')
        print("File berhasil dibaca.")
        
        # Tampilkan 5 baris pertama sebagai preview
        print("Preview data:")
        print(df.head())
        
        # Cek nilai kosong (missing values)
        if df.isnull().values.any():
            print("WARNING: Ada nilai kosong di data.")
            print(df.isnull().sum())
        else:
            print("Tidak ada nilai kosong.")
        
        # Cek tipe data tiap kolom
        print("Tipe data tiap kolom:")
        print(df.dtypes)
        
        # Cek duplikat baris
        duplikat = df.duplicated().sum()
        if duplikat > 0:
            print(f"Ada {duplikat} baris duplikat.")
        else:
            print("Tidak ada duplikat.")
        
        # Contoh cek kolom tanggal jika ada
        if 'tanggal' in df.columns:
            try:
                pd.to_datetime(df['tanggal'])
                print("Kolom 'tanggal' valid sebagai tanggal.")
            except Exception:
                print("Kolom 'tanggal' TIDAK valid sebagai tanggal.")
        
        return df
        
    except FileNotFoundError:
        print("File tidak ditemukan. Pastikan path dan nama file sudah benar.")
    except pd.errors.ParserError:
        print("File tidak dapat diparsing, kemungkinan format CSV bermasalah.")
    except Exception as e:
        print("Terjadi kesalahan:", e)
import pandas as pd
df = cek_csv(file_path)

if df is not None:
    print("File CSV siap digunakan dalam pemrograman.")
else:
    print("File CSV belum siap, cek kembali file dan formatnya.")