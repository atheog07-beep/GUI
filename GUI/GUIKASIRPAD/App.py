import tkinter as tk
from tkinter import messagebox
from Produk import Produk
from Kasir import Kasir
from Laporan import Laporan
from Struk import Struk
from FormLaporan import FormLaporan
from Chart import Chart
from Qris import Qris

FILE_PRODUK  = r"C:\Users\LENOVO\OneDrive\Documents\IF belajar 2\KasirPAD\GUI\GUIKASIRPAD\produk.csv"
FILE_LAPORAN = r"C:\Users\LENOVO\OneDrive\Documents\IF belajar 2\KasirPAD\GUI\GUIKASIRPAD\laporan_penjualan.csv"

class App:  
    def __init__(self, root):
        self.root      = root
        self.produk    = Produk(FILE_PRODUK)
        self.kasir     = Kasir()
        self.laporan   = Laporan(FILE_LAPORAN)
        self.keranjang = self.kasir.keranjang
        self.build()

    def rupiah(self, angka):
        return f"Rp {int(angka):,}".replace(",", ".")

    def build(self):
        self.root.title("KlikRomushaMaret Kasir")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        frame_header = tk.Frame(self.root, bg="#003DA5", height=70)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        tk.Label(frame_header, text="KLiK RomushaMaret  —  Kasir",
                 font=("Arial", 22, "bold"), fg="white", bg="#003DA5").pack(expand=True)

        tk.Frame(self.root, bg="#E61E25", height=10).pack(fill="x")

        frame_tengah = tk.Frame(self.root, bg="white")
        frame_tengah.pack(fill="both", expand=True, padx=30, pady=20)

        self.build_form(frame_tengah)
        self.build_keranjang(frame_tengah)
        self.build_footer()

    def build_form(self, parent):
        frame_form = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=24, pady=20)
        frame_form.pack(side="left", fill="y", ipadx=10)

        tk.Label(frame_form, text="Pilih produk yang akan ditambahkan :",
                 font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", pady=(0,4))

        tk.Label(frame_form, text="Masukkan jumlah barang :").grid(row=2, column=0, sticky="w")
        self.entry_jml = tk.Entry(frame_form, width=12, font=("Arial", 11), relief="solid", bd=1)
        self.entry_jml.insert(0, "1")
        self.entry_jml.grid(row=3, column=0, sticky="w", pady=(5,20))
        self.entry_jml.bind("<KeyRelease>", self.update_harga)

        frame_harga = tk.Frame(frame_form, bg="#f0f4ff", bd=1, relief="solid", padx=12, pady=10)
        frame_harga.grid(row=4, column=0, sticky="we", pady=(0,16))
        tk.Label(frame_harga, text="Harga Satuan Barang : ",
                 font=("Arial", 10), bg="#f0f4ff", fg="#f55555").grid(row=0, column=0, sticky="w")
        self.lblHargaSatuanReal = tk.Label(frame_harga, text="Rp 0",
                 font=("Arial", 10), bg="#f0f4ff", fg="#003DA5")
        self.lblHargaSatuanReal.grid(row=0, column=1, sticky="e", padx=(20,0))

        frame_harga2 = tk.Frame(frame_form, bg="#f0f4ff", bd=1, relief="solid", padx=12, pady=10)
        frame_harga2.grid(row=5, column=0, sticky="we", pady=(0,16))
        tk.Label(frame_harga2, text="Harga Total Barang : ",
                 font=("Arial", 10), bg="#f0f4ff", fg="#f55555").grid(row=0, column=0, sticky="w")
        self.lblHargaTotalReal = tk.Label(frame_harga2, text="Rp 0",
                 font=("Arial", 10), bg="#f0f4ff", fg="#003DA5")
        self.lblHargaTotalReal.grid(row=0, column=1, sticky="e", padx=(20,0))

        self.lblPilih2 = tk.StringVar()
        self.lblPilih2.set("Metode Pembayaran")
        pembayaran = tk.OptionMenu(frame_form, self.lblPilih2, "Cash", "Qris")
        pembayaran.config(width=34, font=("Arial", 10), cursor="hand2" )
        pembayaran.grid(row=6, column=0, sticky="w", pady=(0,16))

        btnTambah = tk.Button(frame_form, text="  Masukan Ke Keranjang  ",
          font=("Arial", 10, "bold"), bg="#003DA5", fg="white",
          relief="flat", padx=10, pady=8, cursor="hand2",
          command=self.tambah_ke_keranjang)
        btnTambah.grid(row=7, column=0, sticky="w", pady=(0,10))
        btnTambah.bind("<Enter>", lambda e: e.widget.config(bg="#0056b3"))
        btnTambah.bind("<Leave>", lambda e: e.widget.config(bg="#003DA5"))
        
        self.lblPilih = tk.StringVar()
        self.lblPilih.set("Pilih produk")
        contoh_produk = [item["nama"] for item in self.produk.daftar]
        opsiProduk = tk.OptionMenu(frame_form, self.lblPilih, *contoh_produk)
        opsiProduk.config(width=34, font=("Arial", 10), cursor="hand2" )
        opsiProduk.grid(row=1, column=0, sticky="w", pady=(0,16))
        self.lblPilih.trace_add("write", self.update_harga)

    def build_keranjang(self, parent):
        frame_kanan = tk.Frame(parent, bg="white")
        frame_kanan.pack(side="left", fill="both", expand=True, padx=(20,0))

        frame_keranjang = tk.Frame(frame_kanan, bg="#003DA5")
        frame_keranjang.pack(fill="x")
        tk.Label(frame_keranjang, text="Keranjang Belanja",
                 font=("Arial", 11, "bold"), fg="white", bg="#003DA5", pady=8).pack(side="left", padx=12)

        self.listKeranjang = tk.Listbox(frame_kanan, font=("Arial", 10),
                                        bg="white", relief="flat", bd=0,
                                        selectbackground="#BBDEFB",
                                        highlightthickness=1,
                                        highlightbackground="#cccccc")
        self.listKeranjang.pack(fill="both", expand=True)

        frmTotal = tk.Frame(frame_kanan, bg="#003DA5", pady=10)
        frmTotal.pack(fill="x")
        self.lblTotal = tk.Label(frmTotal, text="Total   : Rp 0",
                                 font=("Arial", 13, "bold"), fg="#FFD700", bg="#003DA5")
        self.lblTotal.pack(side="right", padx=16)

    def build_footer(self):
        frame_bawah = tk.Frame(self.root, bg="#e8e8e8", pady=12)
        frame_bawah.pack(fill="x", padx=20, pady=4)

        tombol_kiri = [
            ("Lihat Daftar Produk", self.lihat_daftar_produk, "white", "#003DA5"),
            ("Cetak Struk",         self.form_cetak_struk,    "#E61E25", "white"),
        ]
        for text, cmd, bg, fg in tombol_kiri:
            btn = tk.Button(frame_bawah, text=text, command=cmd,
                            font=("Arial", 10), bg=bg, fg=fg,
                            relief="solid", bd=1, padx=10, pady=6, cursor="hand2")
            btn.bind("<Enter>", lambda e, b=bg: e.widget.config(bg="#0056b3", fg="white"))
            btn.bind("<Leave>", lambda e, b=bg, f=fg: e.widget.config(bg=b, fg=f))
            btn.pack(side="left", padx=(0,10))

        tombol_kanan = [
            ("Hapus Keranjang", self.hapus_keranjang, "white", "#003DA5"),
            ("Lihat Laporan",   self.form_laporan,    "white", "#003DA5"),
        ]
        for text, cmd, bg, fg in tombol_kanan:
            btn = tk.Button(frame_bawah, text=text, command=cmd,
                            font=("Arial", 10), bg=bg, fg=fg,
                            relief="solid", bd=1, padx=10, pady=6, cursor="hand2")
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#0056b3", fg="white"))
            btn.bind("<Leave>", lambda e, b=bg, f=fg: e.widget.config(bg=b, fg=f))
            btn.pack(side="right", padx=(10,0))

    # ── METHODS ──────────────────────────────────────────

    def update_harga(self, *args):
        
        item = self.produk.cari(self.lblPilih.get())
        if not item:
            self.lblHargaSatuanReal.config(text="Rp 0")
            self.lblHargaTotalReal.config(text="Rp 0")
            return
        try:
            jumlah = int(self.entry_jml.get())
        except:
            jumlah = 1
        self.lblHargaSatuanReal.config(text=self.rupiah(item["harga"]))
        self.lblHargaTotalReal.config(text=self.rupiah(item["harga"] * jumlah))

    def tambah_ke_keranjang(self):
        try:
            jumlah = int(self.entry_jml.get())
        except:
            messagebox.showerror("Error", "Jumlah harus angka!")
            return
        if jumlah <= 0:
            messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
            return
        item = self.produk.cari(self.lblPilih.get())
        if not item:
            messagebox.showerror("Error", "Produk tidak ditemukan")
            return
        self.kasir.tambah_item(item["kode"], item["nama"], item["harga"], jumlah)
        self.refresh_keranjang()

    def refresh_keranjang(self):
        self.listKeranjang.delete(0, tk.END)  
        total = 0
        for item in self.keranjang:
            self.listKeranjang.insert(tk.END,  
                f"{item['nama']} | {item['jumlah']} x {self.rupiah(item['harga'])}")
            total += item["subtotal"]
        self.lblTotal.config(text=f"Total   : {self.rupiah(total)}")

    def hapus_keranjang(self):
        if not self.keranjang:
            messagebox.showwarning("Error", "Tidak ada barang di keranjang!")
            return
        if messagebox.askyesno("Konfirmasi", "Hapus semua barang di keranjang?"):
            self.kasir.clear_keranjang()  
            self.refresh_keranjang()

    def form_cetak_struk(self):
        if not self.keranjang:
            messagebox.showwarning("Error", "Tidak ada barang dalam keranjang!")
            return
        if self.lblPilih2.get() == "Metode Pembayaran":
            messagebox.showwarning("Error", "Pilih metode pembayaran!")
            return
        total         = self.kasir.hitung_total()
        persen_diskon = self.kasir.diskon()
        nilai_diskon  = total * persen_diskon // 100
        total_bersih  = total - nilai_diskon
        metode        = self.lblPilih2.get()

        def lanjut():
            Struk(self.root, self.keranjang, metode,
                  self.kasir, self.laporan, self.refresh_keranjang)

        if metode == "Qris":
            Qris(self.root, total_bersih, dikonfirmasi=lanjut)  
        else:
            lanjut()

    def form_laporan(self): 
        FormLaporan(self.root, self.laporan,
                    on_chart=lambda: Chart(self.root, self.laporan))

    def lihat_daftar_produk(self):
        win = tk.Toplevel(self.root)
        win.title("Daftar Produk")
        win.geometry("620x460")
        win.configure(bg="white")

        tk.Frame(win, bg="#003DA5", height=8).pack(fill="x")
        tk.Label(win, text="DAFTAR PRODUK TERSEDIA",
                 font=("Arial", 12, "bold"), bg="white", fg="#003DA5").pack(pady=10)

        lb = tk.Listbox(win, font=("Consolas", 10), width=80, height=20,
                        bg="white", relief="flat", highlightbackground="#cccccc")
        lb.pack(padx=16, pady=4)

        for item in self.produk.daftar:
            lb.insert(tk.END,
                f"{item['kode']:<6}{item['nama']:<40}{self.rupiah(item['harga'])}")

        tk.Button(win, text="Tutup", command=win.destroy,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6 ).pack(pady=8)
        
    def buat_button(self, parent, text, command, **kwargs):
        btn = tk.Button(parent, text=text, command=command,
                        bg="white", fg="#003DA5", **kwargs)
        btn.bind("<Enter>", lambda event: event.widget.config(bg="#0056b3", fg="white"))
        btn.bind("<Leave>", lambda event: event.widget.config(bg="white", fg="#003DA5"))
        return btn