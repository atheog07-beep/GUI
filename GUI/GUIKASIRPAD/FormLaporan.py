import tkinter as tk #import library gui
import csv #import modul untuk membaca dan menulis file .csv

class FormLaporan(tk.Toplevel): #inisiasi class FormLaporan yang punya window terpisah dari window utama 
    def __init__(self, parent, laporan, on_chart=None): #construktor
        super().__init__(parent)
        self.laporan  = laporan
        self.on_chart = on_chart  
        self.build()             

    #method untuk build window Laporan penjualan
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
        
        tombol_bawah = [
            ("Lihat Chart", self.lihat_chart, "white", "#003DA5"),
            ("Tutup",   self.destroy,    "white", "#003DA5"),
            ("Hapus Laporan", self.hapus_laporan, "white", "#003DA5")
        ]
        for text, cmd, bg, fg in tombol_bawah:
            btn = tk.Button(frame_btn, text=text, command=cmd,
                            font=("Arial", 10), bg=bg, fg=fg,
                            relief="solid", bd=1, padx=10, pady=6, cursor="hand2")
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#0056b3", fg="white"))
            btn.bind("<Leave>", lambda e, b=bg, f=fg: e.widget.config(bg=b, fg=f))
            btn.pack(side="right", padx=(10,0))
        self.isi_laporan()  

    #method untuk membuka file laporan penjualan dan ditampilkan di listbox
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
    #method untuk hapus laporan penjualan
    def hapus_laporan(self):
        from tkinter import messagebox
        if self.laporan.cek_kosong():
            messagebox.showwarning("Error", "Tidak ada laporan penjualan")
            return
        if messagebox.askyesno("Konfirmasi", "Hapus semua laporan penjualan?"):
            self.laporan.kosongkan()
            messagebox.showinfo("Info", "Laporan berhasil dihapus!")
            self.destroy()
    #method untuk membuka window chart
    def lihat_chart(self):
        if self.on_chart:
            self.on_chart()  

    #method helper untuk mengformat harga atau subtotal menjadi rupiah
    def rupiah(self, angka):
        return f"Rp {int(angka):,}".replace(",", ".")

    #method helper untuk memberikan efek saat ada kursor diatas tombol
    def buat_button(self, parent, text, command, **kwargs):
        btn = tk.Button(parent, text=text, command=command,
                        bg="white", fg="#003DA5", **kwargs)
        btn.bind("<Enter>", lambda event: event.widget.config(bg="#0056b3", fg="white"))
        btn.bind("<Leave>", lambda event: event.widget.config(bg="white", fg="#003DA5"))
        return btn
