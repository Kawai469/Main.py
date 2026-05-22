# Discord Bot - Run Indefinitely Setup

## 🚀 How to Run Your Bot Indefinitely

### **Option 1: Local Machine (Recommended for Development)**

#### **VS Code Debug (Easiest)**
1. Open the project in VS Code
2. Press `F5` or go to Run → Start Debugging
3. Select **"Run Discord Bot with Robust Auto-Restart"**
4. Bot runs indefinitely and auto-restarts on crashes/changes!

#### **Batch File**
- Run `robust_run.bat` for crash-resistant auto-restart
- Run `auto_run.bat` for basic auto-restart on file changes

#### **Manual**
```bash
python robust_restart.py
```

### **Option 2: 24/7 Server/VPS (Production)**

#### **Using Replit (Free & Easy)**
1. Create account at [replit.com](https://replit.com)
2. Create new Python repl
3. Upload your bot files (`main.py`, `.env`)
4. Add this to the top of `main.py`:
```python
import keep_alive
keep_alive.keep_alive()  # Add this line
```
5. Install packages: `pip install discord python-dotenv keep-alive`
6. Run the repl - it stays online 24/7!

#### **Using Railway (Free tier)**
1. Sign up at [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Set environment variables in Railway dashboard
4. Deploy - runs 24/7 with 512MB RAM free

#### **Using Heroku (Free tier)**
1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Create `requirements.txt`:
```
discord.py
python-dotenv
```
4. Create `Procfile`:
```
worker: python main.py
```
5. Deploy: `git push heroku main`

### **Option 3: Windows Service (Advanced)**

#### **Using NSSM (Non-Sucking Service Manager)**
1. Download NSSM from [nssm.cc](https://nssm.cc)
2. Install as service:
```bash
nssm install MyDiscordBot "C:\Path\To\python.exe" "C:\Path\To\main.py"
nssm set MyDiscordBot AppDirectory "C:\Path\To\BotFolder"
nssm start MyDiscordBot
```
3. Bot runs as Windows service, survives reboots!

## 🛡️ **What Makes It Run Indefinitely**

### **Error Handling Added:**
- ✅ Global error handler (`on_error`)
- ✅ Message processing wrapped in try-catch
- ✅ Automatic crash recovery
- ✅ Rate-limited restarts (max 5/hour)

### **Auto-Restart Features:**
- 🔄 Detects file changes and restarts
- 💥 Detects crashes and restarts automatically
- 📊 Prevents restart spam with rate limiting
- 🛑 Graceful shutdown on exit

### **Production Ready:**
- 🌐 Web server ping to prevent idle shutdown
- 🔑 Environment variable validation
- 📝 Comprehensive logging

## 📋 **Requirements Checklist**

- [ ] `.env` file with `DISCORD_TOKEN=your_token_here`
- [ ] All dependencies installed: `pip install discord.py python-dotenv`
- [ ] Bot code has `client.run(TOKEN)` at the end
- [ ] For 24/7: Choose a hosting platform (Replit/Railway/Heroku)

## 🚨 **Troubleshooting**

### **Bot Keeps Crashing:**
- Check console output for error messages
- Verify `DISCORD_TOKEN` is correct
- Ensure bot has proper permissions in Discord

### **Auto-Restart Not Working:**
- Check if Python is in PATH
- Verify file paths in scripts
- Look for permission errors

### **High CPU/Memory Usage:**
- Add delays between operations
- Implement command cooldowns
- Monitor with Task Manager

## 🎯 **Best Practices for 24/7 Bots**

1. **Logging**: Add proper logging instead of print statements
2. **Database**: Use a database for persistent data
3. **Monitoring**: Set up uptime monitoring (UptimeRobot, etc.)
4. **Backups**: Regular backups of important data
5. **Updates**: Keep dependencies updated
6. **Security**: Use environment variables for sensitive data

---

**Your bot is now ready to run indefinitely! 🎉**