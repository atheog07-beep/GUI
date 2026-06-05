class Kasir: #inisiasi class Kasir
    def __init__(self): #constructor
        self.keranjang = []
        
    #method untuk tambah belanjaan ke keranjang
    def tambah_item(self, kode, nama, harga, jumlah):
        #setiap barang dalam keranjang
        for barang in self.keranjang:
            #Jika ditemukan kode barang sama, maka update jumlah dan subtotalnya
            if barang["kode"] == kode:
                barang["jumlah"]  += jumlah
                barang["subtotal"] = barang["jumlah"] * barang["harga"]
                return
        #masukan barangnya ke keranjang
        self.keranjang.append({
            "kode": kode, "nama": nama, "harga": harga,
            "jumlah": jumlah, "subtotal": harga * jumlah
        })

    #method untuk hitung total harga
    def hitung_total(self):
        return sum(i["subtotal"] for i in self.keranjang)

    #method untuk menentukan pemberian diskon
    def diskon(self):
        total = self.hitung_total()
        if total >= 200000: return 15
        elif total >= 100000: return 10
        elif total >= 50000: return 5
        return 0

    #method untuk menghapus keranjang
    def clear_keranjang(self):
        self.keranjang.clear()
