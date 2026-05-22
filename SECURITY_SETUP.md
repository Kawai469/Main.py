# 🔐 Discord Bot Security Setup Guide

## Overview
Your Discord bot files are now protected with multiple layers of security:

1. **File Encryption (Windows EFS)** - Files encrypted at OS level
2. **Read-Only Protection** - Prevents accidental editing
3. **Password Authentication** - Required to run the bot
4. **Encrypted Secrets** - Token stored encrypted

## Protected Files
- `main.py` - Main bot file
- `main2.py` - Secondary bot file
- `.env` - Environment variables (encrypted token)

## How to Run the Bot

### Method 1: Secure Launcher (Recommended)
```batch
secure_run.bat
```
This will prompt for your master password and decrypt the token automatically.

### Method 2: Direct Python (Advanced)
```batch
python secure_launcher.py
```

## Setting Up Encrypted Secrets

1. Run the encryption utility:
```batch
python encrypt_secrets.py
```

2. Select option [1] to encrypt your Discord token

3. Enter your Discord bot token when prompted

4. Create a strong master password (8+ characters)

5. The script will show you what to add to `.env`:
```
MASTER_PASSWORD_HASH=your_password_hash
DISCORD_TOKEN_ENCRYPTED=encrypted_token
```

6. Add these lines to your `.env` file

## Security Features

### Windows EFS Encryption
- Files are encrypted using Windows Encrypting File System
- Only your Windows user account can decrypt them
- Protection persists even if files are copied to another drive

### Read-Only Protection
- Files cannot be accidentally modified
- To edit files, you must first remove read-only attribute:
```batch
Set-ItemProperty -Path "main.py" -Name IsReadOnly -Value $false
```

### Password Protection
- Master password required to run the bot
- Password is hashed (not stored in plain text)
- Token is encrypted with password-derived key

## Troubleshooting

### "Access Denied" Error
- Make sure you're using the same Windows account that encrypted the files
- Check if files are still encrypted: `cipher /c /s:.`

### "Incorrect Password" Error
- Verify you're entering the correct master password
- Check your `.env` file has the correct `MASTER_PASSWORD_HASH`

### Cannot Edit Files
- Remove read-only attribute first:
```batch
Set-ItemProperty -Path "main.py" -Name IsReadOnly -Value $false
```

## Security Best Practices

✅ DO:
- Use a strong master password (12+ characters, mixed case, numbers, symbols)
- Keep `.env` file safe and never commit it to git
- Back up your EFS recovery key
- Keep your Discord token secret

❌ DON'T:
- Share your MASTER_PASSWORD
- Commit encrypted tokens to git
- Use weak passwords
- Disable file encryption

## Emergency Access

If you forget your master password:
1. You cannot recover the encrypted token
2. You must generate a new Discord bot token
3. Re-encrypt with a new password using `encrypt_secrets.py`

## File Structure
```
BotDiscord/
├── main.py (encrypted, read-only)
├── main2.py (encrypted, read-only)
├── .env (encrypted, read-only)
├── secure_launcher.py (launcher script)
├── secure_run.bat (Windows batch launcher)
├── encrypt_secrets.py (encryption utility)
└── SECURITY_SETUP.md (this file)
```
