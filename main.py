from core.fixer import background_cleaner

def main():
    print("🚀 ZeroLag AI Cleaner starting...")
    background_cleaner(interval=600, dry_run=False)  # Set dry_run=True to preview only
    input("🌀 Agent running in background. Press Enter to stop.\n")

if __name__ == "__main__":
    main()
