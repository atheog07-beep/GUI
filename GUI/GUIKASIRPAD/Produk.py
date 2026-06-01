import pandas as pd

class Produk:
    def __init__(self, file_produk):
        self.file_produk = file_produk
        self.daftar      = self.baca()

    def baca(self):
        df = pd.read_csv(self.file_produk) 
        df = df.rename(columns={"nama_barang": "nama"})
        df["kode"]  = df["kode"].astype(str)
        df["harga"] = df["harga"].astype(int)
        return df.to_dict(orient="records")

    def cari(self, nama):
        for item in self.daftar:
            if item["nama"] == nama:
                return item
        return None