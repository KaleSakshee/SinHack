import os
import shutil
import tempfile
import time
import threading
from datetime import datetime
from win10toast import ToastNotifier

# Flags to enable/disable optional features
ENABLE_CACHE_CLEAN = True
ENABLE_LOG_CLEAN = True

# Initialize notifier
toaster = ToastNotifier()

# Summary counters
deleted_count = 0
skipped_count = 0

# Log file for tracking deletions
LOG_FILE = "cleanup_log.txt"

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")

def delete_temp_files(temp_path, dry_run=False):
    global deleted_count, skipped_count
    deleted = 0
    locked = 0

    for root, dirs, files in os.walk(temp_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if dry_run:
                    print(f"🔍 DRY RUN: Would delete {file_path}")
                else:
                    os.remove(file_path)
                    deleted += 1
                    log(f"[🗑️] Deleted temp file: {file_path}")
            except PermissionError:
                print(f"⚠️ Locked: {file_path} - in use by another process")
                locked += 1
            except Exception as e:
                print(f"❌ Error deleting {file_path}: {e}")
                locked += 1

    return deleted, locked

def clear_browser_cache():
    cache_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache")
    ]
    for path in cache_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                try:
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                        log(f"[🧹] Cleared cache file: {full_path}")
                except Exception as e:
                    log(f"[⚠️] Could not delete: {file} - {e}")

def show_notification(deleted, locked):
    toaster.show_toast("ZeroLag Cleaner",
                       f"Cleanup done! 🧹 Deleted: {deleted}, Locked: {locked}",
                       duration=6,
                       icon_path=None,
                       threaded=True)

def run_cleanup_all(dry_run=False):
    global deleted_count, skipped_count
    temp_dir = tempfile.gettempdir()
    log(f"🧹 Clearing temp folder: {temp_dir}")
    deleted, locked = delete_temp_files(temp_dir, dry_run=dry_run)
    deleted_count += deleted
    skipped_count += locked

    if ENABLE_CACHE_CLEAN:
        clear_browser_cache()

    log(f"✅ Temp cleanup completed.")
    log(f"🧼 System cleanup completed.")
    log(f"📊 Summary: Deleted {deleted_count} | Skipped (locked): {skipped_count}")
    show_notification(deleted_count, skipped_count)

def background_cleaner(interval=1800, dry_run=False):
    def job():
        while True:
            log("🌀 Running background cleanup...")
            run_cleanup_all(dry_run=dry_run)
            time.sleep(interval)

    t = threading.Thread(target=job, daemon=True)
    t.start()

if __name__ == "__main__":
    print(">>\n🚀 ZeroLag AI Cleaner starting...")
    run_cleanup_all()
    print("🌀 Agent running in background. Press Enter to stop.")
    input()
