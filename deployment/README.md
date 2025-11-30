# Deployment Resources

This directory contains all deployment-related files for the Pin Hill website.

## Deployment Options

### Option 1: uv + systemd (Recommended for small VMs)
- **Guide**: [DEPLOYMENT-UV.md](./DEPLOYMENT-UV.md)
- **Script**: [deploy-uv.sh](./deploy-uv.sh)
- **Memory**: ~200-300 MB
- **Best for**: e2-micro or similar small instances

### Option 2: Docker
- **Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Script**: [deploy.sh](./deploy.sh)
- **Files**: [Dockerfile](./Dockerfile), [docker-compose.yml](./docker-compose.yml)
- **Memory**: ~400-500 MB
- **Best for**: Larger VMs or multi-service applications

## Quick Start

1. Choose your deployment method
2. Follow the corresponding guide
3. Use the deployment script for updates

## Files

- `DEPLOYMENT-UV.md` - Complete guide for uv-based deployment
- `DEPLOYMENT.md` - Complete guide for Docker-based deployment
- `deploy-uv.sh` - Deployment script for uv setup
- `deploy.sh` - Deployment script for Docker setup
- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration
