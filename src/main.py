import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    try:
        from main_window import FaktorialApp
        
        print("🚀 Memulai Kalkulator Faktorial...")
        print("📱 Loading GUI...")
        
        app = FaktorialApp()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error: Modul tidak ditemukan - {e}")
        print("📦 Pastikan semua dependencies terinstall:")
        print("   pip install customtkinter pillow")
        
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()