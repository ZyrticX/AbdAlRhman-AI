#!/bin/bash

echo "🚀 Abd AlRahman API Deployment Script"
echo "=====================================\n"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit with deployment files"
fi

echo "📦 Available deployment options:"
echo "1. Render (Free, Recommended)"
echo "2. Railway (Free)"
echo "3. Docker Local Test"
echo "4. Manual setup instructions"

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo "\n🎯 Render Deployment:"
        echo "1. Push code to GitHub:"
        echo "   git add . && git commit -m 'Add deployment files' && git push"
        echo "2. Go to https://render.com"
        echo "3. Connect GitHub and deploy with these settings:"
        echo "   - Build: pip install -r requirements_cloud.txt"
        echo "   - Start: python api_cpu.py"
        echo "4. Update frontend URL in App.jsx"
        ;;
    2)
        echo "\n🚄 Railway Deployment:"
        echo "1. Push code to GitHub:"
        echo "   git add . && git commit -m 'Add deployment files' && git push"
        echo "2. Go to https://railway.app"
        echo "3. Deploy from GitHub repo"
        echo "4. Update frontend URL in App.jsx"
        ;;
    3)
        echo "\n🐳 Testing with Docker..."
        if command -v docker &> /dev/null; then
            echo "Building Docker image..."
            docker build -t abd-alrhman-api .
            echo "Running container on port 5000..."
            docker run -p 5000:5000 abd-alrhman-api
        else
            echo "Docker not found. Please install Docker first."
        fi
        ;;
    4)
        echo "\n📖 Opening deployment guide..."
        if command -v code &> /dev/null; then
            code DEPLOYMENT_GUIDE.md
        else
            echo "Please open DEPLOYMENT_GUIDE.md for detailed instructions"
        fi
        ;;
    *)
        echo "Invalid option. Please run the script again."
        ;;
esac

echo "\n✅ Deployment files created successfully!"
echo "📄 Check DEPLOYMENT_GUIDE.md for detailed instructions" 