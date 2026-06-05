import tkinter as tk#impoer library tkinter
from App import App#import class App dari App.py

if __name__ == "__main__":#cek apakah file dijalankan langsung
    root = tk.Tk()#buka window utama 
    app = App(root)#buat objek app berparameter window utama
    root.mainloop()#mulai event loop tkinter
