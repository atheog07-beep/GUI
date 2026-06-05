import tkinter as tk #import library gui
from tkinter import messagebox #import modul dialog popup (error, warning, konfirmasi)
import pandas as pd  #import library pandas
import matplotlib.pyplot as plt #import library matplotlib untuk membuat grafik
import matplotlib.ticker as mticker #import library matplotlib untuk mengformat label disetiap sumbu 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #import untuk menampilkan chart matplotlib di dalam jendela Tkinte

class Chart(tk.Toplevel): #inisiasi class chart yang punya window terpisah
    def __init__(self, parent, laporan): #construktor
        super().__init__(parent)
        self.laporan = laporan
        self.build()
    #method untuk build window chart
    def build(self):
        if self.laporan.cek_kosong():
            messagebox.showwarning("Warning", "Belum ada laporan penjualan")
            self.destroy()
            return

        self.title("Chart Laporan Penjualan")
        self.geometry("900x650")
        self.configure(bg="white")

        tk.Frame(self, bg="#003DA5", height=8).pack(fill="x")
        tk.Label(self, text="Chart Penjualan", font=("Arial", 12, "bold"),
                 bg="white", fg="#003DA5").pack(pady=8)

        self.tampil_chart()  

        tk.Button(self, text="Tutup", command=self.destroy,
                  font=("Arial", 10), bg="white", fg="#003DA5",
                  relief="solid", bd=1, padx=16, pady=6, cursor="hand2").pack(pady=8)
        
    #method untuk menampilkan 4 chart berdasarkan laporan penjualan
    def tampil_chart(self):
        df = pd.read_csv(self.laporan.file, usecols=["tanggal", "nama", "jumlah", "subtotal"])
        df["tanggal"] = pd.to_datetime(df["tanggal"])
        df["hari"]    = df["tanggal"].dt.day_name()
        df["bulan"]   = df["tanggal"].dt.strftime("%b %Y")

        per_produk  = df.groupby("nama")["jumlah"].sum().sort_values(ascending=False)
        per_tanggal = df.groupby(df["tanggal"].dt.strftime("%d %b"))["subtotal"].sum()
        urutan_hari = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        label_hari  = ["Sen","Sel","Rab","Kam","Jum","Sab","Min"]
        per_hari    = df.groupby("hari")["subtotal"].sum().reindex(urutan_hari, fill_value=0)
        per_bulan   = df.groupby("bulan")["subtotal"].sum()

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 7), facecolor="white")
        fig.subplots_adjust(hspace=0.5, wspace=0.4)

        ax1.pie(per_produk.values, labels=per_produk.index, autopct="%1.1f%%",
                startangle=90, textprops={"fontsize": 8})
        ax1.set_title("Produk Terlaris", fontsize=10, fontweight="bold")

        ax2.bar(per_tanggal.index, per_tanggal.values, color="#003DA5")
        ax2.set_title("Penjualan per Tanggal", fontsize=10, fontweight="bold")
        ax2.set_xlabel("Tanggal", fontsize=8)
        ax2.set_ylabel("Total (Rp)", fontsize=8)
        ax2.tick_params(axis="x", rotation=45, labelsize=7)

        ax3.bar(label_hari, per_hari.values, color="#E61E25")
        ax3.set_title("Penjualan per Hari", fontsize=10, fontweight="bold")
        ax3.set_xlabel("Hari", fontsize=8)
        ax3.set_ylabel("Total (Rp)", fontsize=8)

        ax4.bar(per_bulan.index, per_bulan.values, color="#28a745")
        ax4.set_title("Penjualan per Bulan", fontsize=10, fontweight="bold")
        ax4.set_xlabel("Bulan", fontsize=8)
        ax4.set_ylabel("Total (Rp)", fontsize=8)
        ax4.tick_params(axis="x", rotation=20, labelsize=7)

        fmt = mticker.FuncFormatter(lambda x, _: f"Rp {int(x):,}".replace(",", "."))
        ax2.yaxis.set_major_formatter(fmt)
        ax3.yaxis.set_major_formatter(fmt)
        ax4.yaxis.set_major_formatter(fmt)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=4)
