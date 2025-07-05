#!/bin/bash

echo "🚀 Abd AlRahman AI - Hetzner Server Deployment"
echo "============================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_status "Starting deployment on Hetzner server..."

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
print_status "Installing Python and system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx

# Create application directory
print_status "Setting up application directory..."
sudo mkdir -p /opt/abd-alrhman-ai
sudo chown $USER:$USER /opt/abd-alrhman-ai
cd /opt/abd-alrhman-ai

# Clone repository (if not already present)
if [ ! -d ".git" ]; then
    print_status "Cloning repository..."
    git clone https://github.com/ZyrticX/AbdAlRhman-AI.git .
else
    print_status "Repository exists, pulling latest changes..."
    git pull origin main
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip

# Check if GPU is available
if command -v nvidia-smi &> /dev/null; then
    print_status "GPU detected! Installing GPU version..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    API_FILE="api.py"
else
    print_status "No GPU detected. Installing CPU version..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    API_FILE="api_cpu.py"
fi

# Install other requirements
pip install flask flask-cors transformers accelerate einops requests beautifulsoup4 python-dateutil

# Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/abd-alrhman-ai.service > /dev/null <<EOF
[Unit]
Description=Abd AlRahman AI API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/abd-alrhman-ai
Environment=PATH=/opt/abd-alrhman-ai/venv/bin
Environment=PYTHONPATH=/opt/abd-alrhman-ai
ExecStart=/opt/abd-alrhman-ai/venv/bin/python $API_FILE
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
print_status "Starting Abd AlRahman AI service..."
sudo systemctl daemon-reload
sudo systemctl enable abd-alrhman-ai
sudo systemctl start abd-alrhman-ai

# Configure Nginx
print_status "Configuring Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/abd-alrhman-ai > /dev/null <<EOF
server {
    listen 80;
    server_name YOUR_DOMAIN_HERE;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/abd-alrhman-ai /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Setup firewall
print_status "Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

print_status "✅ Deployment completed!"
echo ""
echo "🔧 Next steps:"
echo "1. Update the domain in Nginx config: sudo nano /etc/nginx/sites-available/abd-alrhman-ai"
echo "2. Replace YOUR_DOMAIN_HERE with your actual domain"
echo "3. Get SSL certificate: sudo certbot --nginx -d yourdomain.com"
echo "4. Check service status: sudo systemctl status abd-alrhman-ai"
echo "5. View logs: sudo journalctl -u abd-alrhman-ai -f"
echo ""
echo "🌐 Your API will be available at: http://your-domain.com"
echo "📊 Health check: http://your-domain.com/health"
echo ""
print_status "Abd AlRahman AI is now running on your Hetzner server!" 