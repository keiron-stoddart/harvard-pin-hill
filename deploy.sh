#!/bin/bash

# Pin Hill Website Deployment Script
# Run this script on your GCP VM to deploy the latest version

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Navigate to project directory
cd /opt/pin-hill-website || exit 1

# Pull latest code from GitHub
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Rebuild and start containers
echo "🔨 Building and starting containers..."
docker-compose up -d --build

# Show container status
echo "✅ Deployment complete! Container status:"
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo "🎉 Deployment finished successfully!"
