# Replit Setup Script
# Run this in Replit console to set up your bot

echo "🚀 Setting up Discord Bot on Replit..."

# Install dependencies
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with:"
    echo "DISCORD_TOKEN=your_bot_token_here"
    exit 1
fi

echo "✅ Setup complete!"
echo "🎯 Run: python main.py"
echo "🌐 Your bot will be online 24/7!"