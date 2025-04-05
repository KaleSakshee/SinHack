import os, shutil, tempfile, time, threading, platform, datetime

def log(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

def clear_temp():
    temp_dir = tempfile.gettempdir()
    log(f"🧹 Clearing temp folder: {temp_dir}")

    try:
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except Exception as e:
                    log(f"⚠️ Could not delete file: {f} - {e}")
            for d in dirs:
                try:
                    shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                except Exception as e:
                    log(f"⚠️ Could not delete dir: {d} - {e}")

        log("✅ Temp cleanup completed.")
        return True
    except Exception as e:
        log(f"❌ Error in cleanup: {e}")
        return False

def run_cleanup_all():
    clear_temp()
    # Add other cleanup modules here later
    log("🧼 System cleanup completed.\n")

def background_cleaner(interval=1800):  # default every 30 mins
    def job():
        while True:
            log("🌀 Running background cleanup...")
            run_cleanup_all()
            time.sleep(interval)

    t = threading.Thread(target=job, daemon=True)
    t.start()
