📁 File Organizer / Dosya Düzenleyici
English | Türkçe

<a name="türkçe"></a>
🇹🇷 Türkçe

Düzenleme takıntısı olan biri oalrak, dosyalarımı düzenleyebildiğim bir Python aracı.
Fotoğraf ve videolarınızı oluşturulma tarihlerine göre otomatik olarak düzenler ve yeniden adlandırır.

Özellikler

Kronolojik İsimlendirme: Dosyaları img_YYYYMMDD_X veya vid_YYYYMMDD_X formatında yeniden adlandırır.

Akıllı Sıralama: Dosyaları önce tarihe göre sıralar, ardından o gün çekilen fotoğraflara sırasıyla numara (1, 2, 3...) verir.

EXIF Desteği: Mümkün olduğunda dosya oluşturma tarihi yerine fotoğrafın içindeki gerçek "Çekilme Tarihi"ni kullanır.

Güvenli: İsim çakışmalarını otomatik yönetir ve dosyaları kontrol etmeden asla üzerine yazmaz.

Kurulum

Projeyi indirin:

git clone [https://github.com/zeysdzl/file_organizer.git](https://github.com/zeysdzl/file_organizer.git)
cd file_organizer


Sanal ortamı kurun ve gereksinimleri yükleyin:

python -m venv venv
# venv'i aktifleştirin:
# Windows: .\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt


Kullanım

main.py dosyasını hedef klasör yolu ile birlikte çalıştırın:

python main.py "C:\Fotograflarim\Yolu"


<a name="english"></a>

🇬🇧 English

A Python tool that automatically organizes and renames your photos and videos based on their creation date (EXIF data or file timestamp).

Features

Chronological Naming: Renames files to img_YYYYMMDD_X or vid_YYYYMMDD_X.

Intelligent Sorting: Sorts files by date first, then assigns sequential numbers (1, 2, 3...) for each day.

EXIF Support: Uses the actual "Date Taken" from photo metadata instead of the file creation date whenever possible.

Safe: Handles duplicate names automatically and never overwrites files without checking.

Installation

Clone the repository:

git clone [https://github.com/zeysdzl/file_organizer.git](https://github.com/zeysdzl/file_organizer.git)
cd file_organizer


Create a virtual environment and install dependencies:

python -m venv venv
# Activate venv:
# Windows: .\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt


Usage

Run the main.py script with the target directory path:

python main.py "C:\Path\To\Your\Photos"