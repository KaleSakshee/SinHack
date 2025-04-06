import os
import time
import threading

def clear_temp_folder(temp_path):
    deleted_count = 0
    locked_count = 0

    for filename in os.listdir(temp_path):
        file_path = os.path.join(temp_path, filename)

        # Skip folders
        if os.path.isdir(file_path):
            continue

        try:
            os.remove(file_path)
            print(f"✅ Deleted: {file_path}")
            deleted_count += 1
        except PermissionError:
            # Retry after short delay
            time.sleep(1)
            try:
                os.remove(file_path)
                print(f"✅ Deleted on retry: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"⚠️ Locked: {file_path} - {e}")
                locked_count += 1
        except Exception as e:
            print(f"⚠️ Failed: {file_path} - {e}")
            locked_count += 1

    print(f"\n📊 Summary: Deleted {deleted_count} | Skipped (locked): {locked_count}\n")

def background_cleaner(interval=600):
    temp_path = os.environ.get('TEMP') or "C:\\Users\\ASUS\\AppData\\Local\\Temp"

    def run_cleaner():
        while True:
            print("🧹 Running cleanup...")
            clear_temp_folder(temp_path)
            time.sleep(interval)

    thread = threading.Thread(target=run_cleaner, daemon=True)
    thread.start()
