import tkinter as tk

formCetak = tk.Tk()
formCetak.title("Cetak Struk Belanja")
formCetak.geometry("420x500")
formCetak.resizable(False, False)
formCetak.configure(bg="white")        

frame_dekor = tk.Frame(formCetak, bg="#003DA5", height=8)
frame_dekor.pack(fill="x")
lbl1 = tk.Label(formCetak, text="STRUK BELANJA",
            font=("Arial", 14, "bold"), bg="white", fg="#003DA5")
lbl1.pack(pady=(12, 2))
lbl2 = tk.Label(formCetak, text="18 Juni 2067",
            font=("Arial", 9), bg="white", fg="gray")
lbl2.pack()
lbl3 = tk.Label(formCetak, text="-" * 52,
            font=("Courier", 9), bg="white")
lbl3.pack(pady=(6, 2))

lbl4 = tk.Label(formCetak, text="(isi struk dari keranjang)",
            font=("Courier", 9), bg="white", fg="#000000")
lbl4.pack(anchor="w", padx=20)
lbl5 = tk.Label(formCetak, text="-" * 52,
            font=("Courier", 9), bg="white")
lbl5.pack(pady=(6, 2))
lbl6 = tk.Label(formCetak, text="Total          : Rp15.000-,",
            font=("Courier", 10, "bold"), bg="white")
lbl6.pack(anchor="w", padx=20)
lbl7 = tk.Label(formCetak, text="Total Bersih   : Rp15.000-,",
            font=("Courier", 11, "bold"), bg="white", fg="#003DA5")
lbl7.pack(anchor="w", padx=20)
lbl8 = tk.Label(formCetak, text="-" * 52,
            font=("Courier", 9), bg="white")
lbl8.pack(pady=(6, 2))
lbl9 = tk.Label(formCetak, text="Terima kasih telah berbelanja!",
            font=("Arial", 10, "italic"), bg="white")
lbl9.pack(pady=4)

frameanjay = tk.Frame(formCetak, bg="#E61E25", height=6).pack(fill="x", side="bottom")
btnTutup = tk.Button(formCetak, text="Tutup", command=formCetak.destroy,
            font=("Arial", 10), bg="#003DA5", fg="white",
            relief="flat", padx=16, pady=6)
btnTutup.pack(pady=10, side="bottom")
formCetak.mainloop()