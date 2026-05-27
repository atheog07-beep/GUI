import tkinter as tk

lihatProduk = tk.Tk()
lihatProduk.title("Daftar Produk")
lihatProduk.geometry("620x460")
lihatProduk.configure(bg="white")

frame1 = tk.Frame(lihatProduk, bg="#003DA5", height=8)
frame1.pack(fill="x")
lbljudul = tk.Label(lihatProduk, text="DAFTAR PRODUK TERSEDIA",font=("Arial", 12, "bold"), bg="white", fg="#003DA5")
lbljudul.pack(pady=10)

lb = tk.Listbox(lihatProduk, font=("Arial",9),width=80, height=20,bg="white", relief="flat", highlightbackground= "#cccccc")
lb.pack(padx=16,pady=4)
btnTutup = tk.Button(lihatProduk, text="Tutup", command= lihatProduk.destroy, font=("Arial",10), bg="#003DA5", fg="white", relief="flat", padx=16, pady=6)
btnTutup.pack(pady=8)
lihatProduk.mainloop()