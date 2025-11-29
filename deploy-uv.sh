#!/bin/bash

# Pin Hill Website Deployment Script (uv version)
# Run this script on your GCP VM to deploy the latest version

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Navigate to project directory
cd /opt/pin-hill-website || exit 1

# Pull latest code from GitHub
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Update dependencies with uv
echo "📦 Updating dependencies..."
uv pip install -e .

# Restart systemd service
echo "🔄 Restarting service..."
sudo systemctl restart pinhill

# Show service status
echo "✅ Deployment complete! Service status:"
sudo systemctl status pinhill --no-pager

# Show recent logs
echo "📋 Recent logs:"
sudo journalctl -u pinhill -n 20 --no-pager

echo "🎉 Deployment finished successfully!"
