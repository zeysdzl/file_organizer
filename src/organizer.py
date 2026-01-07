import os
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

class FileOrganizer:
    def __init__(self, target_directory):
        self.target_dir = Path(target_directory)
        
        # Desteklenen uzantılar (küçük harf)
        self.img_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.bmp', '.tiff', '.webp'}
        self.vid_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v'}

    def get_date_taken(self, file_path):
        """
        Dosyanın tarihini bulur.
        1. Fotoğraflar için EXIF verisine (çekildiği tarih) bakar.
        2. Bulamazsa veya videoysa dosya oluşturma/değiştirme tarihine bakar.
        """
        extension = file_path.suffix.lower()

        if extension in self.img_extensions:
            try:
                with Image.open(file_path) as image:
                    exifdata = image.getexif()
                    if exifdata:
                        for tag_id in exifdata:
                            tag = TAGS.get(tag_id, tag_id)
                            if tag == 'DateTimeOriginal':
                                date_str = exifdata.get(tag_id)
                                if date_str:
                                    # Format: YYYY:MM:DD HH:MM:SS
                                    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            except Exception:
                pass

        # EXIF yoksa veya videoysa dosya sistemindeki değiştirilme tarihini al
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp)

    def get_file_prefix(self, file_path):
        """Dosya türüne göre önek (img veya vid) döndürür"""
        extension = file_path.suffix.lower()
        if extension in self.img_extensions:
            return "img"
        elif extension in self.vid_extensions:
            return "vid"
        return None

    def run(self):
        if not self.target_dir.exists():
            print(f"HATA: '{self.target_dir}' klasörü bulunamadı!")
            return

        print(f"Hedef Klasör: {self.target_dir}")
        print("Dosyalar okunuyor ve tarihlerine göre sıralanıyor (bu biraz sürebilir)...")
        
        # 1. Tüm dosyaları topla (Gizli dosyalar hariç)
        files = [f for f in self.target_dir.iterdir() if f.is_file() and not f.name.startswith('.')]
        
        # 2. Dosyaları çekilme tarihine göre eskiden yeniye sırala
        # Bu sayede _1, _2 sıralaması sabah çekilenden akşama doğru gider.
        files_with_dates = []
        for f in files:
            date = self.get_date_taken(f)
            files_with_dates.append((f, date))
        
        # Tarihe göre (eskiden yeniye) sırala
        files_with_dates.sort(key=lambda x: x[1])

        print(f"Toplam {len(files_with_dates)} dosya işlenecek.\n")

        # Günlük sayaçları tutacak sözlük
        # Örn: {'20110905': 1} -> 5 Eylül 2011 için sayaç 1'den başlar
        day_counters = {}
        
        count = 0
        skipped = 0

        for file_path, date_obj in files_with_dates:
            prefix = self.get_file_prefix(file_path)
            
            # Desteklenmeyen dosya türü ise atla
            if not prefix:
                continue

            # Tarih formatı: YYYYMMDD
            date_key = date_obj.strftime("%Y%m%d")
            
            # Bu tarih için sayaç başlat veya varsa al
            if date_key not in day_counters:
                day_counters[date_key] = 1
            
            current_count = day_counters[date_key]
            
            # Sayacı bir sonraki dosya için artırıyoruz
            day_counters[date_key] += 1

            # Yeni isim: img_YYYYMMDD_SAYAÇ.uzanti
            extension = file_path.suffix.lower()
            new_filename = f"{prefix}_{date_key}_{current_count}{extension}"
            new_path = self.target_dir / new_filename
            
            # Eğer dosya zaten istenen isimdeyse işlem yapma
            if new_path == file_path:
                skipped += 1
                continue
            
            # Eğer hedef isimde BAŞKA bir dosya varsa (isim çakışması)
            # Sayacı artırarak boş yer bulana kadar devam et
            while new_path.exists() and new_path != file_path:
                current_count = day_counters[date_key]
                day_counters[date_key] += 1
                new_filename = f"{prefix}_{date_key}_{current_count}{extension}"
                new_path = self.target_dir / new_filename

            # Dosyayı yeniden adlandır
            try:
                file_path.rename(new_path)
                print(f"[OK] {file_path.name} -> {new_path.name}")
                count += 1
            except Exception as e:
                print(f"[HATA] {file_path.name} değiştirilemedi: {e}")

        print(f"\nİşlem Tamamlandı!")
        print(f"Yeniden Adlandırılan: {count}")
        print(f"Pas Geçilen: {skipped}")