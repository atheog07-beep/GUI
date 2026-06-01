import os
import csv
import datetime as dt

class Laporan:
    def __init__(self, file_laporan):
        self.file = file_laporan  

    def simpan(self, keranjang, total_bersih):
        if not keranjang: return
        tanggal      = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tulis_header = not os.path.exists(self.file) or os.path.getsize(self.file) == 0
        with open(self.file, "a", newline="", encoding="utf-8") as f:  
            writer = csv.writer(f)  
            if tulis_header:
                writer.writerow(["tanggal", "kode", "nama", "jumlah", "harga_satuan", "subtotal", "total_bersih"])
            for item in keranjang:
                writer.writerow([
                    tanggal, item["kode"], item["nama"],
                    item["jumlah"], item["harga"], item["subtotal"], total_bersih
                ])

    def kosongkan(self):
        with open(self.file, "w", newline="", encoding="utf-8"):
            pass

    def cek_kosong(self):  
        return not os.path.exists(self.file) or os.path.getsize(self.file) == 0