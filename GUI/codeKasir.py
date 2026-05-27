import datetime as dt
import pandas as pd
import os
import csv

FILE_PRODUK  = r"C:\Users\LENOVO\OneDrive\Documents\IF belajar 2\KasirPAD\GUI\produk.csv"
FILE_LAPORAN = r"C:\Users\LENOVO\OneDrive\Documents\IF belajar 2\KasirPAD\GUI\laporan_penjualan.csv"

keranjang = []

def baca_produk():
    df = pd.read_csv(FILE_PRODUK)
    df = df.rename(columns={"nama_barang": "nama"})  #rename nama_barang jadi nama
    df["kode"]  = df["kode"].astype(str)
    df["harga"] = df["harga"].astype(int)
    return df.to_dict(orient="records")

def garis(karakter="=", n=50):
    return karakter * n  

def rupiah(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

def cek_diskon(total):
    if total >= 200000:
        return 15
    elif total >= 100000:
        return 10
    elif total >= 50000:
        return 5
    else:
        return 0

def cekLaporan():
    #True = laporan kosong/belum ada, False = laporan sudah ada
    return not os.path.exists(FILE_LAPORAN) or os.path.getsize(FILE_LAPORAN) == 0

def laporan_penjualan():
    if len(keranjang) == 0:
        return

    total = 0
    for item in keranjang:
        total += item["subtotal"]

    wktu          = dt.datetime.now()
    tgl_str       = wktu.strftime("%Y-%m-%d %H:%M:%S")
    persen_diskon = cek_diskon(total)
    nilai_diskon  = total * persen_diskon // 100
    total_bersih  = total - nilai_diskon

    #cek file kosong/belum ada
    tulis_header = not os.path.exists(FILE_LAPORAN) or os.path.getsize(FILE_LAPORAN) == 0

    with open(FILE_LAPORAN, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if tulis_header:
            writer.writerow(["tanggal", "kode", "nama", "jumlah", "harga_satuan", "subtotal", "total_bersih"])
        for item in keranjang:
            writer.writerow([
                tgl_str,
                item["kode"],
                item["nama"],   #pakai "nama" bukan "nama_barang" karena udah di-rename
                item["jumlah"],
                item["harga"],
                item["subtotal"],
                total_bersih
            ])
        #made by Adrian Theo Narendra and Vio Febrian
        #UTS_PAD