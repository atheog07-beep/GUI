import tkinter as tk
import datetime as dt

class Struk(tk.Toplevel):
    def __init__(self, parent, keranjang, metode, kasir, laporan, refresh_callback):
        super().__init__(parent)
        self.keranjang        = keranjang
        self.metode           = metode
        self.kasir            = kasir
        self.laporan          = laporan
        self.refresh_callback = refresh_callback
        self.build()

    def rupiah(self, angka):
        return f"Rp {int(angka):,}".replace(",", ".")

    def build(self):
        self.title("Cetak Struk Belanja")
        self.geometry("420x500")
        self.resizable(False, False)
        self.configure(bg="white")

        tk.Frame(self, bg="#003DA5", height=8).pack(fill="x")
        tk.Label(self, text="STRUK BELANJA",
                 font=("Arial", 14, "bold"), bg="white", fg="#003DA5").pack(pady=(12,2))
        tk.Label(self, text=dt.datetime.now().strftime("%d %B %Y"),  
                 font=("Arial", 9), bg="white", fg="gray").pack()
        tk.Label(self, text="-" * 52,
                 font=("Courier", 9), bg="white").pack(pady=(6,2))

        isi_struk = ""
        total = 0
        for item in self.keranjang:
            isi_struk += (f"{item['nama']}\n"
                          f"{item['jumlah']} x {self.rupiah(item['harga'])}"
                          f" = {self.rupiah(item['subtotal'])}\n\n")
            total += item["subtotal"]

        persen_diskon = self.kasir.diskon()  
        nilai_diskon  = total * persen_diskon // 100
        total_bersih  = total - nilai_diskon

        tk.Label(self, text=isi_struk, font=("Courier", 9), bg="white",
                 fg="#000000", justify="left").pack(anchor="w", padx=20)
        tk.Label(self, text="-" * 52, font=("Courier", 9), bg="white").pack(pady=(6,2))
        tk.Label(self, text=f"Total          : {self.rupiah(total)}",
                 font=("Courier", 10, "bold"), bg="white").pack(anchor="w", padx=20)
        tk.Label(self, text=f"Diskon ({persen_diskon}%) : {self.rupiah(nilai_diskon)}",
                 font=("Courier", 10), bg="white").pack(anchor="w", padx=20)
        tk.Label(self, text=f"Total Bersih   : {self.rupiah(total_bersih)}",
                 font=("Courier", 11, "bold"), bg="white", fg="#003DA5").pack(anchor="w", padx=20)
        tk.Label(self, text=f"Metode bayar   : {self.metode}",  
                 font=("Courier", 11), bg="white").pack(anchor="w", padx=20)
        tk.Label(self, text="-" * 52, font=("Courier", 9), bg="white").pack(pady=(6,2))
        tk.Label(self, text="Terima kasih telah berbelanja!",
                 font=("Arial", 10, "italic"), bg="white").pack(pady=4)

        tk.Frame(self, bg="#E61E25", height=6).pack(fill="x", side="bottom")
        tk.Button(self, text="Tutup", command=self.destroy,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6).pack(pady=10, side="bottom")

        self.laporan.simpan(self.keranjang, total_bersih)
        self.kasir.clear_keranjang()
        self.refresh_callback()  