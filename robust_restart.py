import os
import sys
import time
import subprocess
import signal
from dotenv import load_dotenv

load_dotenv()

def get_file_mod_time(filepath):
    """Get the last modification time of a file"""
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return 0

def main():
    script_to_watch = 'main.py'  # Change this to 'main2.py' if you prefer
    check_interval = 2  # Check every 2 seconds
    max_restarts = 5  # Maximum restarts per hour to prevent spam
    restart_count = 0
    last_restart_time = time.time()

    # Check if the script exists
    if not os.path.exists(script_to_watch):
        print(f"❌ Error: {script_to_watch} not found!")
        return

    # Check if token exists
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in .env file!")
        return

    # Get initial modification time
    last_mod_time = get_file_mod_time(script_to_watch)
    process = None

    def start_bot():
        nonlocal process, restart_count, last_restart_time

        # Rate limiting for restarts
        current_time = time.time()
        if current_time - last_restart_time < 3600:  # Within an hour
            restart_count += 1
            if restart_count > max_restarts:
                print(f"⚠️  Too many restarts ({restart_count}) in the last hour. Waiting...")
                time.sleep(300)  # Wait 5 minutes
                restart_count = 0
        else:
            restart_count = 0

        if process:
            print("🛑 Stopping current bot...")
            try:
                process.terminate()
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("⚠️  Bot didn't stop gracefully, forcing kill...")
                process.kill()

        print(f"🚀 Starting bot: {script_to_watch}")
        try:
            process = subprocess.Popen([sys.executable, script_to_watch])
            last_restart_time = current_time
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            return False
        return True

    # Start bot initially
    if not start_bot():
        return

    print(f"👀 Watching for changes in {script_to_watch}...")
    print(f"🔄 Check interval: {check_interval} seconds")
    print("💡 Press Ctrl+C to stop")
    print("📊 Bot will auto-restart on crashes or file changes")

    try:
        while True:
            time.sleep(check_interval)

            # Check if bot process is still running
            if process and process.poll() is not None:
                print(f"💥 Bot crashed with exit code {process.returncode}")
                print("🔄 Restarting bot...")
                if not start_bot():
                    print("❌ Failed to restart bot, exiting...")
                    break
                continue

            # Check for file changes
            current_mod_time = get_file_mod_time(script_to_watch)
            if current_mod_time > last_mod_time:
                print(f"📝 File changed at {time.ctime(current_mod_time)}")
                print("🔄 Restarting bot...")
                if start_bot():
                    last_mod_time = current_mod_time

    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher...")
        if process:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()