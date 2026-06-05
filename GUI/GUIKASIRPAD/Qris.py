import tkinter as tk#impoer library tkinter
import datetime as dt#import datetime 
import qrcode#impoer library qrcode untuk generate qr
from PIL import ImageTk#import ImageTK dari Pillow (konv gambar ke format tkinter)

class Qris(tk.Toplevel):#inisialisasi class Qris, mewarisi child window)
    def __init__(self, parent, total_bersih, dikonfirmasi):#constructor berparameter parent window, total_bersih, dikonfirmasi
        super().__init__(parent)#panggil constructor window induk
        self.total_bersih = total_bersih#simpan total bersih ke attribut
        self.dikonfirmasi = dikonfirmasi#simpan fungsi dikonfirmasi(callback)
        self.build()#panggil method build()

    def rupiah(self, angka):# method untuk format angka rupiah
        return f"Rp {int(angka):,}".replace(",", ".")

    def build(self):#method untuk membangun seluruh tampilan window
        #but window utama
        self.title("Metode Pembayaran QRIS :)")
        self.geometry("380x500")
        self.resizable(False, False)
        self.configure(bg="white")
        
        tk.Frame(self, bg="#003DA5", height=8).pack(fill="x")#dekorasi 
        tk.Label(self, text="Scan QR untuk menyelesaikan pembayaran",#label pernyataan
                 font=("Arial", 9), bg="white", fg="gray").pack()

        frmRingkasan = tk.Frame(self, bg="#f0f4ff", padx=12, pady=10)#grame ringkasan
        frmRingkasan.pack(fill="x", padx=20, pady=10)
        tk.Label(frmRingkasan, text="Total yang harus dibayar :",#label pernyataan
                 font=("Arial", 9), bg="#f0f4ff", fg="#555555").pack(anchor="w")
        tk.Label(frmRingkasan, text=self.rupiah(self.total_bersih),  #label total yang harus dibayar
                 font=("Arial", 14, "bold"), bg="#f0f4ff", fg="#003DA5").pack(anchor="w")

        data_qr = f"KASIR|{self.total_bersih}|{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"#data yang akan dibuat qr
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=5, border=3)#buat objek qrcode
        qr.add_data(data_qr)#masukan data ke objek QR
        qr.make(fit=True)#generate QR
        img_qr  = qr.make_image(fill_color="black", back_color="white")#buat gambar QR
        foto_qr = ImageTk.PhotoImage(img_qr)#konversi gambar ke format tkinter

        frmQR = tk.Frame(self, bg="#003DA5", padx=3, pady=3)#frame dekor
        frmQR.pack(pady=8)
        lblQR = tk.Label(frmQR, image=foto_qr, bg="white")#label untuk tampilan gambar qr
        lblQR.image = foto_qr
        lblQR.pack()

        tk.Label(self, text="Buka aplikasi e-wallet, lalu scan QR di atas",#label pernyataan
                 font=("Arial", 9), bg="white", fg="gray", wraplength=300).pack(pady=(0,10))

        frmBtn = tk.Frame(self, bg="white")#frame untuk penempatan button
        frmBtn.pack(pady=4)
        tk.Button(frmBtn, text="Batal", command=self.destroy,
                  font=("Arial", 10), bg="white", fg="#003DA5",
                  relief="solid", bd=1, padx=16, pady=6,
                  cursor="hand2").pack(side="left", padx=6)#button batal
        tk.Button(frmBtn, text="Konfirmasi Bayar", command=self.konfirmasi,
                  font=("Arial", 10, "bold"), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6,
                  cursor="hand2").pack(side="left", padx=6)#button konfirmasi bayar

        tk.Frame(self, bg="#E61E25", height=6).pack(fill="x", side="bottom")#frame dekor diklik

    def konfirmasi(self):#method dipanggil saat konfirmasi bayar
        #tutup window  QRIS
        self.destroy()
        self.dikonfirmasi()#jalankan callback (lanjut cetak struk)
