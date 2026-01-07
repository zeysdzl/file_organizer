import argparse
import sys
from src.organizer import FileOrganizer

def main():
    # Komut satırı argümanlarını ayarla
    parser = argparse.ArgumentParser(description="Fotoğraf ve Video Düzenleyici")
    
    # Kullanıcıdan klasör yolunu argüman olarak bekliyoruz
    parser.add_argument("path", help="Düzenlenecek klasörün tam yolu")
    
    args = parser.parse_args()

    # Yolu al ve temizle (tırnak işaretlerini temizler)
    target_path = args.path.strip('"').strip("'")

    print("------------------------------------------------")
    print("   DOSYA DÜZENLEYİCİ BAŞLATILIYOR")
    print("------------------------------------------------")

    try:
        organizer = FileOrganizer(target_path)
        organizer.run()
    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit()
    except Exception as e:
        print(f"\nBeklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    main()