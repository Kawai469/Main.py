#!/usr/bin/env python3
"""
Encrypt Secrets Utility for Discord Bot
This script encrypts your Discord token and other secrets for main.py

Usage:
    python encrypt_secrets.py
    
Then add to .env file:
    MASTER_PASSWORD=your_master_password
    DISCORD_TOKEN_ENCRYPTED=encrypted_token_here
"""

from cryptography.fernet import Fernet
import base64
import hashlib
import os

def derive_key(password: str) -> bytes:
    """Derive encryption key from password"""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_secret(secret: str, password: str) -> str:
    """Encrypt a secret with a password"""
    key = derive_key(password)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(secret.encode())
    return encrypted.decode()

def decrypt_secret(encrypted: str, password: str) -> str:
    """Decrypt a secret with a password"""
    key = derive_key(password)
    cipher = Fernet(key)
    try:
        decrypted = cipher.decrypt(encrypted.encode())
        return decrypted.decode()
    except Exception as e:
        raise ValueError(f"Decryption failed - wrong password: {e}")

def main():
    print("=" * 60)
    print("Discord Bot - Secret Encryption Utility")
    print("=" * 60)
    
    while True:
        print("\n[1] Encrypt Discord Token")
        print("[2] Decrypt secret (verify)")
        print("[3] Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            token = input("Enter your Discord bot token: ").strip()
            if not token:
                print("❌ Token cannot be empty!")
                continue
            
            password = input("Enter a master password (min 8 chars): ").strip()
            if len(password) < 8:
                print("❌ Master password must be at least 8 characters!")
                continue
            
            password_confirm = input("Confirm master password: ").strip()
            if password != password_confirm:
                print("❌ Passwords don't match!")
                continue
            
            try:
                encrypted = encrypt_secret(token, password)
                print("\n✅ Encryption successful!")
                print("\n📋 Add these to your .env file:")
                print("-" * 60)
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                print(f"MASTER_PASSWORD_HASH={password_hash}")
                print(f"DISCORD_TOKEN_ENCRYPTED={encrypted}")
                print("-" * 60)
                
                # Optional: save to .env
                save = input("\nSave to .env file? (y/n): ").lower()
                if save == 'y':
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    with open('.env', 'a') as f:
                        f.write(f"\nMASTER_PASSWORD_HASH={password_hash}\n")
                        f.write(f"DISCORD_TOKEN_ENCRYPTED={encrypted}\n")
                    print("✅ Saved to .env")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "2":
            encrypted = input("Enter encrypted secret: ").strip()
            if not encrypted:
                print("❌ Cannot be empty!")
                continue
            
            password = input("Enter master password: ").strip()
            
            try:
                decrypted = decrypt_secret(encrypted, password)
                print(f"\n✅ Decrypted: {decrypted[:20]}..." if len(decrypted) > 20 else f"\n✅ Decrypted: {decrypted}")
            except Exception as e:
                print(f"❌ {e}")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")

if __name__ == "__main__":
    main()
