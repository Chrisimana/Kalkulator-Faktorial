import math

class FaktorialCalculator:
    @staticmethod
    def hitung_faktorial(n):
        """Menghitung faktorial dengan penjabaran"""
        if n < 0:
            raise ValueError("Angka tidak boleh negatif")
        
        if n > 1000:  # Batas untuk menghindari overload
            raise ValueError("Angka terlalu besar untuk dihitung")
        
        if n == 0 or n == 1:
            return 1, "1"
        
        hasil = 1
        penjabaran = []
        
        # Menghitung faktorial dan menyimpan prosesnya
        for i in range(n, 0, -1):
            hasil *= i
            penjabaran.append(str(i))
        
        # Membuat string penjabaran
        penjabaran_str = " × ".join(penjabaran)
        
        return hasil, penjabaran_str
    
    @staticmethod
    def format_angka_besar(angka):
        """Memformat angka besar menjadi string yang mudah dibaca"""
        if angka < 1000000:
            return str(angka)
        
        # Untuk angka sangat besar, tampilkan dalam notasi ilmiah
        return f"{angka:.2e}".replace("e+", " × 10^")
    
    @staticmethod
    def hitung_faktorial_approximasi(n):
        """Menghitung aproksimasi faktorial menggunakan rumus Stirling"""
        if n <= 0:
            return 1
        
        # Rumus Stirling: n! ≈ √(2πn) * (n/e)^n
        import math
        return math.sqrt(2 * math.pi * n) * (n / math.e) ** n