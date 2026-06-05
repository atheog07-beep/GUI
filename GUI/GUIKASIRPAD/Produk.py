import pandas as pd#import library pandas alias pd
import os#import modul os
class Produk:#inisialisasi class Produk
    def __init__(self, file_produk):#constructor berparameter file produk
        base_dir = os.path.dirname(os.path.abspath(__file__))#ambil directory file
        self.file_produk = os.path.join(base_dir, file_produk)#gabung directory dengan nama file
        self.daftar      = self.baca()#panggil method bava()

    def baca(self):#method untuk membaca file produk csv
        df = pd.read_csv(self.file_produk) #baca file csv ke dalam dataframe pd
        df = df.rename(columns={"nama_barang": "nama"})#rename kolom agar seragam
        df["kode"]  = df["kode"].astype(str)#konversi kolom kode ke String
        df["harga"] = df["harga"].astype(int)#konversi kolom harga ke integer
        return df.to_dict(orient="records")#konversi dataframe ke list of dict

    def cari(self, nama):#method untuk mencari produk berdasarkan nama
        for item in self.daftar:#iterasi setiap item dalam produk
            if item["nama"] == nama:#jika nama cocok
                return item#return data produk
        return None#jika tidak, none
