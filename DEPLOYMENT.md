# Pin Hill Website - Deployment Guide

This guide covers deploying the Pin Hill website to a GCP VM using Docker.

## Prerequisites

- GCP VM with Ubuntu/Debian
- Docker and Docker Compose installed
- Git installed
- Domain name (optional, for HTTPS)

## Initial Server Setup

### 1. Install Docker and Docker Compose

```bash
# Update package list
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### 2. Clone the Repository

```bash
# Create directory for the application
sudo mkdir -p /opt/pin-hill-website
sudo chown $USER:$USER /opt/pin-hill-website

# Clone the repository
cd /opt/pin-hill-website
git clone <your-repo-url> .
```

### 3. Initial Deployment

```bash
# Build and start the containers
docker compose up -d --build

# Check container status
docker compose ps

# View logs
docker compose logs -f
```

The application will be running on port 8000.

## Manual Deployment Workflow

When you want to deploy updates:

```bash
# SSH into your GCP VM
ssh user@your-vm-ip

# Run the deployment script
cd /opt/pin-hill-website
./deploy.sh
```

The `deploy.sh` script will:
1. Pull the latest code from GitHub
2. Stop existing containers
3. Rebuild and restart containers
4. Show container status and logs

## Setting Up Nginx Reverse Proxy (Optional)

To serve your site on port 80/443 with HTTPS:

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx
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
        proxy_pass http://localhost:8000;
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
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Certbot will automatically configure HTTPS
```

Certificates will auto-renew. Test renewal:

```bash
sudo certbot renew --dry-run
```

## Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# If not using nginx, allow port 8000
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

## Monitoring and Maintenance

### View Logs

```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View logs for specific service
docker compose logs web
```

### Restart Containers

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart web
```

### Update Application

```bash
# Use the deployment script
./deploy.sh

# Or manually:
git pull origin main
docker compose up -d --build
```

### Backup

Important directories to backup:
- `/opt/pin-hill-website` - Application code
- Nginx configuration (if using): `/etc/nginx/sites-available/pinhill`

## Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs

# Check if port is already in use
sudo lsof -i :8000

# Rebuild from scratch
docker compose down
docker compose up -d --build
```

### Application not accessible

```bash
# Check if container is running
docker compose ps

# Check nginx status (if using)
sudo systemctl status nginx

# Check firewall rules
sudo ufw status
```

### Out of disk space

```bash
# Remove unused Docker images
docker system prune -a

# Check disk usage
df -h
```

## Environment Variables (Optional)

If you need environment variables, create a `.env` file:

```bash
# .env
ENVIRONMENT=production
LOG_LEVEL=info
```

Update `docker-compose.yml` to use it:

```yaml
services:
  web:
    env_file:
      - .env
```

## Automated Testing

Tests run automatically on GitHub when you push code. To run tests locally:

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=term-missing
```

## Security Best Practices

1. **Keep Docker updated**: `sudo apt update && sudo apt upgrade`
2. **Use firewall**: Only open necessary ports
3. **Regular backups**: Backup your code and configuration
4. **Monitor logs**: Check logs regularly for errors
5. **HTTPS only**: Use Let's Encrypt for free SSL certificates
6. **Update dependencies**: Keep Python packages updated

## Support

For issues or questions, check the GitHub repository or contact the maintainer.
