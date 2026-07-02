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
        print(f"❌ Lỗi: {script_to_watch} không tìm thấy!")
        return

    # Get initial modification time
    last_mod_time = get_file_mod_time(script_to_watch)
    process = None

    def start_bot():
        nonlocal process
        if process:
            print("🛑 Dừng Bot hiện tại...")
            process.terminate()
            process.wait()

        print(f"🚀 Đang bắt đầu chạy bot: {script_to_watch}")
        process = subprocess.Popen([sys.executable, script_to_watch])

    # Start bot initially
    start_bot()

    print(f"👀 Đang theo dõi các sự thay đổi của {script_to_watch}...")
    print(f"🔄 Khoảng thời gian: {check_interval} giây")
    print("💡 Ấn Ctrl + C để dừng")

    try:
        while True:
            time.sleep(check_interval)
            current_mod_time = get_file_mod_time(script_to_watch)

            if current_mod_time > last_mod_time:
                print(f"📝 File đã thay đổi lúc {time.ctime(current_mod_time)}")
                print("🔄 Đang reset Bot...")
                start_bot()
                last_mod_time = current_mod_time

    except KeyboardInterrupt:
        print("\n🛑 Đã ngừng xem...")
        if process:
            process.terminate()
            process.wait()
        print("👋 Tạm Biệt!")

if __name__ == "__main__":
    main()