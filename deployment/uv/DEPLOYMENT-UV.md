# Pin Hill Website - Deployment with uv

This guide covers deploying the Pin Hill website to a GCP VM using `uv` (without Docker).

## Prerequisites

- GCP VM (e2-micro works great!)
- Ubuntu/Debian OS
- Domain name (optional, for HTTPS)

## Initial Server Setup

### 1. Install uv and Python

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.bashrc

# Verify
uv --version
python3.12 --version
```

### 2. Clone the Repository

```bash
# Create directory for the application
sudo mkdir -p /opt/pin-hill-website
sudo chown $USER:$USER /opt/pin-hill-website

# Clone the repository
cd /opt/pin-hill-website
git clone git@github.com:keiron-stoddart/harvard-pin-hill.git .
```

### 3. Set Up Virtual Environment

```bash
cd /opt/pin-hill-website

# Create virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

### 4. Test the Application

```bash
# Run manually to test
uvicorn main:app --host 0.0.0.0 --port 8000

# Visit http://your-server-ip:8000
# Press Ctrl+C to stop
```

## Set Up as a System Service

Create a systemd service to run the app automatically:

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/pinhill.service
```

Add this content:

```ini
[Unit]
Description=Pin Hill Website
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/opt/pin-hill-website
Environment="PATH=/opt/pin-hill-website/.venv/bin"
ExecStart=/opt/pin-hill-website/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Replace `YOUR_USERNAME` with your actual username!**

### 2. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable pinhill

# Start service
sudo systemctl start pinhill

# Check status
sudo systemctl status pinhill
```

## Manual Deployment Script

Create a simple deployment script:

```bash
nano /opt/pin-hill-website/deploy-uv.sh
```

Add this content:

```bash
#!/bin/bash
set -e

echo "🚀 Starting deployment..."

cd /opt/pin-hill-website

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Activate virtual environment
source .venv/bin/activate

# Update dependencies
echo "📦 Updating dependencies..."
uv pip install -e .

# Restart service
echo "🔄 Restarting service..."
sudo systemctl restart pinhill

# Show status
echo "✅ Deployment complete! Service status:"
sudo systemctl status pinhill --no-pager

echo "📋 Recent logs:"
sudo journalctl -u pinhill -n 20 --no-pager
```

Make it executable:

```bash
chmod +x /opt/pin-hill-website/deploy-uv.sh
```

## Deployment Workflow

When you want to deploy updates:

```bash
# SSH into your GCP VM
ssh user@your-vm-ip

# Run deployment script
cd /opt/pin-hill-website
./deploy-uv.sh
```

## Set Up Nginx Reverse Proxy

To serve on port 80/443 with HTTPS:

### 1. Install Nginx

```bash
sudo apt install -y nginx
```

### 2. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/pinhill
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/pinhill /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Set Up HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH

# Enable firewall
sudo ufw enable
```

## Monitoring and Maintenance

### View Logs

```bash
# View service logs
sudo journalctl -u pinhill -f

# View recent logs
sudo journalctl -u pinhill -n 50

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Service Management

```bash
# Check status
sudo systemctl status pinhill

# Restart service
sudo systemctl restart pinhill

# Stop service
sudo systemctl stop pinhill

# Start service
sudo systemctl start pinhill

# View service configuration
sudo systemctl cat pinhill
```

### Update Application

```bash
# Use the deployment script
./deploy-uv.sh

# Or manually:
cd /opt/pin-hill-website
git pull origin main
source .venv/bin/activate
uv pip install -e .
sudo systemctl restart pinhill
```

## Troubleshooting

### Service won't start

```bash
# Check logs
sudo journalctl -u pinhill -n 50

# Check if port is in use
sudo lsof -i :8000

# Test manually
cd /opt/pin-hill-website
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Application not accessible

```bash
# Check if service is running
sudo systemctl status pinhill

# Check nginx status
sudo systemctl status nginx

# Check firewall
sudo ufw status
```

### Memory issues

```bash
# Check memory usage
free -h

# Check process memory
ps aux | grep uvicorn
```

## Performance Tuning for e2-micro

Since you have limited resources:

```bash
# Edit service file
sudo nano /etc/systemd/system/pinhill.service
```

Add workers limit:

```ini
ExecStart=/opt/pin-hill-website/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

Reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart pinhill
```

## Backup

Important files to backup:
- `/opt/pin-hill-website` - Application code
- `/etc/systemd/system/pinhill.service` - Service configuration
- `/etc/nginx/sites-available/pinhill` - Nginx configuration

## Security Best Practices

1. **Keep system updated**: `sudo apt update && sudo apt upgrade`
2. **Use firewall**: Only open necessary ports (22, 80, 443)
3. **HTTPS only**: Use Let's Encrypt for SSL
4. **Regular backups**: Backup configuration and code
5. **Monitor logs**: Check logs regularly for errors

## Comparison: uv vs Docker

| Feature | uv | Docker |
|---------|-----|--------|
| Memory usage | ~200-300 MB | ~400-500 MB |
| Deployment speed | Fast | Slower (build time) |
| Complexity | Simple | More complex |
| Isolation | Virtual env | Container |
| Best for | Small VMs | Multi-service apps |

For your e2-micro and simple website, **uv is the better choice**!
