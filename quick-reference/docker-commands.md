# Docker Commands Quick Reference

## Container Management

### Basic Container Operations
```bash
# Run container
docker run [OPTIONS] IMAGE [COMMAND]

# Run container in background
docker run -d IMAGE

# Run container interactively
docker run -it IMAGE

# Run container with name
docker run --name CONTAINER_NAME IMAGE

# Run container with port mapping
docker run -p HOST_PORT:CONTAINER_PORT IMAGE

# Run container with volume mount
docker run -v HOST_PATH:CONTAINER_PATH IMAGE

# Run container with environment variables
docker run -e KEY=VALUE IMAGE
```

### Container Lifecycle
```bash
# Start container
docker start CONTAINER_NAME

# Stop container
docker stop CONTAINER_NAME

# Restart container
docker restart CONTAINER_NAME

# Pause container
docker pause CONTAINER_NAME

# Unpause container
docker unpause CONTAINER_NAME

# Kill container
docker kill CONTAINER_NAME

# Remove container
docker rm CONTAINER_NAME

# Remove running container (force)
docker rm -f CONTAINER_NAME
```

### Container Information
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Show container logs
docker logs CONTAINER_NAME

# Follow container logs
docker logs -f CONTAINER_NAME

# Show container stats
docker stats CONTAINER_NAME

# Inspect container
docker inspect CONTAINER_NAME

# Execute command in container
docker exec CONTAINER_NAME COMMAND

# Execute interactive shell
docker exec -it CONTAINER_NAME /bin/bash
```

## Image Management

### Image Operations
```bash
# List images
docker images

# Pull image
docker pull IMAGE_NAME

# Push image
docker push IMAGE_NAME

# Build image
docker build -t IMAGE_NAME .

# Build image from specific Dockerfile
docker build -f Dockerfile.prod -t IMAGE_NAME .

# Remove image
docker rmi IMAGE_NAME

# Remove unused images
docker image prune

# Remove all images
docker rmi $(docker images -q)
```

### Image Information
```bash
# Show image history
docker history IMAGE_NAME

# Inspect image
docker inspect IMAGE_NAME

# Show image layers
docker image inspect IMAGE_NAME

# Tag image
docker tag SOURCE_IMAGE TARGET_IMAGE
```

## Volume Management

### Volume Operations
```bash
# List volumes
docker volume ls

# Create volume
docker volume create VOLUME_NAME

# Inspect volume
docker volume inspect VOLUME_NAME

# Remove volume
docker volume rm VOLUME_NAME

# Remove unused volumes
docker volume prune

# Remove all volumes
docker volume rm $(docker volume ls -q)
```

### Volume Usage
```bash
# Mount named volume
docker run -v VOLUME_NAME:CONTAINER_PATH IMAGE

# Mount bind volume
docker run -v HOST_PATH:CONTAINER_PATH IMAGE

# Mount read-only volume
docker run -v HOST_PATH:CONTAINER_PATH:ro IMAGE

# Use tmpfs mount
docker run --tmpfs CONTAINER_PATH IMAGE
```

## Network Management

### Network Operations
```bash
# List networks
docker network ls

# Create network
docker network create NETWORK_NAME

# Create network with subnet
docker network create --subnet=172.20.0.0/16 NETWORK_NAME

# Inspect network
docker network inspect NETWORK_NAME

# Remove network
docker network rm NETWORK_NAME

# Remove unused networks
docker network prune

# Remove all networks
docker network rm $(docker network ls -q)
```

### Network Usage
```bash
# Connect container to network
docker network connect NETWORK_NAME CONTAINER_NAME

# Disconnect container from network
docker network disconnect NETWORK_NAME CONTAINER_NAME

# Run container on specific network
docker run --network NETWORK_NAME IMAGE

# Run container with host networking
docker run --network host IMAGE

# Run container with no networking
docker run --network none IMAGE
```

## Docker Compose

### Basic Operations
```bash
# Start services
docker-compose up

# Start services in background
docker-compose up -d

# Start specific service
docker-compose up SERVICE_NAME

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Build services
docker-compose build

# Build specific service
docker-compose build SERVICE_NAME

# Scale service
docker-compose up --scale SERVICE_NAME=NUM
```

### Service Management
```bash
# Start services
docker-compose start

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Show service logs
docker-compose logs

# Follow service logs
docker-compose logs -f

# Execute command in service
docker-compose exec SERVICE_NAME COMMAND

# Show service status
docker-compose ps
```

## System Management

### System Information
```bash
# Show Docker version
docker version

# Show Docker info
docker info

# Show system usage
docker system df

# Show system events
docker events

# Show system events for specific container
docker events --filter container=CONTAINER_NAME
```

### System Cleanup
```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove all unused resources
docker system prune

# Remove all unused resources including images
docker system prune -a
```

## Security Commands

### Security Operations
```bash
# Run container as non-root user
docker run --user 1000:1000 IMAGE

# Run container with read-only filesystem
docker run --read-only IMAGE

# Drop all capabilities
docker run --cap-drop ALL IMAGE

# Add specific capability
docker run --cap-add NET_BIND_SERVICE IMAGE

# Use security profile
docker run --security-opt seccomp=profile.json IMAGE

# Use AppArmor profile
docker run --security-opt apparmor=docker-default IMAGE
```

### Resource Limits
```bash
# Set memory limit
docker run --memory=512m IMAGE

# Set CPU limit
docker run --cpus=1.0 IMAGE

# Set both memory and CPU limits
docker run --memory=512m --cpus=1.0 IMAGE

# Set I/O limits
docker run --device-read-bps /dev/sda:1mb IMAGE

# Set process limit
docker run --pids-limit=100 IMAGE
```

## Registry Commands

### Registry Operations
```bash
# Login to registry
docker login

# Login to specific registry
docker login REGISTRY_URL

# Logout from registry
docker logout

# Search images
docker search IMAGE_NAME

# Show registry info
docker info | grep -i registry
```

## Troubleshooting Commands

### Debugging
```bash
# Show container processes
docker exec CONTAINER_NAME ps aux

# Show container network info
docker exec CONTAINER_NAME ip addr

# Show container routing table
docker exec CONTAINER_NAME ip route

# Test network connectivity
docker exec CONTAINER_NAME ping -c 3 8.8.8.8

# Test DNS resolution
docker exec CONTAINER_NAME nslookup google.com

# Show container environment
docker exec CONTAINER_NAME env

# Show container filesystem
docker exec CONTAINER_NAME df -h
```

### Health Checks
```bash
# Check container health
docker inspect CONTAINER_NAME | grep -A 10 "Health"

# Show container health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Test health check manually
docker exec CONTAINER_NAME curl -f http://localhost/health
```

## Useful Aliases

### Common Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias drm='docker rm'
alias drmi='docker rmi'
alias dstop='docker stop'
alias dstart='docker start'
alias drestart='docker restart'
alias dlogs='docker logs'
alias dexec='docker exec -it'
alias dcompose='docker-compose'
alias dcu='docker-compose up'
alias dcd='docker-compose down'
alias dcb='docker-compose build'
alias dcl='docker-compose logs'
alias dce='docker-compose exec'
```

## Environment Variables

### Common Environment Variables
```bash
# Docker daemon configuration
DOCKER_HOST=tcp://localhost:2376
DOCKER_TLS_VERIFY=1
DOCKER_CERT_PATH=/path/to/certs

# Docker Compose
COMPOSE_PROJECT_NAME=myproject
COMPOSE_FILE=docker-compose.yml:docker-compose.override.yml

# Registry
DOCKER_REGISTRY=registry.example.com
DOCKER_USERNAME=username
DOCKER_PASSWORD=password
```
