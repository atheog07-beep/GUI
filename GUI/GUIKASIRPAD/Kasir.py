class Kasir:
    def __init__(self):
        self.keranjang = []

    def tambah_item(self, kode, nama, harga, jumlah):
        for barang in self.keranjang:
            if barang["kode"] == kode:
                barang["jumlah"]  += jumlah
                barang["subtotal"] = barang["jumlah"] * barang["harga"]
                return
        self.keranjang.append({
            "kode": kode, "nama": nama, "harga": harga,
            "jumlah": jumlah, "subtotal": harga * jumlah
        })

    def hitung_total(self):
        return sum(i["subtotal"] for i in self.keranjang)

    def diskon(self):
        total = self.hitung_total()
        if total >= 200000: return 15
        elif total >= 100000: return 10
        elif total >= 50000: return 5
        return 0

    def clear_keranjang(self):
        self.keranjang.clear()
    
    