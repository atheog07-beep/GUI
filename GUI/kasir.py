
import tkinter as tk #import library tkinter
from tkinter import messagebox#import messagebox dari library tkinter
import codeKasir #import modul backend kasir
import datetime as dt#menampilkan tanggal
import qrcode#import library qr code
from PIL import ImageTk #import module tkinter image
import pandas as pd
import matplotlib.pyplot as plt

"""
Function cari_produk
mencari produk dari daftar produk, berdasarkan nama
mengembalikam dictionary jika data ditemukan
"""
def cari_produk(nama):
    for item in produk:#iterasi setiap item dalam produk
        if item["nama"] == nama:#jika nama ketemu, kembalikan item
            return item
    return None  #jika tidak, return none

"""
Function tambah_ke_keranjang
ambil produk yang dipilih dan jumlahnya, lalu menambahnya ke keranjang
<<jika item sudah ada, jumlah&subtotal diperbarui>>
"""
def tambah_ke_keranjang():
    nama_produk = lblPilih.get()#ambil produk dari option menu
    try:
        jumlah = int(entry_jml.get())#konversi input jml ke integer
    except:
        messagebox.showerror("Error", "Jumlah harus angka!") #jika bukan angka akan error
        return
    if jumlah <= 0:  
        messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
        return
    item = cari_produk(nama_produk)#cari produk berdasarkan nama
    if item == None:
        messagebox.showerror("Error", "Produk yang dicari tidak ditemukan") #jika produk tidak ditemukan
        return   
    subTotal = item["harga"] * jumlah#hitung subtotal
    sudah_ada = False#bool untuk cek apakah priodyk sudah ada dalam keranjang
    for barang in keranjang:#iterasi item dlm keranjang
        if barang["kode"] == item["kode"]:#jika item sudah ada, update keranjang
            barang["jumlah"] += jumlah
            barang["subtotal"] = barang["jumlah"] * barang["harga"]
            sudah_ada = True
    if not sudah_ada:#jika tidak ada, tambah item ke keranjang
        keranjang.append({"kode": item["kode"], "nama": item["nama"], "harga": item["harga"], "jumlah": jumlah, "subtotal": subTotal})
    
    refresh_keranjang()#refresh keranjang

"""
Function formLaporan
membuka windows anak isi laporan penjualan
"""
def formLaporan():
    #bentuk window
    lihatLaporan = tk.Toplevel()
    lihatLaporan.title("Laporan Penjualan")
    lihatLaporan.geometry("620x460")
    lihatLaporan.configure(bg="white")

    #buat frame judul dan label judul
    frame1 = tk.Frame(lihatLaporan, bg="#003DA5", height=8)
    frame1.pack(fill="x")
    lbljudul = tk.Label(lihatLaporan, text="Laporan Penjualan",font=("Arial", 12, "bold"), bg="white", fg="#003DA5")
    lbljudul.pack(pady=10)
    #buat listbox untuk menampilkan laporan penjualan
    lb = tk.Listbox(lihatLaporan, font=("Arial",9),width=80, height=20,bg="white", relief="flat", highlightbackground= "#cccccc")
    lb.pack(padx=16,pady=4)
    #buat button hapus keranjang dan tutup window
    frame_btn = tk.Frame(lihatLaporan, bg="#e8e8e8", pady=8)
    frame_btn.pack(fill="x", padx=10)

    btnchart = tk.Button(frame_btn, text="Lihat Chart", command=formChart,
              font=("Arial", 10), bg="#003DA5", fg="white",
              relief="flat", padx=16, pady=6)
    btnchart.pack(side="left", padx=6)
    btnHapus = tk.Button(frame_btn, text="Hapus Laporan", command= lambda: hapus_laporan(lihatLaporan), font=("Arial",10), bg="#003DA5", fg="white", relief="flat", padx=16, pady=6)
    btnHapus.pack(side="right",padx=10)
    btnTutup2 = tk.Button(frame_btn, text="Tutup", command= lihatLaporan.destroy, font=("Arial",10), bg="#003DA5", fg="white", relief="flat", padx=16, pady=6)
    btnTutup2.pack(side="left", padx=10)

    import csv
    if codeKasir.cekLaporan():
        lb.insert(tk.END, "Belum ada laporan penjualan")
    else:
        with open(codeKasir.FILE_LAPORAN, newline="", encoding="utf-8") as f:
            baca = csv.DictReader(f) 
            tanggal_sebelumnya = None
            baris = None
            for baris in baca:
                tanggal = baris["tanggal"]
                if tanggal != tanggal_sebelumnya:
                    lb.insert(tk.END, codeKasir.garis())         # FIX: tambah ()
                    lb.insert(tk.END, f"Tanggal : {tanggal}")
                    lb.insert(tk.END, f"{'Nama Barang':<38} {'Jml':>5} {'Harga':>14} {'Subtotal':>14}")
                    lb.insert(tk.END, codeKasir.garis("-"))     # FIX: tambah ()
                    tanggal_sebelumnya = tanggal
                lb.insert(tk.END,
                    f"  {baris['nama']:<38} {baris['jumlah']:>5} "
                    f"{codeKasir.rupiah(baris['harga_satuan']):>14} "
                    f"{codeKasir.rupiah(baris['subtotal']):>14}"
                )
            if baris:
                lb.insert(tk.END, codeKasir.garis("-"))
                lb.insert(tk.END, f"  {'Total Bersih':>55} {codeKasir.rupiah(baris['total_bersih'])}")
                lb.insert(tk.END, codeKasir.garis())

"""
function formChart, buat window chart penjualan /w 4 grafik
-produk terlaris (pie chart)
-total penj/tanggal (batang)
-total penj/hari (batang)
-total penj/bulan (batang)
data dari laporan_penjualan.txt, pakai pandas df
"""
def formChart():
    if codeKasir.cekLaporan():
        messagebox.showwarning("Chart", "Belum ada data penjualan")
        return
    chart = tk.Toplevel()
    chart.title("Chart Laporan Penjualan")
    chart.geometry("900x650")
    chart.configure(bg="white")

    frmDekor = tk.Frame(chart, bg="#003DA5", height=8)
    frmDekor.pack(fill="x")
    lbl1 = tk.Label(chart, text="Chart Penjualan", font=("Arial", 12, "bold"), bg="white", fg="#003DA5")
    lbl1.pack(pady=8)
    df = pd.read_csv(codeKasir.FILE_LAPORAN, usecols=["tanggal", "nama", "jumlah", "subtotal"])
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df["hari"]  = df["tanggal"].dt.day_name()
    df["bulan"] = df["tanggal"].dt.strftime("%b %Y")

    per_produk  = df.groupby("nama")["jumlah"].sum().sort_values(ascending=False)
    per_tanggal = df.groupby(df["tanggal"].dt.strftime("%d %b"))["subtotal"].sum()
    urutan_hari = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    label_hari  = ["Sen","Sel","Rab","Kam","Jum","Sab","Min"]
    per_hari    = df.groupby("hari")["subtotal"].sum().reindex(urutan_hari, fill_value=0)
    per_bulan   = df.groupby("bulan")["subtotal"].sum()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 7), facecolor="white")
    fig.subplots_adjust(hspace=0.5, wspace=0.4)

    #grafik 1: pie chart produk terlaris
    ax1.pie(per_produk.values, labels=per_produk.index, autopct="%1.1f%%",
            startangle=90, textprops={"fontsize": 8})
    ax1.set_title("Produk Terlaris", fontsize=10, fontweight="bold")

    #grafik 2: batang total penjualan per tanggal
    ax2.bar(per_tanggal.index, per_tanggal.values, color="#003DA5")
    ax2.set_title("Penjualan per Tanggal", fontsize=10, fontweight="bold")
    ax2.set_xlabel("Tanggal", fontsize=8)
    ax2.set_ylabel("Total (Rp)", fontsize=8)
    ax2.tick_params(axis="x", rotation=45, labelsize=7)

    #grafik 3: batang total penjualan per hari
    ax3.bar(label_hari, per_hari.values, color="#E61E25")
    ax3.set_title("Penjualan per Hari", fontsize=10, fontweight="bold")
    ax3.set_xlabel("Hari", fontsize=8)
    ax3.set_ylabel("Total (Rp)", fontsize=8)

    #grafik 4: batang total penjualan per bulan
    ax4.bar(per_bulan.index, per_bulan.values, color="#28a745")
    ax4.set_title("Penjualan per Bulan", fontsize=10, fontweight="bold")
    ax4.set_xlabel("Bulan", fontsize=8)
    ax4.set_ylabel("Total (Rp)", fontsize=8)
    ax4.tick_params(axis="x", rotation=20, labelsize=7)

    #format sumbu Y semua grafik batang agar tidak pakai notasi 1e6
    import matplotlib.ticker as mticker
    fmt = mticker.FuncFormatter(lambda x, _: f"Rp {int(x):,}")
    ax2.yaxis.set_major_formatter(fmt)
    ax3.yaxis.set_major_formatter(fmt)
    ax4.yaxis.set_major_formatter(fmt)

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=chart)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=4)

    tk.Button(chart, text="Tutup", command=chart.destroy,
              font=("Arial", 10), bg="white", fg="#003DA5",
              relief="solid", bd=1, padx=16, pady=6).pack(pady=8)

"""
function lihat_daftar_produk
buka child window, tampilkan semua produk
"""
def lihat_daftar_produk():
    #buat window
    lihatProduk = tk.Toplevel()
    lihatProduk.title("Daftar Produk")
    lihatProduk.geometry("620x460")
    lihatProduk.configure(bg="white")
    #buat frame untuk header biru
    frame1 = tk.Frame(lihatProduk, bg="#003DA5", height=8)
    frame1.pack(fill="x")
    #buat label judul
    lbljudul = tk.Label(lihatProduk, text="DAFTAR PRODUK TERSEDIA", font=("Arial", 12, "bold"), bg="white", fg="#003DA5")
    lbljudul.pack(pady=10)
    #buat listbox daftar produk
    lb = tk.Listbox(lihatProduk, font=("Consolas", 10), width=80, height=20, bg="white",
                    relief="flat", highlightbackground="#cccccc")
    lb.pack(padx=16, pady=4)
    #masukan setiap produk ke listbox : kode, nama, harga, kategori
    for item in produk:
        teks = (
            f"{item['kode']:<6}"
            f"{item['nama']:<40}"
            f"{codeKasir.rupiah(item['harga']):<12}"
            f"{item['kategori']:>12}"
        )
        lb.insert(tk.END, teks)
    #buat tombol tutup window
    btnTutup = tk.Button(lihatProduk, text="Tutup", command=lihatProduk.destroy, font=("Arial", 10), bg="#003DA5", fg="white", relief="flat", padx=16, pady=6)
    btnTutup.pack(pady=8)
"""
function hapus_keranjang
mengosongkan isi keranjang
"""
def hapus_keranjang():
    if len(keranjang) == 0: #jika keranjang kosong maka error
        messagebox.showwarning("Error", "Tidak ada barang di keranjang!")
        return
    if messagebox.askyesno("Konfirmasi", "Hapus semua barang di keranjang?"):
        codeKasir.keranjang.clear() #jika ada maka kosongkan keranjang
        refresh_keranjang() #perbarui isi keranjang
 

"""
Function hapus_laporan
#menghapus isi laporan
#@param lihatLaporanuntuk tutup window
"""
def hapus_laporan(lihatLaporan):
    with open(codeKasir.FILE_LAPORAN, "r") as f:#buka FILE_LAPORAN mode r
        cek = f.readlines()
    if len(cek) == 0:
        messagebox.showwarning("Error", "Tidak ada laporan penjualan")#jika tidak ada laporan akan error
        return
    if messagebox.askyesno("Konfirmasi", "Hapus semua laporan penjualan?"):#jika ada
        with open (codeKasir.FILE_LAPORAN, "w"):#buka file laporan mode write
            pass#hapus isi laporan
        messagebox.showinfo("Info", "Laporan berhasil dihapus!")
        lihatLaporan.destroy()#tutup window laporan
"""
window untuk pembayaran Qris
"""
def formQris(total_bersih, dikonfirmasi):
    #buat window
    qris = tk.Toplevel(root)
    qris.title("Metode Pembayaran QRIS :)")
    qris.geometry("380x500")
    qris.resizable(False, False)
    qris.configure(bg="white")

    frDekor = tk.Frame(qris, bg="#003DA5", height=8)#dekorasi
    frDekor.pack(fill = "x")
    #label perintah
    lbl1 = tk.Label(qris,  text="Scan QR untuk menyelesaikan pembayaran",
             font=("Arial", 9), bg="white", fg="gray")
    lbl1.pack()
    #frame ringkasan
    frmRingkasan = tk.Frame(qris,bg="#f0f4ff", padx=12, pady=10)
    frmRingkasan.pack(fill="x", padx=20, pady=10)
    lbl2 = tk.Label(frmRingkasan, text="Total yang harus dibayar :",
             font=("Arial", 9), bg="#f0f4ff", fg="#555555")
    lbl2.pack(anchor="w")
    lbl3 = tk.Label(frmRingkasan, text=codeKasir.rupiah(total_bersih),#total harga
             font=("Arial", 14, "bold"), bg="#f0f4ff", fg="#003DA5")
    lbl3.pack(anchor="w")

    data_qr = f"INDOMARET|{total_bersih}|{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"#isi data qr
 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=3,
    )
    qr.add_data(data_qr)#tambah data_qr
    qr.make(fit=True)#buat qr
    img_qr = qr.make_image(fill_color="black", back_color="white")#buat img qr
 
    foto_qr = ImageTk.PhotoImage(img_qr)#buat imageTk
 
    frmQR = tk.Frame(qris, bg="#003DA5", padx=3, pady=3)
    frmQR.pack(pady=8)
    lblQR = tk.Label(frmQR, image=foto_qr, bg="white")#image
    lblQR.image = foto_qr#simpen referensi agar tidak di-GC
    lblQR.pack()
    #tip pengguna aja
    tk.Label(qris, text="Buka aplikasi e-wallet, lalu scan QR di atas",
             font=("Arial", 9), bg="white", fg="gray",
             wraplength=300).pack(pady=(0, 10))
 
    #deklarasi tombol
    frmBtn = tk.Frame(qris, bg="white")
    frmBtn.pack(pady=4)
 
    def konfirmasi():#jika dikonfirmasi pembayaran
        qris.destroy()
        dikonfirmasi() 
    
    #button batal
    tk.Button(frmBtn, text="Batal", command=qris.destroy,
              font=("Arial", 10), bg="white", fg="#003DA5",
              relief="solid", bd=1, padx=16, pady=6,
              cursor="hand2").pack(side="left", padx=6)
    #button konfirmasi
    tk.Button(frmBtn, text="Konfirmasi Bayar", command=konfirmasi,
              font=("Arial", 10, "bold"), bg="#003DA5", fg="white",
              relief="flat", padx=16, pady=6,
              cursor="hand2").pack(side="left", padx=6)
 
    #dekor bawah
    tk.Frame(qris, bg="#E61E25", height=6).pack(fill="x", side="bottom")

"""
function refresh_keranjang
memperbarui tampilan listbox keranjang dan label total
"""
def refresh_keranjang():
    listKeranjang.delete(0, tk.END) #hapus isi keranjang lama
    total = 0
    for item in keranjang:
        teks = ( #format teks : nama | jumlah * harga
            f"{item['nama']} | "
            f"{item['jumlah']} x "
            f"{codeKasir.rupiah(item['harga'])}"
        )
        listKeranjang.insert(tk.END, teks) #masukan baris ke listbox
        total += item["subtotal"] #akumulasi total
    lblTotal.config(
        text=f"Total : {codeKasir.rupiah(total)}" #perbarui label total
    )

"""
function formCetakStruk
menampilkan window cetak struk
terdapat total, diskon, methode pembayaran
menyimoan laporan penjualan
"""
def formCetakStruk():
    if len(keranjang) == 0: #jika keranjang kosong akan error
        messagebox.showwarning("Error", "Tidak ada barang apapun dalam Keranjang!")
        return
 
    metode = lblPilih2.get() #ambil metode pembayaran
    if metode == "Metode Pembayaran": #jika tidak ada pilihan maka
        messagebox.showwarning("Error", "Pilih metode pembayaran!") #muncul error
        return
    
    #hitung total disini dulu biar bisa dikirim ke formQris
    total = sum(item["subtotal"] for item in keranjang)
    persen_diskon = codeKasir.cek_diskon(total)
    nilai_diskon  = total * persen_diskon // 100
    total_bersih  = total - nilai_diskon
 
    if metode == "Qris": #jika metode Qris
        formQris(total_bersih, dikonfirmasi=lanjut_cetak)#lanjut cetak struk
        return
 
    lanjut_cetak() #jika Cash langsung cetak

def lanjut_cetak():
    #buat window Cetak
    formCetak = tk.Toplevel(root)
    formCetak.title("Cetak Struk Belanja")
    formCetak.geometry("420x500")
    formCetak.resizable(False, False)
    formCetak.configure(bg="white")
 
    #buat frame untuk dekorasi
    frame_dekor = tk.Frame(formCetak, bg="#003DA5", height=8)
    frame_dekor.pack(fill="x")
    #buat label judul
    lbl1 = tk.Label(formCetak, text="STRUK BELANJA",
            font=("Arial", 14, "bold"), bg="white", fg="#003DA5")
    lbl1.pack(pady=(12, 2))
    #buat label tanggal
    lbl2 = tk.Label(formCetak, text=dt.datetime.now().strftime("%d %B %Y"),
            font=("Arial", 9), bg="white", fg="gray")
    lbl2.pack()
    #buat label garis pemisah
    lbl3 = tk.Label(formCetak, text="-" * 52,
            font=("Courier", 9), bg="white")
    lbl3.pack(pady=(6, 2))
 
    #hitung total & diskon 
    isi_struk = ""
    total = 0
    for item in keranjang:
        isi_struk += (f"{item['nama']}\n"
                      f"{item['jumlah']} x "
                      f"{codeKasir.rupiah(item['harga'])}"
                      f" = "
                      f"{codeKasir.rupiah(item['subtotal'])}\n\n")
        total += item["subtotal"] #akumulasi total harga
 
    persen_diskon = codeKasir.cek_diskon(total) #hitung diskon berdasarkan total belanja
    nilai_diskon  = total * persen_diskon // 100
    total_bersih  = total - nilai_diskon
 
    #buat label tampilan rincian item
    lbl4 = tk.Label(formCetak, text=isi_struk, font=("Courier", 9), bg="white", fg="#000000", justify="left")
    lbl4.pack(anchor="w", padx=20)
    #label garis
    lbl5 = tk.Label(formCetak, text="-" * 52,
            font=("Courier", 9), bg="white")
    lbl5.pack(pady=(6, 2))
    #total harga sebelum diskon
    lbl6 = tk.Label(formCetak, text=f"Total          : {codeKasir.rupiah(total)}",
            font=("Courier", 10, "bold"), bg="white")
    lbl6.pack(anchor="w", padx=20)
    #label rincian diskon
    lblDiskon = tk.Label(formCetak, text=f"Diskon ({persen_diskon}%) : {codeKasir.rupiah(nilai_diskon)}",
                         font=("Courier", 10), bg="white")
    lblDiskon.pack(anchor="w", padx=20)
    #label total bersih setelah diskon
    lbl7 = tk.Label(formCetak, text=f"Total Bersih   : {codeKasir.rupiah(total_bersih)}",
            font=("Courier", 11, "bold"), bg="white", fg="#003DA5")
    lbl7.pack(anchor="w", padx=20)
    #label metode pembayaran yang dipilih
    lblMetode = tk.Label(formCetak, text=f"Metode bayar   : {lblPilih2.get()}", font=("Courier", 11), bg="white")
    lblMetode.pack(anchor="w", padx=20)
    #label baris pemisah
    lbl8 = tk.Label(formCetak, text="-" * 52,
            font=("Courier", 9), bg="white")
    lbl8.pack(pady=(6, 2))
    #label ucapan terimakasih
    lbl9 = tk.Label(formCetak, text="Terima kasih telah berbelanja!",
            font=("Arial", 10, "italic"), bg="white")
    lbl9.pack(pady=4)
    #frame dekorasi bawah
    tk.Frame(formCetak, bg="#E61E25", height=6).pack(fill="x", side="bottom")
    #buat button tutup window
    btnTutup = tk.Button(formCetak, text="Tutup", command=formCetak.destroy,
            font=("Arial", 10), bg="#003DA5", fg="white",
            relief="flat", padx=16, pady=6)
    btnTutup.pack(pady=10, side="bottom")
 
    try:
        codeKasir.laporan_penjualan()
    except Exception as e:
        messagebox.showerror("Debug", f"Error laporan: {e}") #buat laporan penjualan, simpan ke file
    keranjang.clear() #hapus isi keranjang
    refresh_keranjang() #perbarui isi keranjang

"""
function update_harga
dipanggil setiap kali produk dipilih/jml berubah
update label harga
@param *bebas agar bisa digunakan sebagai callback trace
"""
def update_harga(*bebas):
    nama_produk = lblPilih.get()#ambil produk
    item = cari_produk(nama_produk)#cari produk
    if item == None:#jika produk tdk ada maka reset ke default
        lblHargaSatuanReal.config(text="Rp 0")
        lblHargaTotalReal.config(text="Rp 0")
        return
    harga = item['harga']#harga satuan produk
    try:
        jumlah = int(entry_jml.get())#ambil jumlah entry, konversi ke int
    except:
        jumlah = 1#default ke 1 jika input tidak valid
    total = harga * jumlah #hitung total
    #tampil harga
    lblHargaSatuanReal.config(text=codeKasir.rupiah(harga))
    lblHargaTotalReal.config(text=codeKasir.rupiah(total))
    
#MAIN
keranjang = codeKasir.keranjang#referensi ke keranjang di modul backend

#buat main window
root = tk.Tk()
root.title("KlikRomushaMaret Kasir")
root.geometry("1000x700")
root.resizable(False, False)
root.configure(bg="white")

#frame untuk header
frame_header = tk.Frame(root, bg="#003DA5", height=70)
frame_header.pack(fill="x")
frame_header.pack_propagate(False)
#buat label judul
lblJudul = tk.Label(frame_header, text="KLiK RomushaMaret  —  Kasir",
         font=("Arial", 22, "bold"), fg="white", bg="#003DA5")
lblJudul.pack(expand=True)

#frame dekorasi
frame1 =tk.Frame(root, bg="#E61E25", height=10)
frame1.pack(fill="x")

#frame tengah
frame_tengah = tk.Frame(root, bg="white")
frame_tengah.pack(fill="both", expand=True, padx=30, pady=20)


produk = codeKasir.baca_produk() #baca produk
contoh_produk = [item["nama"] for item in produk]#list nama produk

#frame form di sisi kiri main window
frame_form = tk.Frame(frame_tengah, bg="white", bd=1, relief="solid",
                      padx=24, pady=20)
frame_form.pack(side="left", fill="y", ipadx=10)

#frame harga satuan
frame_harga = tk.Frame(frame_form, bg = "#f0f4ff", bd=1, relief = "solid", padx=12,pady=10)
frame_harga.grid(row=4,column=0,sticky="we",pady=(0,16))
#label harga satuan 
lblHargaSatuan = tk.Label (frame_harga, text= "Harga Satuan Barang : ", font=("Arial", 10), bg="#f0f4ff", fg="#f55555")
lblHargaSatuan.grid(row =0, column = 0,sticky="w")
lblHargaSatuanReal = tk.Label(frame_harga, text="Rp 00",  font=("Arial", 10), bg="#f0f4ff", fg="#003DA5")
lblHargaSatuanReal.grid(row=0,column=1,sticky="e", padx=(20,0))

#frame harga total
frame_harga2 = tk.Frame(frame_form, bg = "#f0f4ff", bd=1, relief = "solid", padx=12,pady=10)
frame_harga2.grid(row=5,column=0,sticky="we",pady=(0,16))
#label harga total
lblHargaTotal = tk.Label (frame_harga2, text= "Harga Total Barang : ", font=("Arial", 10), bg="#f0f4ff", fg="#f55555")
lblHargaTotal.grid(row =0, column = 0,sticky="w")
lblHargaTotalReal = tk.Label(frame_harga2, text="Rp 00",  font=("Arial", 10), bg="#f0f4ff", fg="#003DA5")
lblHargaTotalReal.grid(row=0,column=1,sticky="e", padx=(20,0))

#dropdown menu
lblPilih2 = tk.StringVar()
lblPilih2.set("Metode Pembayaran")#opsi default
pembayaran = ["Cash", "Qris"]#pilihan metode pembayaran
pembayaran1 = tk.OptionMenu(frame_form, lblPilih2, *pembayaran)#option menu dropdown
pembayaran1.config(width=34, font=("Arial",10))
pembayaran1.grid(row=6, column=0,sticky="w", pady=(0,16))

#buat button tambah
btnTambah = tk.Button(frame_form, text="  Masukan Ke Keranjang  ",font=("Arial", 10, "bold"), 
                      bg="#003DA5", fg="white",relief="flat", padx=10, pady=8, cursor="hand2", command = tambah_ke_keranjang)
btnTambah.grid(row=7, column = 0, sticky="w", pady=(0,10)
               )
#buat label tambah
lblTambah = tk.Label(frame_form, text="Pilih produk yang akan ditambahkan :",
         font=("Arial", 10), bg="white")
lblTambah.grid(row=0, column=0, sticky="w", pady=(0, 4))

#dropdown menu
lblPilih = tk.StringVar()
lblPilih.trace_add("write", update_harga)#update harga
lblPilih.set("Pilih produk")#opsin default

#dropdown isi daftar produk
opsiProduk = tk.OptionMenu(frame_form, lblPilih, *contoh_produk)
opsiProduk.config(width=34, font=("Arial",10))
opsiProduk.grid(row=1, column=0,sticky="w", pady=(0,16))
#buat label jumlah barang
lblJml = tk.Label(frame_form, text ="Masukkan jumlah barang : " )
lblJml.grid(row=2, column=0, sticky = "w")
#entry jml barang
entry_jml = tk.Entry(frame_form, width= 12, font=("Arial",11),relief="solid",bd=1)
entry_jml.insert(0,"1")#default =1
entry_jml.grid(row=3, column= 0, sticky="w", pady=(5,20))
entry_jml.bind("<KeyRelease>", update_harga)#update harga setiap user mengetik

#fame kanan
frame_kanan = tk.Frame(frame_tengah, bg = "white")
frame_kanan.pack(side="left", fill="both",expand=True,padx=(20,0))

#frame keranjang
frame_keranjang = tk.Frame(frame_kanan, bg= "#003DA5")
frame_keranjang.pack(fill="x")
#buat label judul
lblKeranjang = tk.Label(frame_keranjang, text="Keranjang Belanja", font=("Arial", 11, "bold"), fg="white", bg="#003DA5", pady=8)
lblKeranjang.pack(side="left", padx=12)

#buat listBox keranjang
listKeranjang = tk.Listbox(frame_kanan,  font=("Arial", 10),
                                bg="white", relief="flat", bd=0,
                                selectbackground="#BBDEFB",
                                highlightthickness=1,
                                highlightbackground="#cccccc")
listKeranjang.pack(fill="both",expand=True)

#frame harga total
frmTotal = tk.Frame(frame_kanan, bg="#003DA5", pady=10)
frmTotal.pack(fill="x")
#label harga total
lblTotal = tk.Label(frmTotal, text="Total   : Rp 0", font=("Arial",13,"bold"),
                    fg="#FFD700", bg="#003DA5")
lblTotal.pack(side="right",padx = 16)

#frame bawah
frame_bawah = tk.Frame(root, bg="#e8e8e8", pady=12)
frame_bawah.pack(fill="x", padx=20, pady=4)
#buat button lihat produk
btnLihatProduk = tk.Button(frame_bawah, text="Lihat Daftar Produk",font=("Arial", 10), bg="white", fg="#003DA5",relief="solid", bd=1, padx=10, pady=6, cursor="hand2", command=lihat_daftar_produk)
btnLihatProduk.pack(side="left")
#buat button cetak produk
btnCetak = tk.Button(frame_bawah, text="Cetak Struk",
         font=("Arial", 10), bg="#E61E25", fg="white",
         relief="solid", bd=1, padx=10, pady=6, cursor="hand2",
         command=formCetakStruk)
btnCetak.pack(side="left", padx=10)
#buat button lihat laporan
btnLihatLaporan = tk.Button(frame_bawah, text = "Lihat Laporan", font=("Arial",10),bg="white",fg="#003DA5", relief="solid", bd=1, padx = 10, pady =6, cursor="hand2", command=formLaporan)
btnLihatLaporan.pack(side="right", padx = 10)
#buat button haspus keranjang
btnHapusKeranjang = tk.Button(frame_bawah, text = "Hapus Keranjang", font=("Arial",10),bg="white",fg="#003DA5", relief="solid", bd=1, padx = 10, pady =6, cursor="hand2", command=hapus_keranjang)
btnHapusKeranjang.pack(side="right")
root.mainloop()#mulai event loop tkinter

"""
ISTILAH:
bg=background
fg=foreground
relief=border (tampilan 3d)
bd=borderwidth
padx=padding x (horizontal)
pady=padding y(vertikal)
cursor=ikon kursor menu
command=function yang dipanggil
side=sisi penempatan
fill=arah pengisiang ruang
expand=ekspansi fleksible
row=baris ke-
column=kolom ke-
sticky=perataan dalam sel

Made by Ahong & Theo
theo= frontend
ahong ganteng=backend
"""