import os
import shutil
import tempfile
import time
import threading
import platform
import datetime
import psutil
from win10toast import ToastNotifier

# Flags to enable/disable optional features
ENABLE_CACHE_CLEAN = True
ENABLE_LOG_CLEAN = True

# Initialize notifier
toaster = ToastNotifier()

# Summary counters
deleted_count = 0
skipped_count = 0

def log(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

def notify(title, msg):
    try:
        toaster.show_toast(title, msg, duration=5)
    except:
        print(f"[🔔] {title} - {msg}")

def delete_temp_files():
    global deleted_count, skipped_count
    temp_dir = tempfile.gettempdir()
    log(f"🧹 Clearing temp folder: {temp_dir}")
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception:
                skipped_count += 1
                log(f"⚠️ Locked: {file_path} - in use by another process")
        for d in dirs:
            try:
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
            except Exception as e:
                log(f"⚠️ Could not delete dir: {d} - {e}")

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

def delete_log_files(folders):
    for folder in folders:
        folder = os.path.expandvars(folder)
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(".log"):
                    try:
                        os.remove(os.path.join(folder, file))
                        log(f"[🗑️] Deleted log file: {file}")
                    except Exception as e:
                        log(f"[⚠️] Could not delete log: {file} - {e}")

def run_cleanup_all():
    delete_temp_files()
    if ENABLE_CACHE_CLEAN:
        clear_browser_cache()
    if ENABLE_LOG_CLEAN:
        log_folders = [r"%TEMP%", r"%USERPROFILE%\AppData\Local\Microsoft\Windows\WebCache"]
        delete_log_files(log_folders)
    log(f"✅ Temp cleanup completed.")
    log(f"🧼 System cleanup completed.")
    log(f"📊 Summary: Deleted {deleted_count} | Skipped (locked): {skipped_count}")
    notify("ZeroLag Cleaner", f"Cleanup done! Deleted: {deleted_count}, Skipped: {skipped_count}")

def background_cleaner(interval=1800):
    def job():
        while True:
            log("🌀 Running background cleanup...")
            run_cleanup_all()
            time.sleep(interval)
    t = threading.Thread(target=job, daemon=True)
    t.start()

if __name__ == "__main__":
    print(">>\n🚀 ZeroLag AI Cleaner starting...")
    run_cleanup_all()
    print("🌀 Agent running in background. Press Enter to stop.")
    input()
