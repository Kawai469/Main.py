import os
import sys
import time
import subprocess
import signal

def get_file_mod_time(filepath):
    """Get the last modification time of a file"""
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return 0

def main():
    script_to_watch = 'main.py'  # Change this to 'main2.py' if you prefer
    check_interval = 2  # Check every 2 seconds

    # Check if the script exists
    if not os.path.exists(script_to_watch):
        print(f"❌ Error: {script_to_watch} not found!")
        return

    # Get initial modification time
    last_mod_time = get_file_mod_time(script_to_watch)
    process = None

    def start_bot():
        nonlocal process
        if process:
            print("🛑 Stopping current bot...")
            process.terminate()
            process.wait()

        print(f"🚀 Starting bot: {script_to_watch}")
        process = subprocess.Popen([sys.executable, script_to_watch])

    # Start bot initially
    start_bot()

    print(f"👀 Watching for changes in {script_to_watch}...")
    print(f"🔄 Check interval: {check_interval} seconds")
    print("💡 Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(check_interval)
            current_mod_time = get_file_mod_time(script_to_watch)

            if current_mod_time > last_mod_time:
                print(f"📝 File changed at {time.ctime(current_mod_time)}")
                print("🔄 Restarting bot...")
                start_bot()
                last_mod_time = current_mod_time

    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher...")
        if process:
            process.terminate()
            process.wait()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()