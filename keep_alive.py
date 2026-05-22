from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return "Bot is running! 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """
    Creates a Flask server to prevent the bot from going idle.
    Call this function before client.run() in your main bot file.
    """
    t = Thread(target=run)
    t.start()
    print("🌐 Keep-alive server started on port 8080")

if __name__ == "__main__":
    keep_alive()
    # Keep the thread alive
    while True:
        time.sleep(60)