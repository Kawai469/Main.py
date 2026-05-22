import getpass
import sys
import os
from cryptography.fernet import Fernet
import base64
import hashlib

def get_master_password():
    """Prompt for master password"""
    return getpass.getpass("Enter master password to run the bot: ")

def verify_password(password, stored_hash):
    """Verify password against stored hash"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == stored_hash

def load_encrypted_token(password):
    """Load and decrypt the Discord token"""
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()

        master_password_hash = None
        encrypted_token = None

        for line in lines:
            if line.startswith('MASTER_PASSWORD_HASH='):
                master_password_hash = line.split('=', 1)[1].strip()
            elif line.startswith('DISCORD_TOKEN_ENCRYPTED='):
                encrypted_token = line.split('=', 1)[1].strip()

        if not master_password_hash or not encrypted_token:
            print("❌ Missing encrypted credentials in .env file")
            return None

        if not verify_password(password, master_password_hash):
            print("❌ Incorrect password")
            return None

        # Derive key from password
        key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
        fernet = Fernet(key)

        # Decrypt token
        decrypted_token = fernet.decrypt(encrypted_token.encode()).decode()
        return decrypted_token

    except Exception as e:
        print(f"❌ Error loading encrypted token: {e}")
        return None

def main():
    print("🔐 Bot Launcher - Password Protected")
    print("=" * 40)

    password = get_master_password()
    token = load_encrypted_token(password)

    if token:
        print("✅ Password verified. Starting bot...")
        # Set environment variable for the bot
        os.environ['DISCORD_TOKEN'] = token
        # Import and run the main bot
        try:
            import main
        except Exception as e:
            print(f"❌ Error running bot: {e}")
    else:
        print("❌ Access denied. Bot will not start.")
        sys.exit(1)

if __name__ == "__main__":
    main()