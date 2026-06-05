import tkinter as tk #import library gui
from tkinter import messagebox #import modul dialog popup (error, warning, konfirmasi)
from Produk import Produk #impoert class untuk membaca dan mencari data produk dari CSV
from Kasir import Kasir #import class untuk mengelola keranjang belanja dan transaksi
from Laporan import Laporan #import class untuk menyimpan dan membaca laporan penjualan
from Struk import Struk #import class untuk window Struk
from FormLaporan import FormLaporan #import class untuk window laporan penjualan
from Chart import Chart #import class untuk window diagram
from Qris import Qris #import class untuk window Qris
import os #import untuk mengambil path file secara dinamis

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #mendapatkan lokasi folder tempat file itu berada
FILE_PRODUK = os.path.join(BASE_DIR, "produk.csv")  #path lengkap ke file produk
FILE_LAPORAN = os.path.join(BASE_DIR, "laporan_penjualan.csv")  #path lengkap ke file laporan_penjualan

class App: #inisiasi class App sebagai window utama
    def __init__(self, root): #constructor
        self.root      = root
        self.produk    = Produk(FILE_PRODUK)
        self.kasir     = Kasir()
        self.laporan   = Laporan(FILE_LAPORAN)
        self.keranjang = self.kasir.keranjang
        self.build() #panggil method build
        
    #method helper untuk mengformat harga atau subtotal menjadi format mata uang Rupiah
    def rupiah(self, angka):
        return f"Rp {int(angka):,}".replace(",", ".")
        
    #build keseluruhan layout utama aplikasi
    def build(self):

        #untuk judul
        self.root.title("KlikRomushaMaret Kasir")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        #frame header (kepala)
        frame_header = tk.Frame(self.root, bg="#003DA5", height=70)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        tk.Label(frame_header, text="KLiK RomushaMaret  —  Kasir",
                 font=("Arial", 22, "bold"), fg="white", bg="#003DA5").pack(expand=True)

        tk.Frame(self.root, bg="#E61E25", height=10).pack(fill="x")

        #frame tengah
        frame_tengah = tk.Frame(self.root, bg="white")
        frame_tengah.pack(fill="both", expand=True, padx=30, pady=20)

        #untuk build frame kiri, kanan, bawah dan tombolnya
        self.build_form(frame_tengah)
        self.build_keranjang(frame_tengah)
        self.build_footer()
        
    #Membangun frame kiri berisi form pemilihan produk, input jumlah, tampilan harga, pilihan metode pembayaran, dan tombol tambah ke keranjang
    def build_form(self, parent):

        #bentuk frame kiri
        frame_form = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=24, pady=20)
        frame_form.pack(side="left", fill="y", ipadx=10)

        #label untuk Pilih produk
        tk.Label(frame_form, text="Pilih produk yang akan ditambahkan :",
                 font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", pady=(0,4))
        
        #label untuk masukan jumlah barang
        tk.Label(frame_form, text="Masukkan jumlah barang :").grid(row=2, column=0, sticky="w")
        self.entry_jml = tk.Entry(frame_form, width=12, font=("Arial", 11), relief="solid", bd=1)
        self.entry_jml.insert(0, "1")
        self.entry_jml.grid(row=3, column=0, sticky="w", pady=(5,20))
        self.entry_jml.bind("<KeyRelease>", self.update_harga)

        #buat label untuk harga satuan barang
        frame_harga = tk.Frame(frame_form, bg="#f0f4ff", bd=1, relief="solid", padx=12, pady=10)
        frame_harga.grid(row=4, column=0, sticky="we", pady=(0,16))
        tk.Label(frame_harga, text="Harga Satuan Barang : ",
                 font=("Arial", 10), bg="#f0f4ff", fg="#f55555").grid(row=0, column=0, sticky="w")
        self.lblHargaSatuanReal = tk.Label(frame_harga, text="Rp 0",
                 font=("Arial", 10), bg="#f0f4ff", fg="#003DA5")
        self.lblHargaSatuanReal.grid(row=0, column=1, sticky="e", padx=(20,0))

        #buat label untuk harga total barang
        frame_harga2 = tk.Frame(frame_form, bg="#f0f4ff", bd=1, relief="solid", padx=12, pady=10)
        frame_harga2.grid(row=5, column=0, sticky="we", pady=(0,16))
        tk.Label(frame_harga2, text="Harga Total Barang : ",
                 font=("Arial", 10), bg="#f0f4ff", fg="#f55555").grid(row=0, column=0, sticky="w")
        self.lblHargaTotalReal = tk.Label(frame_harga2, text="Rp 0",
                 font=("Arial", 10), bg="#f0f4ff", fg="#003DA5")
        self.lblHargaTotalReal.grid(row=0, column=1, sticky="e", padx=(20,0))

        #option menu untuk pilih metode pembayaran
        self.lblPilih2 = tk.StringVar()
        self.lblPilih2.set("Metode Pembayaran")
        pembayaran = tk.OptionMenu(frame_form, self.lblPilih2, "Cash", "Qris")
        pembayaran.config(width=34, font=("Arial", 10), cursor="hand2" )
        pembayaran.grid(row=6, column=0, sticky="w", pady=(0,16))

        #button untuk masukan belanjaan ke keranjang
        btnTambah = tk.Button(frame_form, text="  Masukan Ke Keranjang  ",
          font=("Arial", 10, "bold"), bg="#003DA5", fg="white",
          relief="flat", padx=10, pady=8, cursor="hand2",
          command=self.tambah_ke_keranjang)
        btnTambah.grid(row=7, column=0, sticky="w", pady=(0,10))
        btnTambah.bind("<Enter>", lambda e: e.widget.config(bg="#0056b3"))
        btnTambah.bind("<Leave>", lambda e: e.widget.config(bg="#003DA5"))
        
        #option menu untuk pilih produk yang mau di beli
        self.lblPilih = tk.StringVar()
        self.lblPilih.set("Pilih produk")
        contoh_produk = [item["nama"] for item in self.produk.daftar]
        opsiProduk = tk.OptionMenu(frame_form, self.lblPilih, *contoh_produk)
        opsiProduk.config(width=34, font=("Arial", 10), cursor="hand2" )
        opsiProduk.grid(row=1, column=0, sticky="w", pady=(0,16))
        self.lblPilih.trace_add("write", self.update_harga)
        
    #build frame kanan berisi daftar item di keranjang belanja dan label total harga
    def build_keranjang(self, parent):
        #buat frame kanan
        frame_kanan = tk.Frame(parent, bg="white")
        frame_kanan.pack(side="left", fill="both", expand=True, padx=(20,0))

        #buat label keranjang
        frame_keranjang = tk.Frame(frame_kanan, bg="#003DA5")
        frame_keranjang.pack(fill="x")
        tk.Label(frame_keranjang, text="Keranjang Belanja",
                 font=("Arial", 11, "bold"), fg="white", bg="#003DA5", pady=8).pack(side="left", padx=12)
        
        #listbox untuk menampilkan daftar item di keranjang
        self.listKeranjang = tk.Listbox(frame_kanan, font=("Arial", 10),
                                        bg="white", relief="flat", bd=0,
                                        selectbackground="#BBDEFB",
                                        highlightthickness=1,
                                        highlightbackground="#cccccc")
        self.listKeranjang.pack(fill="both", expand=True)

        #frame total harga di bagian bawah keranjang
        frmTotal = tk.Frame(frame_kanan, bg="#003DA5", pady=10)
        frmTotal.pack(fill="x")
        self.lblTotal = tk.Label(frmTotal, text="Total   : Rp 0",
                                 font=("Arial", 13, "bold"), fg="#FFD700", bg="#003DA5")
        self.lblTotal.pack(side="right", padx=16)
        
    #build baris tombol lihat produk, cetak struk, hapus keranjang, dan lihat laporan di bagian bawah
    def build_footer(self):
        #frame bawah
        frame_bawah = tk.Frame(self.root, bg="#e8e8e8", pady=12)
        frame_bawah.pack(fill="x", padx=20, pady=4)
        
        #daftar tombol kiri
        tombol_kiri = [
            ("Lihat Daftar Produk", self.lihat_daftar_produk, "white", "#003DA5"),
            ("Cetak Struk",         self.form_cetak_struk,    "#E61E25", "white"),
        ]
        #berikan efek hover
        for text, cmd, bg, fg in tombol_kiri:
            btn = tk.Button(frame_bawah, text=text, command=cmd,
                            font=("Arial", 10), bg=bg, fg=fg,
                            relief="solid", bd=1, padx=10, pady=6, cursor="hand2")
            btn.bind("<Enter>", lambda e, b=bg: e.widget.config(bg="#0056b3", fg="white"))
            btn.bind("<Leave>", lambda e, b=bg, f=fg: e.widget.config(bg=b, fg=f))
            btn.pack(side="left", padx=(0,10))

        #daftar tombol kanan
        tombol_kanan = [
            ("Hapus Keranjang", self.hapus_keranjang, "white", "#003DA5"),
            ("Lihat Laporan",   self.form_laporan,    "white", "#003DA5"),
        ]
        #berikan efek hover
        for text, cmd, bg, fg in tombol_kanan:
            btn = tk.Button(frame_bawah, text=text, command=cmd,
                            font=("Arial", 10), bg=bg, fg=fg,
                            relief="solid", bd=1, padx=10, pady=6, cursor="hand2")
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#0056b3", fg="white"))
            btn.bind("<Leave>", lambda e, b=bg, f=fg: e.widget.config(bg=b, fg=f))
            btn.pack(side="right", padx=(10,0))

    #method untuk memperbarui tampilan harga satuan dan harga total setiap kali produk atau jumlah barang berubah
    def update_harga(self, *args): 
        item = self.produk.cari(self.lblPilih.get()) #cari produk berdasarkan nama yang dipilih
        #kalo item tidak ditemukan, maka harga satuan dan total akan direset
        if not item: 
            self.lblHargaSatuanReal.config(text="Rp 0")
            self.lblHargaTotalReal.config(text="Rp 0")
            return
        #jika input bukan angka, jumlah jadi 1
        try:
            jumlah = int(self.entry_jml.get())
        except:
            jumlah = 1
        #tampilkan harga satuan dan harga total dalam format rupiah
        self.lblHargaSatuanReal.config(text=self.rupiah(item["harga"]))
        self.lblHargaTotalReal.config(text=self.rupiah(item["harga"] * jumlah))

    #method untuk menambahkan produk yang dipilih ke keranjang belanja
    def tambah_ke_keranjang(self):
        #jika input bukan angka, messagebox muncul
        try:
            jumlah = int(self.entry_jml.get())
        except:
            messagebox.showerror("Error", "Jumlah harus angka!")
            return
        #jika jumlah kurang dari sama dengan 0, maka messagebox muncul
        if jumlah <= 0:
            messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
            return
        item = self.produk.cari(self.lblPilih.get()) #cari produk berdasarkan nama yang dipilih
        #kalo item tidak ditemukan, maka messagebox muncul
        if not item:
            messagebox.showerror("Error", "Produk tidak ditemukan")
            return
        #tambahkan item ke keranjang dan perbarui keranjangnya
        self.kasir.tambah_item(item["kode"], item["nama"], item["harga"], jumlah)
        self.refresh_keranjang()
        
    #method untuk me-refresh tampilan listbox keranjang dan memperbarui label total harga
    def refresh_keranjang(self):
        self.listKeranjang.delete(0, tk.END)  #hapus semua isi listbox
        total = 0 #harga total awal
        #setiap item dalam keranjang, akan ditambahkan ke listbox
        for item in self.keranjang:
            self.listKeranjang.insert(tk.END,  
                f"{item['nama']} | {item['jumlah']} x {self.rupiah(item['harga'])}")
            total += item["subtotal"]
        #perbarui label harga total
        self.lblTotal.config(text=f"Total   : {self.rupiah(total)}")
        
    #method untuk menghapus isi keranjang secara keseluruhan
    def hapus_keranjang(self):
        #jika keranjang kosong, maka messagebox muncul
        if not self.keranjang:
            messagebox.showwarning("Error", "Tidak ada barang di keranjang!")
            return
        #tampilkan popup konfirmasi untuk clear keranjang
        if messagebox.askyesno("Konfirmasi", "Hapus semua barang di keranjang?"):
            self.kasir.clear_keranjang()  
            self.refresh_keranjang()
            
    #method untuk menampilkan struk pembayaran 
    def form_cetak_struk(self):
        #jika keranjang kosong, maka messagebox muncul
        if not self.keranjang:
            messagebox.showwarning("Error", "Tidak ada barang dalam keranjang!")
            return
        #jika belum pilih metode pembayaran, maka muncul messagebox
        if self.lblPilih2.get() == "Metode Pembayaran":
            messagebox.showwarning("Error", "Pilih metode pembayaran!")
            return

        total         = self.kasir.hitung_total()
        persen_diskon = self.kasir.diskon()
        nilai_diskon  = total * persen_diskon // 100
        total_bersih  = total - nilai_diskon
        metode        = self.lblPilih2.get()

        #fungsi lokal untuk membuka window struk
        def lanjut():
            Struk(self.root, self.keranjang, metode,
                  self.kasir, self.laporan, self.refresh_keranjang)

        #jika pilih metode Qris, maka tampilkan window qris
        if metode == "Qris":
            Qris(self.root, total_bersih, dikonfirmasi=lanjut)  
        else:#langsung cetak struk jika metode Cash
            lanjut() 
            
    #method untuk membuka form laporan penjualan dengan opsi untuk melihat chart
    def form_laporan(self): 
        FormLaporan(self.root, self.laporan,
                    on_chart=lambda: Chart(self.root, self.laporan))
        
    #method untuk menampilkan window daftar produk
    def lihat_daftar_produk(self):
        win = tk.Toplevel(self.root) #buat window baru sebagai child dari root
        win.title("Daftar Produk")
        win.geometry("620x460")
        win.configure(bg="white")

        #untuk bagian head window
        tk.Frame(win, bg="#003DA5", height=8).pack(fill="x")
        tk.Label(win, text="DAFTAR PRODUK TERSEDIA",
                 font=("Arial", 12, "bold"), bg="white", fg="#003DA5").pack(pady=10)

        #listbox untuk menampilkan daftar produk
        lb = tk.Listbox(win, font=("Consolas", 10), width=80, height=20,
                        bg="white", relief="flat", highlightbackground="#cccccc")
        lb.pack(padx=16, pady=4)

        #perulangan untuk tambahkan baris ke listbox
        for item in self.produk.daftar:
            lb.insert(tk.END,
                f"{item['kode']:<6}{item['nama']:<40}{self.rupiah(item['harga'])}")
        #tombol tutup window
        tk.Button(win, text="Tutup", command=win.destroy,
                  font=("Arial", 10), bg="#003DA5", fg="white",
                  relief="flat", padx=16, pady=6 ).pack(pady=8)
        
    #method helper untuk memberikan efek saat ada kursor diatas tombol
    def buat_button(self, parent, text, command, **kwargs):
        btn = tk.Button(parent, text=text, command=command,
                        bg="white", fg="#003DA5", **kwargs)
        btn.bind("<Enter>", lambda event: event.widget.config(bg="#0056b3", fg="white")) #ubah warna saat hover
        btn.bind("<Leave>", lambda event: event.widget.config(bg="white", fg="#003DA5")) #kembalikan warna saat kursor pergi
        return btn #kembalikan objek button ke pemanggil
