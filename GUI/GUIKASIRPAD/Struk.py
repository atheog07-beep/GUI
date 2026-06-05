import tkinter as tk#import library tkinter
import datetime as dt#import datetime

class Struk(tk.Toplevel):#inisialisasi class Struk, mewarisi window anak
    def __init__(self, parent, keranjang, metode, kasir, laporan, refresh_callback):#constructor berparameter semua data utk cetak struk
        super().__init__(parent)#panggil constructor parent
        self.keranjang        = keranjang
        self.metode           = metode
        self.kasir            = kasir
        self.laporan          = laporan
        self.refresh_callback = refresh_callback
        self.build()#panggil method build

    def rupiah(self, angka):#method pembantu untuk format angka ke rupiah
        return f"Rp {int(angka):,}".replace(",", ".")

    def build(self):#method untuk membangun window utama
        #bangun window utama
        self.title("Cetak Struk Belanja")
        self.geometry("420x500")
        self.resizable(False, False)
        self.configure(bg="white")

        tk.Frame(self, bg="#003DA5", height=8).pack(fill="x")#buat frame dekor
        tk.Label(self, text="STRUK BELANJA",
                 font=("Arial", 14, "bold"), bg="white", fg="#003DA5").pack(pady=(12,2))#label judul
        tk.Label(self, text=dt.datetime.now().strftime("%d %B %Y"),#label tanggal transaksi
                 font=("Arial", 9), bg="white", fg="gray").pack()
        tk.Label(self, text="-" * 52,
                 font=("Courier", 9), bg="white").pack(pady=(6,2))#label garis pemisah

        isi_struk = ""#deklarasi string
        total = 0#deklarasi total harga
        for item in self.keranjang:#iterasi setiap item dalam keranjang
            isi_struk += (f"{item['nama']}\n"
                          f"{item['jumlah']} x {self.rupiah(item['harga'])}"
                          f" = {self.rupiah(item['subtotal'])}\n\n")#tambah nama, jumlah, subtotal harga
            total += item["subtotal"]#akumulasi total harga
        #definisikan persen diskon, nilai diskon dan hitung total bersih
        persen_diskon = self.kasir.diskon()
        nilai_diskon  = total * persen_diskon // 100
        total_bersih  = total - nilai_diskon

        tk.Label(self, text=isi_struk, font=("Courier", 9), bg="white",
                 fg="#000000", justify="left").pack(anchor="w", padx=20)#label rincian semua item belanja
        tk.Label(self, text="-" * 52, font=("Courier", 9), bg="white").pack(pady=(6,2))#label pemisah
        tk.Label(self, text=f"Total          : {self.rupiah(total)}",
                 font=("Courier", 10, "bold"), bg="white").pack(anchor="w", padx=20)#label total sebelum diskon
        tk.Label(self, text=f"Diskon ({persen_diskon}%) : {self.rupiah(nilai_diskon)}",
                 font=("Courier", 10), bg="white").pack(anchor="w", padx=20)#label diskon
        tk.Label(self, text=f"Total Bersih   : {self.rupiah(total_bersih)}",
                 font=("Courier", 11, "bold"), bg="white", fg="#003DA5").pack(anchor="w", padx=20)#label total bersih
        tk.Label(self, text=f"Metode bayar   : {self.metode}",  
                 font=("Courier", 11), bg="white").pack(anchor="w", padx=20)#label metode bayar
        tk.Label(self, text="-" * 52, font=("Courier", 9), bg="white").pack(pady=(6,2))#label garis pemisah
        tk.Label(self, text="Terima kasih telah berbelanja!",
                 font=("Arial", 10, "italic"), bg="white").pack(pady=4)#label ucapan terimakasih

        tk.Frame(self, bg="#E61E25", height=6).pack(fill="x", side="bottom")#frame demor
        tk.Button(self, text="Tutup", command=self.destroy,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6, cursor="hand2").pack(pady=10, side="bottom")#tombol tutup window struk

        self.laporan.simpan(self.keranjang, total_bersih)#simpan transaksi ke file laproan csv
        self.kasir.clear_keranjang()#kosongkan keranjang setelah selesai transaksi
        self.refresh_callback()  #panggil callback untuk update listbox
