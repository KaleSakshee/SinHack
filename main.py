from core.fixer import background_cleaner

def main():
    print("🚀 ZeroLag AI Cleaner starting...")
    background_cleaner(interval=600)  # every 10 mins
    input("🌀 Agent running in background. Press Enter to stop.\n")

if __name__ == "__main__":
    main()
