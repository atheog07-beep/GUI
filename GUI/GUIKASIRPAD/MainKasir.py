import tkinter as tk#impoer library tkinter
from App import App#import class App dari App.py

if __name__ == "__main__":
    root = tk.Tk() #window parent nya
    app = App(root) #panggil class app dengan root sebagai argumen
    root.mainloop() #menjalankan aplikasi
