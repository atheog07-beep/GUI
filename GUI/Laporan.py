import tkinter as tk

lihatLaporan = tk.Tk()
lihatLaporan.title("Laporan Penjualan")
lihatLaporan.geometry("620x460")
lihatLaporan.configure(bg="white")

frame1 = tk.Frame(lihatLaporan, bg="#003DA5", height=8)
frame1.pack(fill="x")
lbljudul = tk.Label(lihatLaporan, text="Laporan Penjualan",font=("Arial", 12, "bold"), bg="white", fg="#003DA5")
lbljudul.pack(pady=10)

lb = tk.Listbox(lihatLaporan, font=("Arial",9),width=80, height=20,bg="white", relief="flat", highlightbackground= "#cccccc")
lb.pack(padx=16,pady=4)
btnTutup = tk.Button(lihatLaporan, text="Tutup", command= lihatLaporan.destroy, font=("Arial",10), bg="#003DA5", fg="white", relief="flat", padx=16, pady=6)
btnTutup.pack(pady=8)
lihatLaporan.mainloop()