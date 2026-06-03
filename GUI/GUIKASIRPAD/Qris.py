import tkinter as tk
import datetime as dt
import qrcode
from PIL import ImageTk

class Qris(tk.Toplevel):
    def __init__(self, parent, total_bersih, dikonfirmasi):
        super().__init__(parent)
        self.total_bersih = total_bersih
        self.dikonfirmasi = dikonfirmasi
        self.build()

    def rupiah(self, angka):
        return f"Rp {int(angka):,}".replace(",", ".")

    def build(self):
        self.title("Metode Pembayaran QRIS :)")
        self.geometry("380x500")
        self.resizable(False, False)
        self.configure(bg="white")

        tk.Frame(self, bg="#003DA5", height=8).pack(fill="x")  
        tk.Label(self, text="Scan QR untuk menyelesaikan pembayaran",
                 font=("Arial", 9), bg="white", fg="gray").pack()

        frmRingkasan = tk.Frame(self, bg="#f0f4ff", padx=12, pady=10)
        frmRingkasan.pack(fill="x", padx=20, pady=10)
        tk.Label(frmRingkasan, text="Total yang harus dibayar :",
                 font=("Arial", 9), bg="#f0f4ff", fg="#555555").pack(anchor="w")
        tk.Label(frmRingkasan, text=self.rupiah(self.total_bersih),  
                 font=("Arial", 14, "bold"), bg="#f0f4ff", fg="#003DA5").pack(anchor="w")

        data_qr = f"KASIR|{self.total_bersih}|{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=5, border=3)
        qr.add_data(data_qr)
        qr.make(fit=True)
        img_qr  = qr.make_image(fill_color="black", back_color="white")
        foto_qr = ImageTk.PhotoImage(img_qr)

        frmQR = tk.Frame(self, bg="#003DA5", padx=3, pady=3)
        frmQR.pack(pady=8)
        lblQR = tk.Label(frmQR, image=foto_qr, bg="white")
        lblQR.image = foto_qr
        lblQR.pack()

        tk.Label(self, text="Buka aplikasi e-wallet, lalu scan QR di atas",
                 font=("Arial", 9), bg="white", fg="gray", wraplength=300).pack(pady=(0,10))

        frmBtn = tk.Frame(self, bg="white")
        frmBtn.pack(pady=4)
        tk.Button(frmBtn, text="Batal", command=self.destroy,
                  font=("Arial", 10), bg="white", fg="#003DA5",
                  relief="solid", bd=1, padx=16, pady=6,
                  cursor="hand2").pack(side="left", padx=6)
        tk.Button(frmBtn, text="Konfirmasi Bayar", command=self.konfirmasi,
                  font=("Arial", 10, "bold"), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6,
                  cursor="hand2").pack(side="left", padx=6)

        tk.Frame(self, bg="#E61E25", height=6).pack(fill="x", side="bottom")

    def konfirmasi(self):
        self.destroy()
        self.dikonfirmasi()