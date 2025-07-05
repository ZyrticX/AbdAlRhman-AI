# 🚀 Abd AlRahman AI - Hetzner Server Deployment Guide

## Quick Deploy (Automated)

### Step 1: Upload Files to Your Server
```bash
# On your local machine
git add .
git commit -m "Add Hetzner deployment files"
git push origin main

# On your Hetzner server
git clone https://github.com/ZyrticX/AbdAlRhman-AI.git
cd AbdAlRhman-AI
chmod +x deploy_hetzner.sh
./deploy_hetzner.sh
```

### Step 2: Configure Domain
```bash
# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/abd-alrhman-ai
# Replace YOUR_DOMAIN_HERE with your actual domain

# Restart Nginx
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

## Manual Deployment (Step by Step)

### Prerequisites
- Ubuntu 20.04+ or Debian 11+
- Root or sudo access
- Domain name (optional but recommended)

### Step 1: System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx htop
```

### Step 2: Application Setup
```bash
# Create app directory
sudo mkdir -p /opt/abd-alrhman-ai
sudo chown $USER:$USER /opt/abd-alrhman-ai
cd /opt/abd-alrhman-ai

# Clone repository
git clone https://github.com/ZyrticX/AbdAlRhman-AI.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
```

### Step 3: Install PyTorch
```bash
# For GPU servers (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CPU-only servers
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Step 4: Install Other Dependencies
```bash
pip install flask flask-cors transformers accelerate einops requests beautifulsoup4 python-dateutil
```

### Step 5: Create Systemd Service
```bash
sudo nano /etc/systemd/system/abd-alrhman-ai.service
```

Add this content:
```ini
[Unit]
Description=Abd AlRahman AI API
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/opt/abd-alrhman-ai
Environment=PATH=/opt/abd-alrhman-ai/venv/bin
Environment=PYTHONPATH=/opt/abd-alrhman-ai
ExecStart=/opt/abd-alrhman-ai/venv/bin/python api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Note**: Replace `YOUR_USERNAME` with your actual username and use `api.py` for GPU or `api_cpu.py` for CPU.

### Step 6: Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable abd-alrhman-ai
sudo systemctl start abd-alrhman-ai

# Check status
sudo systemctl status abd-alrhman-ai
```

### Step 7: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/abd-alrhman-ai
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for AI model responses
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
```

### Step 8: Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/abd-alrhman-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Step 10: SSL Certificate (Optional)
```bash
sudo certbot --nginx -d your-domain.com
```

## Testing Your Deployment

### Check Service Status
```bash
sudo systemctl status abd-alrhman-ai
sudo journalctl -u abd-alrhman-ai -f
```

### Test API Endpoints
```bash
# Health check
curl http://your-domain.com/health

# Test chat
curl -X POST http://your-domain.com/api \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Updating Your API

```bash
cd /opt/abd-alrhman-ai
git pull origin main
sudo systemctl restart abd-alrhman-ai
```

## Monitoring

### View Logs
```bash
sudo journalctl -u abd-alrhman-ai -f
```

### Check Resource Usage
```bash
htop
nvidia-smi  # For GPU servers
```

### Check Service
```bash
sudo systemctl status abd-alrhman-ai
```

## Troubleshooting

### Common Issues

1. **Service won't start**
   ```bash
   sudo journalctl -u abd-alrhman-ai -n 50
   ```

2. **Permission errors**
   ```bash
   sudo chown -R $USER:$USER /opt/abd-alrhman-ai
   ```

3. **Memory issues**
   - Use `api_cpu.py` for CPU deployment
   - Consider smaller model alternatives

4. **Port conflicts**
   ```bash
   sudo netstat -tlnp | grep :5000
   ```

### Performance Optimization

1. **For GPU servers**: Use `api.py` (original version)
2. **For CPU servers**: Use `api_cpu.py` (optimized version)
3. **Memory management**: Monitor with `htop`
4. **Model caching**: First request takes longer (model loading)

## Server Specifications

### Recommended Specs

**CPU Version:**
- 4+ CPU cores
- 8GB+ RAM
- 20GB+ storage

**GPU Version:**
- NVIDIA GPU with 8GB+ VRAM
- 16GB+ RAM
- 50GB+ storage

### Hetzner Server Types

- **CAX21**: 4 vCPU, 8GB RAM (good for CPU version)
- **CCX33**: 8 vCPU, 32GB RAM (excellent for CPU version)
- **CX41**: 4 vCPU, 16GB RAM (good for CPU version)

## Security Considerations

1. **Rate limiting**: Add nginx rate limiting
2. **API authentication**: Consider adding API keys
3. **Regular updates**: Keep system and dependencies updated
4. **Backup**: Regular backups of your customizations

Your Abd AlRahman AI is now running on your dedicated Hetzner server! 🎉 