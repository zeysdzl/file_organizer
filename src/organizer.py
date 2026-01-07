import os
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

class FileOrganizer:
    def __init__(self, target_directory):
        self.target_dir = Path(target_directory)
        
        # Supported extensions (lowercase)
        self.img_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.bmp', '.tiff', '.webp'}
        self.vid_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v'}

    def get_date_taken(self, file_path):
        """
        Retrieves the date the file was taken/created.
        1. For photos, checks EXIF data (Date Time Original).
        2. If not found or if it's a video, uses the file system creation/modification time.
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

        # If no EXIF or it is a video, get modification time from file system
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp)

    def get_file_prefix(self, file_path):
        """Returns prefix (img or vid) based on file type"""
        extension = file_path.suffix.lower()
        if extension in self.img_extensions:
            return "img"
        elif extension in self.vid_extensions:
            return "vid"
        return None

    def run(self):
        if not self.target_dir.exists():
            print(f"ERROR: Directory '{self.target_dir}' not found!")
            return

        print(f"Target Directory: {self.target_dir}")
        print("Reading files and sorting by date (this may take a while)...")
        
        # 1. Collect all files (excluding hidden files)
        files = [f for f in self.target_dir.iterdir() if f.is_file() and not f.name.startswith('.')]
        
        # 2. Sort files by taken date from oldest to newest
        # This ensures the _1, _2 sequence follows chronological order.
        files_with_dates = []
        for f in files:
            date = self.get_date_taken(f)
            files_with_dates.append((f, date))
        
        # Sort by date
        files_with_dates.sort(key=lambda x: x[1])

        print(f"Total {len(files_with_dates)} files will be processed.\n")

        # Dictionary to hold daily counters
        # Ex: {'20110905': 1} -> Counter starts at 1 for September 5, 2011
        day_counters = {}
        
        count = 0
        skipped = 0

        for file_path, date_obj in files_with_dates:
            prefix = self.get_file_prefix(file_path)
            
            # Skip unsupported file types
            if not prefix:
                continue

            # Date format: YYYYMMDD
            date_key = date_obj.strftime("%Y%m%d")
            
            # Initialize or increment counter for this date
            if date_key not in day_counters:
                day_counters[date_key] = 1
            
            current_count = day_counters[date_key]
            
            # Increment counter for the next file
            day_counters[date_key] += 1

            # New name: img_YYYYMMDD_COUNTER.extension
            extension = file_path.suffix.lower()
            new_filename = f"{prefix}_{date_key}_{current_count}{extension}"
            new_path = self.target_dir / new_filename
            
            # If file already has the correct name, skip
            if new_path == file_path:
                skipped += 1
                continue
            
            # If the target name exists but it's NOT the same file (name collision)
            # Increment counter until a free slot is found
            while new_path.exists() and new_path != file_path:
                current_count = day_counters[date_key]
                day_counters[date_key] += 1
                new_filename = f"{prefix}_{date_key}_{current_count}{extension}"
                new_path = self.target_dir / new_filename

            # Rename the file
            try:
                file_path.rename(new_path)
                print(f"[OK] {file_path.name} -> {new_path.name}")
                count += 1
            except Exception as e:
                print(f"[ERROR] Could not rename {file_path.name}: {e}")

        print(f"\nOperation Completed!")
        print(f"Renamed: {count}")
        print(f"Skipped: {skipped}")
