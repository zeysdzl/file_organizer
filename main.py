import argparse
import sys
from src.organizer import FileOrganizer

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Photo and Video Organizer")
    
    # Expect the folder path as an argument from the user
    parser.add_argument("path", help="Full path of the directory to organize")
    
    args = parser.parse_args()

    # Get the path and clean it (remove quotes)
    target_path = args.path.strip('"').strip("'")

    print("------------------------------------------------")
    print("   STARTING FILE ORGANIZER")
    print("------------------------------------------------")

    try:
        organizer = FileOrganizer(target_path)
        organizer.run()
    except KeyboardInterrupt:
        print("\nOperation stopped by user.")
        sys.exit()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
