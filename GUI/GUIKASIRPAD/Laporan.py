import os#import modul os untuk cek file csv
import csv#import modul csv untuk baca csv
import datetime as dt#import datetime untuk ambil waktu sekarang

class Laporan:#inisialisasi class Laporan
    def __init__(self, file_laporan):#constructor berparameter file_laporan
        self.file = file_laporan  #simpan path laporan ke attribut

    def simpan(self, keranjang, total_bersih):#method untuk simpan transaksi
        if not keranjang: return#jika keranjang kosong, exit
        tanggal      = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")#ambil waktu saat ini dengan format
        tulis_header = not os.path.exists(self.file) or os.path.getsize(self.file) == 0#jika file belum ada = true, perlu tulis header
        with open(self.file, "a", newline="", encoding="utf-8") as f:#buka file mode append
            writer = csv.writer(f)#buat objek csv writer
            if tulis_header:#jika file baru
                writer.writerow(["tanggal", "kode", "nama", "jumlah", "harga_satuan", "subtotal", "total_bersih"])#buat header
            for item in keranjang:#iterasi untuk tulis satu baris/kolom
                writer.writerow([
                    tanggal, item["kode"], item["nama"],
                    item["jumlah"], item["harga"], item["subtotal"], total_bersih
                ])

    def kosongkan(self):#method untuk hapus semua isi laporan
        with open(self.file, "w", newline="", encoding="utf-8"):
            pass

    def cek_kosong(self):  #cek apakah laporan kosong
        return not os.path.exists(self.file) or os.path.getsize(self.file) == 0
