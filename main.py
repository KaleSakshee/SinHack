from core.fixer import background_cleaner

def main():
    print("🚀 ZeroLag AI Cleaner starting...")
    background_cleaner(interval=600)  # runs every 10 minutes
    input("🌀 Agent running in background. Press Enter to stop.\n")

if __name__ == "__main__":
    main()
