# Deployment Resources

This directory contains all deployment-related files for the Pin Hill website.

## Deployment Options

### Option 1: uv + systemd (Recommended for small VMs)
- **Directory**: [uv/](./uv/)
- **Guide**: [uv/DEPLOYMENT-UV.md](./uv/DEPLOYMENT-UV.md)
- **Script**: [uv/deploy-uv.sh](./uv/deploy-uv.sh)
- **Memory**: ~200-300 MB
- **Best for**: e2-micro or similar small instances

### Option 2: Docker
- **Directory**: [docker/](./docker/)
- **Guide**: [docker/DEPLOYMENT.md](./docker/DEPLOYMENT.md)
- **Script**: [docker/deploy.sh](./docker/deploy.sh)
- **Files**: [docker/Dockerfile](./docker/Dockerfile), [docker/docker-compose.yml](./docker/docker-compose.yml)
- **Memory**: ~400-500 MB
- **Best for**: Larger VMs or multi-service applications

## Quick Start

1. Choose your deployment method (`uv/` or `docker/`)
2. Follow the corresponding guide
3. Use the deployment script for updates

## Directory Structure

```
deployment/
├── README.md           # This file
├── uv/                 # uv-based deployment
│   ├── DEPLOYMENT-UV.md
│   └── deploy-uv.sh
└── docker/             # Docker-based deployment
    ├── DEPLOYMENT.md
    ├── Dockerfile
    ├── docker-compose.yml
    └── deploy.sh
```

