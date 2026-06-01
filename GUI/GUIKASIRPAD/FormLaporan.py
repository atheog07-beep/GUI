import tkinter as tk
import csv

class FormLaporan(tk.Toplevel):
    def __init__(self, parent, laporan, on_chart=None):
        super().__init__(parent)
        self.laporan  = laporan
        self.on_chart = on_chart  
        self.build()             

    def build(self):
        self.title("Laporan Penjualan")
        self.geometry("620x460")
        self.configure(bg="white")

        tk.Frame(self, bg="#003DA5", height=8).pack(fill="x")
        tk.Label(self, text="Laporan Penjualan", font=("Arial", 12, "bold"),
                 bg="white", fg="#003DA5").pack(pady=10)

        self.lb = tk.Listbox(self, font=("Arial", 9), width=80, height=20,
                             bg="white", relief="flat", highlightbackground="#cccccc")
        self.lb.pack(padx=16, pady=4)

        # frame button
        frame_btn = tk.Frame(self, bg="#e8e8e8", pady=8)
        frame_btn.pack(fill="x", padx=10)

        tk.Button(frame_btn, text="Lihat Chart", command=self.lihat_chart,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6).pack(side="left", padx=6)
        tk.Button(frame_btn, text="Tutup", command=self.destroy,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Hapus Laporan", command=self.hapus_laporan,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6).pack(side="right", padx=10)

        self.isi_laporan()  

    def isi_laporan(self):
        if self.laporan.cek_kosong():
            self.lb.insert(tk.END, "Belum ada laporan penjualan")
            return
        with open(self.laporan.file, newline="", encoding="utf-8") as f:
            baca = csv.DictReader(f)
            tanggal_sebelumnya = None
            baris = None
            for baris in baca:
                tanggal = baris["tanggal"]
                if tanggal != tanggal_sebelumnya:
                    self.lb.insert(tk.END, "=" * 50)
                    self.lb.insert(tk.END, f"Tanggal : {tanggal}")
                    self.lb.insert(tk.END, f"{'Nama Barang':<38} {'Jml':>5} {'Harga':>14} {'Subtotal':>14}")
                    self.lb.insert(tk.END, "-" * 50)
                    tanggal_sebelumnya = tanggal
                self.lb.insert(tk.END,
                    f"  {baris['nama']:<38} {baris['jumlah']:>5} "
                    f"{self.rupiah(baris['harga_satuan']):>14} "
                    f"{self.rupiah(baris['subtotal']):>14}"
                )

    def hapus_laporan(self):
        from tkinter import messagebox
        if self.laporan.cek_kosong():
            messagebox.showwarning("Error", "Tidak ada laporan penjualan")
            return
        if messagebox.askyesno("Konfirmasi", "Hapus semua laporan penjualan?"):
            self.laporan.kosongkan()
            messagebox.showinfo("Info", "Laporan berhasil dihapus!")
            self.destroy()

    def lihat_chart(self):
        if self.on_chart:
            self.on_chart()  
    
    def rupiah(self, angka):
        return f"Rp {int(angka):,}".replace(",", ".")