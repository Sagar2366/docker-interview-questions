# Docker Interview Questions - Complete Guide

[![GitHub stars](https://img.shields.io/github/stars/Sagar2366/docker-interview-questions.svg)](https://github.com/Sagar2366/docker-interview-questions/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Sagar2366/docker-interview-questions.svg)](https://github.com/Sagar2366/docker-interview-questions/network)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive collection of **90+ Docker interview questions** with detailed answers, practical examples, and diagrams for DevOps and Site Reliability Engineering roles.

## Table of Contents

- [Basic Concepts (10 Questions)](#basic-concepts)
- [Docker Architecture (10 Questions)](#docker-architecture)
- [Docker Networking (10 Questions)](#docker-networking)
- [Docker Security (10 Questions)](#docker-security)
- [Docker Compose (10 Questions)](#docker-compose)
- [Dockerfile Best Practices (10 Questions)](#dockerfile-best-practices)
- [Latest Features (10 Questions)](#latest-features)
- [Advanced Topics (10 Questions)](#advanced-topics)
- [Practical Scenarios (10 Questions)](#practical-scenarios)

---

# Basic Concepts

## 1. What is Docker and how does it differ from virtual machines?

### Answer:
Docker is a containerization platform that packages applications and their dependencies into lightweight, portable containers. Unlike virtual machines, Docker containers share the host OS kernel.

### Key Differences:

| Aspect | Docker Containers | Virtual Machines |
|--------|------------------|------------------|
| **Resource Usage** | Lightweight, minimal overhead | Heavy, full OS overhead |
| **Startup Time** | Seconds | Minutes |
| **Isolation** | Process-level | Hardware-level |
| **Portability** | High | Medium |
| **Density** | High (100s per host) | Low (10s per host) |

### Architecture Comparison:
```
Docker Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Host Operating System                    │
├─────────────────────────────────────────────────────────────┤
│                     Docker Engine                          │
├─────────────────────────────────────────────────────────────┤
│  Container 1  │  Container 2  │  Container 3  │  Container 4 │
│  App A        │  App B        │  App C        │  App D       │
│  Libraries    │  Libraries    │  Libraries    │  Libraries   │
└─────────────────────────────────────────────────────────────┘

VM Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Host Operating System                    │
├─────────────────────────────────────────────────────────────┤
│                      Hypervisor                            │
├─────────────────────────────────────────────────────────────┤
│    VM 1       │    VM 2       │    VM 3       │    VM 4     │
│  Guest OS     │  Guest OS     │  Guest OS     │  Guest OS   │
│  App A        │  App B        │  App C        │  App D       │
│  Libraries    │  Libraries    │  Libraries    │  Libraries   │
└─────────────────────────────────────────────────────────────┘
```

### When to Use Each:
- **Docker**: Microservices, CI/CD, development environments
- **VMs**: Legacy applications, different OS requirements, strong isolation needs

## 2. Explain the Docker architecture and its main components.

### Answer:
Docker uses a client-server architecture with several key components working together.

### Docker Architecture Components:
```
┌─────────────────┐     REST API     ┌─────────────────────────────────────┐
│  Docker Client  │◄────────────────►│         Docker Daemon              │
│                 │                  │         (dockerd)                   │
│ • docker build  │                  │                                     │
│ • docker run    │                  │ ┌─────────────────────────────────┐ │
│ • docker pull   │                  │ │        API Server              │ │
│ • docker push   │                  │ │  • REST API endpoints          │ │
└─────────────────┘                  │ │  • Authentication              │ │
                                     │ └─────────────────────────────────┘ │
┌─────────────────┐                  │                                     │
│ Docker Registry │                  │ ┌─────────────────────────────────┐ │
│                 │                  │ │     Object Management           │ │
│ • Docker Hub    │                  │ │  • Images                      │ │
│ • Private Reg   │                  │ │  • Containers                  │ │
│ • ECR/GCR/ACR   │                  │ │  • Networks                    │ │
└─────────────────┘                  │ │  • Volumes                     │ │
                                     │ └─────────────────────────────────┘ │
                                     │                                     │
                                     │ ┌─────────────────────────────────┐ │
                                     │ │      Runtime Interface          │ │
                                     │ │        containerd               │ │
                                     │ └─────────────┬───────────────────┘ │
                                     └───────────────┼─────────────────────┘
                                                     │
                                     ┌───────────────┼─────────────────────┐
                                     │               ▼                     │
                                     │  ┌─────────────────┐                │
                                     │  │      runc       │                │
                                     │  └─────────┬───────┘                │
                                     │            ▼                        │
                                     │  ┌─────────────────┐                │
                                     │  │   Container     │                │
                                     │  │   Process       │                │
                                     │  └─────────────────┘                │
                                     └─────────────────────────────────────┘
```

### Main Components:

#### 1. Docker Client
- Command-line interface (CLI)
- Communicates with Docker daemon via REST API
- Can connect to remote daemons

#### 2. Docker Daemon (dockerd)
- Background service managing Docker objects
- Handles API requests
- Manages images, containers, networks, volumes

#### 3. Docker Images
- Read-only templates for creating containers
- Built from Dockerfile instructions
- Stored in layers for efficiency

#### 4. Docker Containers
- Running instances of Docker images
- Isolated processes with their own filesystem
- Can be started, stopped, moved, deleted

#### 5. Docker Registry
- Stores and distributes Docker images
- Docker Hub is the default public registry
- Private registries for enterprise use

### Basic Commands:
```bash
# Build image from Dockerfile
docker build -t myapp:latest .

# Run container from image
docker run -d -p 8080:80 myapp:latest

# List running containers
docker ps

# Pull image from registry
docker pull nginx:alpine

# Push image to registry
docker push myregistry.com/myapp:latest
```

## 3. What is a Docker image and how is it different from a container?

### Answer:
A Docker image is a read-only template used to create containers, while a container is a running instance of an image.

### Image vs Container:

| Aspect | Docker Image | Docker Container |
|--------|--------------|------------------|
| **State** | Static, immutable | Dynamic, mutable |
| **Purpose** | Template/Blueprint | Running application |
| **Layers** | Read-only layers | Read-only + writable layer |
| **Storage** | Stored on disk | Running in memory |
| **Lifecycle** | Built once, used many times | Created, started, stopped, deleted |

### Visual Representation:
```
Docker Image (Template):
┌─────────────────────────────────────────────────────────────┐
│                    Docker Image                            │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: CMD ["nginx", "-g", "daemon off;"]              │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: COPY index.html /usr/share/nginx/html/          │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: RUN apt-get install -y nginx                    │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: FROM ubuntu:20.04                               │
└─────────────────────────────────────────────────────────────┘

Docker Container (Running Instance):
┌─────────────────────────────────────────────────────────────┐
│                 Docker Container                           │
├─────────────────────────────────────────────────────────────┤
│  Writable Layer: Container changes, logs, temp files      │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: CMD ["nginx", "-g", "daemon off;"] (Read-only)  │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: COPY index.html /usr/share/nginx/html/ (R/O)    │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: RUN apt-get install -y nginx (Read-only)        │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: FROM ubuntu:20.04 (Read-only)                   │
└─────────────────────────────────────────────────────────────┘
```

### Key Concepts:

#### Docker Images:
- **Immutable**: Cannot be changed once built
- **Layered**: Built in layers for efficiency
- **Shareable**: Can be shared via registries
- **Versioned**: Tagged with versions (e.g., nginx:1.21, nginx:latest)

#### Docker Containers:
- **Mutable**: Can be modified during runtime
- **Isolated**: Run in separate namespaces
- **Ephemeral**: Can be easily created and destroyed
- **Stateful**: Can maintain state during execution

### Practical Examples:

#### Working with Images:
```bash
# List images
docker images

# Build image from Dockerfile
docker build -t myapp:v1.0 .

# Pull image from registry
docker pull nginx:alpine

# Remove image
docker rmi nginx:alpine

# Inspect image details
docker inspect nginx:alpine
```

#### Working with Containers:
```bash
# Create and run container
docker run -d --name webserver nginx:alpine

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop webserver

# Start stopped container
docker start webserver

# Remove container
docker rm webserver

# Execute command in running container
docker exec -it webserver /bin/sh
```

### Image Creation Process:
```dockerfile
# Dockerfile example
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

```bash
# Build process creates layers
docker build -t mynode-app .

# Each instruction creates a new layer:
# Layer 1: FROM node:16-alpine
# Layer 2: WORKDIR /app
# Layer 3: COPY package*.json ./
# Layer 4: RUN npm install
# Layer 5: COPY . .
# Layer 6: EXPOSE 3000
# Layer 7: CMD ["npm", "start"]
```

### Container Lifecycle:
```bash
# Create container (doesn't start it)
docker create --name mycontainer nginx:alpine

# Start created container
docker start mycontainer

# Run container (create + start)
docker run -d --name webserver nginx:alpine

# Pause container
docker pause webserver

# Unpause container
docker unpause webserver

# Stop container gracefully
docker stop webserver

# Kill container forcefully
docker kill webserver

# Remove container
docker rm webserver
```

## 4. Explain the difference between CMD and ENTRYPOINT in Dockerfile.

### Answer:
Both CMD and ENTRYPOINT define what command runs when a container starts, but they behave differently when additional arguments are provided.

### Key Differences:

| Aspect | CMD | ENTRYPOINT |
|--------|-----|------------|
| **Override** | Completely replaced by docker run args | Args appended to ENTRYPOINT |
| **Purpose** | Default command or arguments | Fixed command that always runs |
| **Flexibility** | High - can be completely changed | Low - command is fixed |
| **Use Case** | Default behavior that can be overridden | Core application that always runs |

### Behavior Comparison:

#### CMD Examples:
```dockerfile
# Shell form (not recommended)
CMD echo "Hello World"

# Exec form (recommended)
CMD ["echo", "Hello World"]

# With parameters
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# Using CMD
docker build -t cmd-demo .
docker run cmd-demo                    # Output: Hello World
docker run cmd-demo echo "Goodbye"     # Output: Goodbye (CMD overridden)
```

#### ENTRYPOINT Examples:
```dockerfile
# Fixed command
ENTRYPOINT ["echo", "Hello"]

# Application entrypoint
ENTRYPOINT ["python", "app.py"]

# Script entrypoint
ENTRYPOINT ["./entrypoint.sh"]
```

```bash
# Using ENTRYPOINT
docker build -t entry-demo .
docker run entry-demo                  # Output: Hello
docker run entry-demo World            # Output: Hello World (args appended)
```

### Combined Usage (Best Practice):
```dockerfile
# ENTRYPOINT defines the executable
ENTRYPOINT ["python", "app.py"]

# CMD provides default arguments
CMD ["--port", "8080", "--env", "production"]
```

```bash
# Combined behavior
docker run myapp                       # python app.py --port 8080 --env production
docker run myapp --port 3000           # python app.py --port 3000 (CMD overridden)
```

### Real-World Examples:

#### Web Server (CMD):
```dockerfile
FROM nginx:alpine
CMD ["nginx", "-g", "daemon off;"]
# Allows: docker run nginx-image nginx-debug
```

#### Database (ENTRYPOINT + CMD):
```dockerfile
FROM postgres:13
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]
# Always runs entrypoint script, but can change database command
```

#### CLI Tool (ENTRYPOINT):
```dockerfile
FROM alpine
COPY mytool /usr/local/bin/
ENTRYPOINT ["mytool"]
# Always runs mytool, arguments passed to it
```

### Shell vs Exec Form:
```dockerfile
# Shell form - runs in shell (/bin/sh -c)
CMD echo $HOME                         # Variable expansion works
ENTRYPOINT echo $HOME

# Exec form - direct execution (recommended)
CMD ["echo", "$HOME"]                  # No variable expansion
ENTRYPOINT ["echo", "$HOME"]

# Exec form with variable expansion
CMD ["/bin/sh", "-c", "echo $HOME"]    # Explicit shell
```

### Best Practices:
1. **Use ENTRYPOINT** for fixed executable
2. **Use CMD** for default arguments
3. **Prefer exec form** over shell form
4. **Combine both** for flexibility
5. **Use shell form** only when you need shell features

## 5. Explain Docker layers and how they work.

### Answer:
Docker images are built using a layered filesystem. Each instruction in a Dockerfile creates a new read-only layer. When you run a container, Docker adds a writable layer on top.

### Layer Architecture:
```
Container (Read-Write Layer)
┌─────────────────────────────┐ ← Writable layer (changes here)
│     Container Layer         │
├─────────────────────────────┤
│     Layer 4: COPY app.py    │ ← Read-only layers
├─────────────────────────────┤   (shared between containers)
│     Layer 3: RUN install    │
├─────────────────────────────┤
│     Layer 2: RUN update     │
├─────────────────────────────┤
│     Layer 1: FROM ubuntu    │
└─────────────────────────────┘
```

### How Layers Work:

#### 1. Layer Creation:
```dockerfile
FROM ubuntu:20.04          # Layer 1 (base)
RUN apt-get update         # Layer 2 (package index)
RUN apt-get install -y git # Layer 3 (git installation)
WORKDIR /app              # Layer 4 (directory creation)
COPY app.py .             # Layer 5 (file copy)
CMD ["python", "app.py"]  # Layer 6 (metadata only)
```

#### 2. Layer Sharing:
```
Image A                    Image B
┌─────────────────┐       ┌─────────────────┐
│ App A files     │       │ App B files     │
├─────────────────┤       ├─────────────────┤
│ Python install  │       │ Node.js install │
├─────────────────┤       ├─────────────────┤
│                 │       │                 │
│   Shared Base   │◄────► │   Shared Base   │
│  Ubuntu:20.04   │       │  Ubuntu:20.04   │
│                 │       │                 │
└─────────────────┘       └─────────────────┘
```

### Copy-on-Write (CoW) Mechanism:
```
Multiple Containers from Same Image:

Container 1        Container 2        Container 3
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Write Layer │   │ Write Layer │   │ Write Layer │
├─────────────┤   ├─────────────┤   ├─────────────┤
│             │   │             │   │             │
│        Shared Read-Only Layers                  │
│         (Image Layers)                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Layer Caching Benefits:

#### Build Cache Example:
```dockerfile
# First build
FROM node:16-alpine        # ✓ Downloaded
WORKDIR /app              # ✓ Layer created
COPY package*.json ./     # ✓ Layer created
RUN npm install           # ✓ Layer created (slow)
COPY . .                  # ✓ Layer created
RUN npm run build         # ✓ Layer created

# Second build (only code changed)
FROM node:16-alpine        # ✓ Cache hit
WORKDIR /app              # ✓ Cache hit
COPY package*.json ./     # ✓ Cache hit
RUN npm install           # ✓ Cache hit (fast!)
COPY . .                  # ✗ Cache miss (code changed)
RUN npm run build         # ✗ Rebuilt
```

### Practical Commands:

#### View Image Layers:
```bash
# Show image history
docker history nginx:alpine

# Detailed layer information
docker image inspect nginx:alpine

# Show layer sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

#### Analyze Layer Changes:
```bash
# Show changes in container
docker diff container_name

# Export container changes
docker export container_name > container.tar

# Save image layers
docker save nginx:alpine > nginx.tar
```

### Layer Optimization Strategies:

#### 1. Order Instructions by Change Frequency:
```dockerfile
# ✅ Good - stable instructions first
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./      # Changes less frequently
RUN npm install
COPY . .                   # Changes more frequently
RUN npm run build

# ❌ Bad - unstable instructions first
FROM node:16-alpine
COPY . .                   # Changes frequently
RUN npm install            # Cache invalidated often
```

#### 2. Combine Related Commands:
```dockerfile
# ✅ Good - single layer
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ Bad - multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean
```

#### 3. Use Multi-stage Builds:
```dockerfile
# Build stage (large)
FROM node:16 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Production stage (small)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# Only final artifacts, not build dependencies
```

### Layer Limits and Considerations:
- **Maximum layers**: 127 layers per image
- **Layer size**: Each layer adds to total image size
- **Cache invalidation**: Changes invalidate all subsequent layers
- **Security**: Each layer can introduce vulnerabilities

### Troubleshooting Layer Issues:
```bash
# Find large layers
docker history --human --format "table {{.CreatedBy}}\t{{.Size}}" image_name

# Analyze layer content
docker run --rm -it image_name sh
du -sh /*

# Check for cache misses
docker build --no-cache -t image_name .
```
## 6. What are Docker volumes and why are they important?

### Answer:
Docker volumes are the preferred mechanism for persisting data generated and used by Docker containers. They solve the problem of data loss when containers are removed.

### Why Volumes are Important:
- **Data Persistence**: Data survives container lifecycle
- **Performance**: Better I/O than container filesystem
- **Sharing**: Multiple containers can share data
- **Backup**: Easy to backup and restore
- **Portability**: Independent of host filesystem

### Volume Types:

#### 1. Named Volumes (Recommended)
```bash
# Create named volume
docker volume create mydata

# Use named volume
docker run -v mydata:/app/data nginx

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata
```

#### 2. Anonymous Volumes
```bash
# Create anonymous volume
docker run -v /app/data nginx

# Docker creates random name
docker volume ls
```

#### 3. Bind Mounts
```bash
# Mount host directory
docker run -v /host/path:/container/path nginx

# Mount current directory
docker run -v $(pwd):/app nginx
```

#### 4. tmpfs Mounts (Memory)
```bash
# Mount in memory
docker run --tmpfs /app/temp nginx

# With options
docker run --tmpfs /app/temp:noexec,nosuid,size=100m nginx
```

### Volume Management:
```bash
# Create volume with driver options
docker volume create --driver local --opt type=nfs --opt device=:/path myvolume

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune

# Backup volume
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu tar xzf /backup/backup.tar.gz -C /
```

## 7. How do you build a Docker image from a Dockerfile?

### Answer:
Docker images are built from Dockerfiles using the `docker build` command. The build process creates layers for each instruction.

### Basic Dockerfile:
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Build Commands:
```bash
# Basic build
docker build -t myapp .

# Build with tag and version
docker build -t myapp:v1.0 .

# Build from specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t myapp .

# Build without cache
docker build --no-cache -t myapp .
```

### Build Context:
```bash
# Build from URL
docker build https://github.com/user/repo.git

# Build from tarball
docker build - < archive.tar.gz

# Build with specific context
docker build -f /path/to/Dockerfile /path/to/context
```

### Multi-stage Build:
```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
CMD ["npm", "start"]
```

## 8. What is Docker Compose and when would you use it?

### Answer:
Docker Compose is a tool for defining and running multi-container Docker applications using YAML configuration files.

### When to Use Docker Compose:
- **Multi-container applications**
- **Development environments**
- **Local testing**
- **Service orchestration**
- **Simplified deployment**

### Basic docker-compose.yml:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - api
      - db

  api:
    build: ./api
    environment:
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Compose Commands:
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Scale services
docker-compose up --scale web=3

# Build services
docker-compose build
```

## 9. Explain Docker networking basics.

### Answer:
Docker provides several networking options to enable communication between containers and external networks.

### Network Types:

#### 1. Bridge (Default)
```bash
# Default bridge network
docker run -d nginx

# Custom bridge network
docker network create mynetwork
docker run -d --network mynetwork nginx
```

#### 2. Host
```bash
# Use host network
docker run -d --network host nginx
```

#### 3. None
```bash
# No network access
docker run -d --network none nginx
```

### Network Commands:
```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Create network
docker network create --driver bridge mynetwork

# Connect container to network
docker network connect mynetwork container_name

# Disconnect container
docker network disconnect mynetwork container_name
```

### Port Publishing:
```bash
# Publish port
docker run -p 8080:80 nginx

# Publish all exposed ports
docker run -P nginx

# Publish to specific interface
docker run -p 127.0.0.1:8080:80 nginx
```

## 10. How do you troubleshoot Docker containers?

### Answer:
Docker provides various tools and techniques for troubleshooting container issues.

### Common Troubleshooting Steps:

#### 1. Check Container Status
```bash
# List all containers
docker ps -a

# Check container logs
docker logs container_name

# Follow logs in real-time
docker logs -f container_name

# Check last 100 lines
docker logs --tail 100 container_name
```

#### 2. Inspect Container
```bash
# Detailed container information
docker inspect container_name

# Check container processes
docker exec container_name ps aux

# Check resource usage
docker stats container_name
```

#### 3. Access Container
```bash
# Execute interactive shell
docker exec -it container_name /bin/bash

# Execute specific command
docker exec container_name ls -la /app

# Run debugging container
docker run --rm -it --pid container:target_container alpine
```

#### 4. Network Troubleshooting
```bash
# Check network configuration
docker network inspect bridge

# Test connectivity
docker exec container_name ping google.com

# Check port bindings
docker port container_name
```

#### 5. Storage Issues
```bash
# Check disk usage
docker system df

# Check container changes
docker diff container_name

# Clean up unused resources
docker system prune
```

### Common Issues and Solutions:

#### Container Won't Start:
```bash
# Check exit code
docker ps -a

# View detailed logs
docker logs container_name

# Run with different entrypoint
docker run --entrypoint /bin/bash image_name
```

#### Performance Issues:
```bash
# Monitor resources
docker stats

# Check container limits
docker inspect container_name | grep -i memory

# Analyze processes
docker exec container_name top
```

#### Network Issues:
```bash
# Check DNS resolution
docker exec container_name nslookup google.com

# Test port connectivity
docker exec container_name telnet hostname port

# Check routing
docker exec container_name ip route
```

---
# Docker Architecture

## 1. Explain Docker's client-server architecture in detail.

### Answer:
Docker uses a client-server architecture that separates the user interface from the container management engine, enabling flexible deployment and remote management.

### Architecture Components:

#### 1. Docker Client (`docker` CLI)
- **Purpose**: User interface to Docker ecosystem
- **Communication**: REST API over Unix socket or TCP
- **Features**: Command-line interface, remote daemon connection, plugin system support

```bash
# Client configuration examples
docker version                    # Shows client and server versions
docker context ls                 # List available contexts
docker context use remote-host    # Switch to remote Docker host
docker -H tcp://remote:2376 ps    # Connect to remote daemon
```

#### 2. Docker Daemon (`dockerd`)
- **Purpose**: Core Docker service and API server
- **Responsibilities**: API request handling, image management, container lifecycle, network management

```bash
# Daemon management
sudo systemctl status docker      # Check daemon status
sudo systemctl start docker       # Start daemon
journalctl -u docker.service -f   # Follow daemon logs
```

#### 3. containerd
- **Purpose**: High-level container runtime
- **Functions**: Container lifecycle management, image management, runtime abstraction

#### 4. runc
- **Purpose**: Low-level OCI runtime
- **Functions**: Container creation and execution, namespace and cgroup management

### Communication Flow:
```
User Command → Docker Client → Docker Daemon → containerd → runc → Linux Kernel
```

## 2. What is containerd and how does it relate to Docker?

### Answer:
containerd is a high-level container runtime that serves as the core container runtime for Docker. It was extracted from Docker to create a more modular container ecosystem.

### containerd Features:

#### 1. Container Lifecycle Management
```bash
# Direct containerd usage (ctr command)
ctr images pull docker.io/library/nginx:latest
ctr containers create docker.io/library/nginx:latest nginx-container
ctr tasks start nginx-container
ctr tasks list
```

#### 2. Image Management
```bash
# Image operations with containerd
ctr images list
ctr images pull docker.io/library/alpine:latest
ctr images remove docker.io/library/alpine:latest
```

### Benefits of containerd:
- **Modularity**: Can be used without Docker daemon
- **Kubernetes Integration**: Direct CRI support
- **Performance**: Optimized for container operations
- **Industry Standard**: CNCF graduated project

## 3. Explain the role of runc in Docker's architecture.

### Answer:
runc is the low-level container runtime that actually creates and runs containers. It interfaces directly with the Linux kernel to set up the container environment.

### runc Responsibilities:

#### 1. OCI Runtime Implementation
```bash
# OCI bundle structure
/path/to/bundle/
├── config.json          # Container configuration
└── rootfs/              # Container root filesystem
```

#### 2. Namespace Management
- **PID Namespace**: Process isolation
- **Network Namespace**: Network isolation
- **Mount Namespace**: Filesystem isolation
- **IPC Namespace**: Inter-process communication isolation
- **UTS Namespace**: Hostname isolation
- **User Namespace**: User ID isolation

#### 3. cgroups Resource Management
```bash
# cgroups hierarchy
/sys/fs/cgroup/
├── cpu/docker/container_id/
├── memory/docker/container_id/
└── blkio/docker/container_id/
```

### runc Operations:
```bash
# Container lifecycle
runc create container_id --bundle /path/to/bundle
runc start container_id
runc state container_id
runc kill container_id SIGTERM
runc delete container_id
```

## 4. What are Docker namespaces and how do they provide isolation?

### Answer:
Docker uses Linux namespaces to provide process isolation. Each namespace type isolates a specific aspect of the system.

### Namespace Types:

#### 1. PID Namespace
- **Purpose**: Isolates process IDs
- **Benefit**: Containers have their own process tree

#### 2. Network Namespace
- **Purpose**: Isolates network interfaces
- **Benefit**: Containers have separate network stacks

#### 3. Mount Namespace
- **Purpose**: Isolates filesystem mounts
- **Benefit**: Containers have separate filesystem views

#### 4. IPC Namespace
- **Purpose**: Isolates inter-process communication
- **Benefit**: Containers cannot interfere with each other's IPC

#### 5. UTS Namespace
- **Purpose**: Isolates hostname and domain name
- **Benefit**: Containers can have different hostnames

#### 6. User Namespace
- **Purpose**: Isolates user and group IDs
- **Benefit**: Root in container is not root on host

### Example:
```bash
# View namespaces of a container
docker exec container_name ls -la /proc/self/ns/

# Create container with specific namespace
docker run --pid=host nginx  # Uses host PID namespace
```

## 5. How does Docker use cgroups for resource management?

### Answer:
cgroups (control groups) limit and monitor resource usage of containers, providing resource isolation and management.

### Resource Types:

#### 1. CPU Management
```bash
# Limit CPU usage
docker run --cpus="1.5" nginx
docker run --cpu-shares=512 nginx
```

#### 2. Memory Management
```bash
# Limit memory
docker run --memory="512m" nginx
docker run --memory="1g" --memory-swap="2g" nginx
```

#### 3. I/O Management
```bash
# Limit I/O
docker run --device-read-bps /dev/sda:1mb nginx
docker run --device-write-bps /dev/sda:1mb nginx
```

### cgroup Hierarchy:
```
/sys/fs/cgroup/
├── cpu/docker/container_id/
│   ├── cpu.cfs_quota_us
│   └── cpu.shares
├── memory/docker/container_id/
│   ├── memory.limit_in_bytes
│   └── memory.usage_in_bytes
└── blkio/docker/container_id/
    └── blkio.throttle.read_bps_device
```

## 6. Explain Docker's storage driver architecture.

### Answer:
Docker uses storage drivers to manage how images and containers are stored on the host filesystem.

### Common Storage Drivers:

#### 1. overlay2 (Recommended)
- **Features**: Uses overlay filesystem, good performance, efficient storage
- **Use Case**: Most production environments

#### 2. aufs
- **Features**: Union filesystem, good compatibility
- **Use Case**: Older systems, development

#### 3. devicemapper
- **Features**: Block-level storage, production-ready
- **Use Case**: Enterprise environments

#### 4. btrfs
- **Features**: Copy-on-write filesystem
- **Use Case**: Systems with btrfs filesystem

### Storage Driver Selection:
```bash
# Check current storage driver
docker info | grep "Storage Driver"

# Configure storage driver in daemon.json
{
  "storage-driver": "overlay2"
}
```

## 7. What is the Docker daemon and how do you configure it?

### Answer:
The Docker daemon (`dockerd`) is the background service that manages Docker objects and handles container operations.

### Daemon Configuration:
```json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "registry-mirrors": ["https://mirror.example.com"],
  "insecure-registries": ["registry.example.com:5000"]
}
```

### Daemon Management:
```bash
# Start daemon
sudo systemctl start docker

# Stop daemon
sudo systemctl stop docker

# Restart daemon
sudo systemctl restart docker

# View daemon logs
journalctl -u docker.service
```

## 8. How does Docker handle image layers and the copy-on-write mechanism?

### Answer:
Docker uses a copy-on-write (CoW) mechanism for efficient storage and fast container creation.

### Layer Structure:
```
Container Layer (Read-Write)
├── Image Layer 3 (Read-Only)
├── Image Layer 2 (Read-Only)
└── Image Layer 1 (Read-Only)
```

### Copy-on-Write Process:
1. **Read Operations**: Read from existing layers
2. **Write Operations**: Copy to container layer
3. **Delete Operations**: Mark as deleted in container layer

### Benefits:
- **Efficiency**: Shared layers between containers
- **Speed**: Fast container creation
- **Storage**: Minimal disk usage
- **Caching**: Reuse unchanged layers

### Example:
```bash
# View image layers
docker history nginx

# View container layer changes
docker diff container_name
```

## 9. Explain Docker's networking architecture and bridge networks.

### Answer:
Docker creates a default bridge network (`docker0`) and allows custom networks for container communication.

### Default Bridge Network:
- **Subnet**: Usually 172.17.0.0/16
- **Gateway**: 172.17.0.1
- **DNS**: Container name resolution
- **Isolation**: Containers can communicate

### Network Management:
```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Create custom network
docker network create --driver bridge mynetwork

# Connect container to network
docker network connect mynetwork container_name
```

## 10. What is the Docker API and how do you interact with it?

### Answer:
Docker provides a REST API for programmatic access to Docker functionality.

### API Endpoints:
- **Containers**: `/containers/`
- **Images**: `/images/`
- **Networks**: `/networks/`
- **Volumes**: `/volumes/`
- **System**: `/info`, `/version`

### API Usage:
```bash
# Enable API access
dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2376

# List containers via API
curl -X GET http://localhost:2376/containers/json

# Create container via API
curl -X POST http://localhost:2376/containers/create \
  -H "Content-Type: application/json" \
  -d '{"Image": "nginx"}'
```

### Security Considerations:
- **TLS**: Use HTTPS in production
- **Authentication**: Implement proper auth
- **Authorization**: Control access levels
- **Network**: Restrict API access

---
# Docker Networking

## 1. Explain Docker's default networking model and bridge networks.

### Answer:
Docker creates a default bridge network (`docker0`) that provides network isolation and connectivity for containers.

### Default Bridge Network:
- **Subnet**: 172.17.0.0/16 (configurable)
- **Gateway**: 172.17.0.1
- **DNS**: Automatic container name resolution
- **Isolation**: Containers can communicate with each other

### Network Flow:
```
Internet → Host Network → docker0 Bridge → Container Network
```

### Example:
```bash
# View default bridge network
docker network inspect bridge

# Run containers on default bridge
docker run -d --name web1 nginx
docker run -d --name web2 nginx

# Containers can communicate by IP
docker exec web1 ping 172.17.0.3
```

## 2. What are the different Docker networking modes and when to use each?

### Answer:

### 1. Bridge Mode (Default)
- **Use Case**: Single host, isolated containers
- **Isolation**: Containers isolated from host
- **Communication**: Containers can communicate via IP/name

```bash
docker run -d nginx  # Uses bridge mode
```

### 2. Host Mode
- **Use Case**: Maximum performance, single container per port
- **Isolation**: No network isolation
- **Communication**: Direct host network access

```bash
docker run -d --network host nginx
```

### 3. None Mode
- **Use Case**: Maximum isolation, custom networking
- **Isolation**: No network access
- **Communication**: Manual network setup required

```bash
docker run -d --network none nginx
```

### 4. Overlay Mode
- **Use Case**: Multi-host networking (Docker Swarm)
- **Isolation**: Cross-host container communication
- **Communication**: Encrypted overlay network

```bash
docker network create --driver overlay myoverlay
```

### 5. Macvlan Mode
- **Use Case**: Legacy applications, direct network access
- **Isolation**: Each container gets MAC address
- **Communication**: Direct network interface access

```bash
docker network create --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 mymacvlan
```

## 3. How do you create and manage custom Docker networks?

### Answer:

### Create Custom Networks:
```bash
# Create bridge network
docker network create mynetwork

# Create network with custom subnet
docker network create --subnet=172.20.0.0/16 mynetwork

# Create network with custom gateway
docker network create --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 mynetwork

# Create network with custom driver
docker network create --driver bridge mynetwork
```

### Network Management:
```bash
# List networks
docker network ls

# Inspect network
docker network inspect mynetwork

# Remove network
docker network rm mynetwork

# Remove unused networks
docker network prune
```

### Connect Containers:
```bash
# Connect container to network
docker network connect mynetwork container_name

# Disconnect container from network
docker network disconnect mynetwork container_name

# Run container on specific network
docker run -d --network mynetwork nginx
```

## 4. Explain Docker's service discovery and DNS resolution.

### Answer:
Docker provides built-in DNS resolution for container-to-container communication.

### DNS Resolution:
- **Container Names**: Resolve to container IP
- **Network Aliases**: Custom names for containers
- **Service Names**: In Docker Compose/Swarm

### Examples:
```bash
# Create network
docker network create mynetwork

# Run containers with custom names
docker run -d --name web --network mynetwork nginx
docker run -d --name db --network mynetwork postgres

# Containers can communicate by name
docker exec web ping db
docker exec db ping web
```

### Network Aliases:
```bash
# Create container with alias
docker run -d --name web \
  --network mynetwork \
  --network-alias webserver nginx

# Other containers can reach it via alias
docker exec db ping webserver
```

## 5. How do you expose and publish container ports?

### Answer:

### Port Exposure vs Publishing:

| Concept | Description | Example |
|---------|-------------|---------|
| **EXPOSE** | Documents port (Dockerfile) | `EXPOSE 80` |
| **Publish** | Maps host port to container | `-p 8080:80` |

### Port Publishing Options:
```bash
# Map host port to container port
docker run -p 8080:80 nginx

# Map random host port
docker run -P nginx

# Map specific host IP
docker run -p 127.0.0.1:8080:80 nginx

# Map UDP port
docker run -p 8080:80/udp nginx

# Map multiple ports
docker run -p 8080:80 -p 8443:443 nginx
```

### Port Range:
```bash
# Map port range
docker run -p 8080-8090:80-90 nginx
```

## 6. What is Docker's network security model?

### Answer:

### Network Isolation:
- **Default**: Containers isolated from host
- **Bridge**: Containers can communicate within network
- **Host**: No isolation (security risk)

### Security Best Practices:
```bash
# Use custom networks for isolation
docker network create --internal secure-network

# Limit container communication
docker run --network secure-network nginx

# Use host networking only when necessary
docker run --network host nginx
```

### Firewall Integration:
```bash
# Block external access to bridge network
iptables -A DOCKER-USER -i docker0 -j DROP

# Allow specific container communication
iptables -A DOCKER-USER -s 172.17.0.2 -d 172.17.0.3 -j ACCEPT
```

## 7. How do you troubleshoot Docker networking issues?

### Answer:

### Common Issues and Solutions:

#### 1. Container Cannot Reach Internet
```bash
# Check DNS resolution
docker exec container_name nslookup google.com

# Check routing
docker exec container_name ip route

# Check network configuration
docker network inspect bridge
```

#### 2. Containers Cannot Communicate
```bash
# Check if containers are on same network
docker network inspect network_name

# Test connectivity
docker exec container1 ping container2

# Check firewall rules
iptables -L DOCKER-USER
```

#### 3. Port Not Accessible
```bash
# Check port mapping
docker port container_name

# Check if port is listening
docker exec container_name netstat -tlnp

# Check host firewall
sudo ufw status
```

### Debugging Commands:
```bash
# View container network info
docker inspect container_name | grep -A 20 "NetworkSettings"

# View network details
docker network inspect network_name

# Test network connectivity
docker exec container_name ping -c 3 8.8.8.8
```

## 8. Explain Docker Compose networking.

### Answer:

### Default Compose Network:
- **Name**: `{project_name}_default`
- **Driver**: Bridge
- **Communication**: All services can communicate by name

### Compose Network Configuration:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend
  
  db:
    image: postgres
    networks:
      - backend
      - frontend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### External Networks:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - external-network

networks:
  external-network:
    external: true
```

## 9. How do you implement load balancing with Docker networking?

### Answer:

### Using Docker Compose:
```yaml
version: '3.8'
services:
  nginx:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - web1
      - web2
  
  web1:
    image: nginx
    networks:
      - app-network
  
  web2:
    image: nginx
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Using External Load Balancer:
```bash
# Create network for load balancer
docker network create lb-network

# Run load balancer
docker run -d --name haproxy \
  --network lb-network \
  -p 80:80 \
  -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg \
  haproxy

# Run backend services
docker run -d --name web1 --network lb-network nginx
docker run -d --name web2 --network lb-network nginx
```

## 10. What are Docker's network plugins and how do you use them?

### Answer:

### Network Plugin Types:
1. **Bridge**: Default plugin
2. **Overlay**: Multi-host networking
3. **Macvlan**: Direct network access
4. **Third-party**: Weave, Calico, Flannel

### Using Network Plugins:
```bash
# Install Weave plugin
docker plugin install weaveworks/net-plugin:latest

# Create network with plugin
docker network create --driver weave mynetwork

# Use network
docker run -d --network mynetwork nginx
```

### Plugin Configuration:
```bash
# Configure plugin
docker plugin set weaveworks/net-plugin:latest \
  WEAVE_PASSWORD=secret

# Enable plugin
docker plugin enable weaveworks/net-plugin:latest
```

---
# Docker Security

## 1. What are the main security concerns with Docker containers?

### Answer:
Docker security involves multiple layers of protection, from the container runtime to the host system.

### Primary Security Concerns:

#### 1. Container Escape Vulnerabilities
**Prevention Strategies:**
```bash
# Run as non-root user
docker run --user 1000:1000 nginx

# Drop all capabilities
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx

# Use read-only filesystem
docker run --read-only nginx

# Apply security profiles
docker run --security-opt seccomp=profile.json nginx
```

#### 2. Image Security Vulnerabilities
**Mitigation Strategies:**
```bash
# Use minimal base images
FROM alpine:latest  # Instead of ubuntu:latest

# Scan images for vulnerabilities
docker scan myimage:latest
trivy image myimage:latest

# Use multi-stage builds
FROM node:16 AS builder
# ... build steps
FROM alpine:latest
COPY --from=builder /app/dist /app

# Sign and verify images
docker trust sign myimage:latest
DOCKER_CONTENT_TRUST=1 docker pull myimage:latest
```

#### 3. Runtime Security Threats
**Runtime Security Controls:**
```bash
# Resource limits
docker run --memory=512m --cpus=1.0 --pids-limit=100 nginx

# Network isolation
docker network create --internal secure-net
docker run --network secure-net nginx

# Security profiles
docker run --security-opt apparmor=docker-default nginx
docker run --security-opt seccomp=default nginx

# No new privileges
docker run --security-opt no-new-privileges nginx
```

### Comprehensive Security Best Practices:

#### Defense in Depth Strategy:
```bash
# Multi-layered security approach
docker run -d \
  --name secure-app \
  --user 1000:1000 \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --read-only \
  --tmpfs /tmp \
  --memory=512m \
  --cpus=1.0 \
  --pids-limit=100 \
  --security-opt no-new-privileges \
  --security-opt seccomp=default \
  --security-opt apparmor=docker-default \
  --network custom-network \
  myapp:latest
```

## 2. How do you secure Docker images and what is image scanning?

### Answer:

### Image Security Measures:

#### 1. Use Official Base Images
```dockerfile
# Good: Use official, minimal base images
FROM node:16-alpine

# Bad: Use large, potentially vulnerable images
FROM ubuntu:20.04
```

#### 2. Keep Images Updated
```dockerfile
# Pin specific versions
FROM node:16.14.2-alpine

# Regularly update base images
FROM node:18-alpine
```

#### 3. Minimize Attack Surface
```dockerfile
# Multi-stage builds to reduce final image size
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["npm", "start"]
```

### Image Scanning:
```bash
# Scan image for vulnerabilities
docker scan nginx:latest

# Scan with specific options
docker scan --severity high nginx:latest

# Scan with output format
docker scan --format json nginx:latest
```

### Third-party Scanning Tools:
```bash
# Trivy scanner
trivy image nginx:latest

# Clair scanner
clair-scanner --ip 172.17.0.1 nginx:latest

# Anchore scanner
anchore-cli image add nginx:latest
anchore-cli image vuln nginx:latest all
```

## 3. Explain Docker's security model and isolation mechanisms.

### Answer:

### Docker Security Model:

#### 1. Namespace Isolation
```bash
# View container namespaces
docker exec container_name ls -la /proc/self/ns/

# Run container with specific namespace
docker run --pid=host nginx  # Uses host PID namespace
```

#### 2. cgroups Resource Limits
```bash
# Limit memory usage
docker run --memory=512m nginx

# Limit CPU usage
docker run --cpus=1.0 nginx

# Limit I/O operations
docker run --device-read-bps /dev/sda:1mb nginx
```

#### 3. Capabilities
```bash
# Drop all capabilities
docker run --cap-drop ALL nginx

# Add specific capabilities
docker run --cap-add NET_BIND_SERVICE nginx

# List container capabilities
docker exec container_name capsh --print
```

#### 4. Seccomp Profiles
```bash
# Use custom seccomp profile
docker run --security-opt seccomp=profile.json nginx

# Disable seccomp (not recommended)
docker run --security-opt seccomp=unconfined nginx
```

## 4. How do you manage secrets in Docker containers?

### Answer:

### Docker Secrets (Swarm Mode):
```bash
# Create secret
echo "mysecretpassword" | docker secret create db_password -

# Use secret in service
docker service create \
  --secret db_password \
  --name web \
  nginx
```

### Docker Compose Secrets:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Environment Variables:
```bash
# Pass secret as environment variable
docker run -e DB_PASSWORD=secret nginx

# Use .env file
docker run --env-file .env nginx
```

### Volume Mounts for Secrets:
```bash
# Mount secret file
docker run -v /host/secrets:/app/secrets:ro nginx

# Use tmpfs for sensitive data
docker run --tmpfs /tmp:noexec,nosuid,size=100m nginx
```

### External Secret Management:
```bash
# HashiCorp Vault integration
docker run -e VAULT_ADDR=https://vault.example.com nginx

# AWS Secrets Manager
docker run -e AWS_REGION=us-east-1 nginx
```

## 5. What are Docker's security best practices for production?

### Answer:

### Production Security Checklist:

#### 1. Container Configuration
```bash
# Run as non-root user
docker run --user 1000:1000 nginx

# Use read-only filesystem
docker run --read-only nginx

# Drop unnecessary capabilities
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx

# Limit container resources
docker run --memory=512m --cpus=1.0 nginx
```

#### 2. Network Security
```bash
# Use custom networks
docker network create --internal secure-network

# Limit port exposure
docker run -p 127.0.0.1:8080:80 nginx

# Use TLS for communication
docker run -p 443:443 -v /certs:/certs nginx
```

#### 3. Image Security
```dockerfile
# Use minimal base images
FROM alpine:latest

# Run as non-root user
RUN adduser -D -s /bin/sh appuser
USER appuser

# Remove package manager
RUN apk del apk-tools

# Use multi-stage builds
FROM node:16-alpine AS builder
# ... build steps
FROM alpine:latest
COPY --from=builder /app /app
```

#### 4. Runtime Security
```bash
# Use security profiles
docker run --security-opt seccomp=profile.json nginx

# Enable AppArmor
docker run --security-opt apparmor=docker-default nginx

# Use SELinux
docker run --security-opt label:type:container_t nginx
```

## 6. How do you implement Docker security scanning in CI/CD?

### Answer:

### CI/CD Security Pipeline:

#### 1. Pre-build Scanning
```yaml
# GitHub Actions example
name: Security Scan
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t myapp:latest .
      
      - name: Scan image
        run: docker scan myapp:latest
      
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
```

#### 2. Base Image Scanning
```bash
# Scan base images regularly
docker scan node:16-alpine
docker scan nginx:alpine
docker scan postgres:13-alpine
```

#### 3. Dependency Scanning
```bash
# Scan for vulnerable dependencies
npm audit
pip check
go list -json -m all | nancy sleuth
```

## 7. Explain Docker's security features: AppArmor, SELinux, and seccomp.

### Answer:

#### 1. AppArmor
- **Purpose**: Mandatory Access Control (MAC)
- **Function**: Restricts container capabilities
- **Usage**: Prevents privilege escalation

```bash
# Use AppArmor profile
docker run --security-opt apparmor=docker-default nginx

# Custom AppArmor profile
docker run --security-opt apparmor=my-profile nginx

# Disable AppArmor (not recommended)
docker run --security-opt apparmor=unconfined nginx
```

#### 2. SELinux
- **Purpose**: Mandatory Access Control (MAC)
- **Function**: Labels and enforces access policies
- **Usage**: Prevents unauthorized access

```bash
# Use SELinux labels
docker run --security-opt label:type:container_t nginx

# Custom SELinux context
docker run --security-opt label:user:system_u nginx

# Disable SELinux (not recommended)
docker run --security-opt label:disable nginx
```

#### 3. seccomp
- **Purpose**: System call filtering
- **Function**: Restricts system calls
- **Usage**: Prevents malicious system calls

```bash
# Use seccomp profile
docker run --security-opt seccomp=profile.json nginx

# Default seccomp profile
docker run --security-opt seccomp=default nginx

# Disable seccomp (not recommended)
docker run --security-opt seccomp=unconfined nginx
```

### Custom seccomp Profile:
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["read", "write", "open", "close"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

## 8. How do you secure Docker daemon and API access?

### Answer:

### Daemon Security Configuration:

#### 1. TLS Configuration
```bash
# Generate certificates
openssl genrsa -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem

# Configure daemon with TLS
dockerd \
  --tlsverify \
  --tlscacert=ca.pem \
  --tlscert=server-cert.pem \
  --tlskey=server-key.pem \
  -H=0.0.0.0:2376
```

#### 2. API Access Control
```bash
# Restrict API access
dockerd -H unix:///var/run/docker.sock -H tcp://127.0.0.1:2376

# Use firewall rules
iptables -A INPUT -p tcp --dport 2376 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 2376 -j DROP
```

#### 3. User Authentication
```bash
# Create Docker group
sudo groupadd docker
sudo usermod -aG docker $USER

# Restrict socket permissions
sudo chmod 660 /var/run/docker.sock
sudo chown root:docker /var/run/docker.sock
```

## 9. What are Docker security vulnerabilities and how do you mitigate them?

### Answer:

### Common Vulnerabilities:

#### 1. Container Escape
- **Risk**: Breaking out of container isolation
- **Mitigation**: Use non-privileged containers, security profiles

```bash
# Mitigate container escape
docker run --user 1000:1000 nginx
docker run --security-opt seccomp=profile.json nginx
docker run --read-only nginx
```

#### 2. Privilege Escalation
- **Risk**: Gaining root access
- **Mitigation**: Drop capabilities, use non-root users

```bash
# Prevent privilege escalation
docker run --cap-drop ALL nginx
docker run --user 1000:1000 nginx
```

#### 3. Resource Exhaustion
- **Risk**: DoS attacks, resource starvation
- **Mitigation**: Set resource limits

```bash
# Limit resources
docker run --memory=512m --cpus=1.0 nginx
docker run --pids-limit=100 nginx
```

#### 4. Network Attacks
- **Risk**: Man-in-the-middle, data interception
- **Mitigation**: Use encrypted networks, limit exposure

```bash
# Secure networking
docker network create --internal secure-network
docker run --network secure-network nginx
```

## 10. How do you implement Docker security monitoring and auditing?

### Answer:

### Security Monitoring:

#### 1. Container Monitoring
```bash
# Monitor container processes
docker exec container_name ps aux

# Monitor network connections
docker exec container_name netstat -tlnp

# Monitor file system changes
docker exec container_name find / -type f -newer /tmp/timestamp
```

#### 2. Audit Logging
```bash
# Enable audit logging
dockerd --log-driver=json-file --log-opt max-size=10m

# Monitor Docker daemon logs
journalctl -u docker.service -f

# Audit container events
docker events --filter container=container_name
```

#### 3. Security Scanning
```bash
# Regular image scanning
docker scan nginx:latest

# Runtime security monitoring
docker exec container_name cat /proc/self/status

# Network security monitoring
docker exec container_name ss -tlnp
```

#### 4. Compliance Monitoring
```bash
# Check container compliance
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/docker-bench-security

# CIS Docker Benchmark
docker run --rm --net host --pid host --userns host \
  --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security
```

---
# Docker Compose

## 1. What is Docker Compose and how does it differ from Docker?

### Answer:
Docker Compose is a tool for defining and running multi-container Docker applications using YAML configuration files. It simplifies the management of complex applications with multiple interconnected services.

### Docker vs Docker Compose:

| Aspect | Docker | Docker Compose |
|--------|--------|----------------|
| **Scope** | Single container | Multi-container applications |
| **Configuration** | Command line arguments | YAML file (declarative) |
| **Orchestration** | Manual container management | Automated service orchestration |
| **Networking** | Manual network setup | Automatic service discovery |
| **Scaling** | Manual scaling | Built-in scaling commands |
| **Dependencies** | Manual dependency management | Automatic dependency resolution |

### When to Use Each:

#### Use Docker when:
- Single container applications
- Simple microservices
- Learning Docker basics
- Quick testing or prototyping

#### Use Docker Compose when:
- Multi-container applications
- Development environments
- Local testing of distributed systems
- Applications with databases, caches, queues
- Microservices architectures

### Practical Examples:

#### Docker Command (Single Container):
```bash
# Multiple manual commands needed
docker network create myapp-network
docker volume create myapp-data
docker run -d --name db --network myapp-network -v myapp-data:/var/lib/postgresql/data postgres:13
docker run -d --name web --network myapp-network -p 80:80 --link db nginx
```

#### Docker Compose (Multi-Container):
```yaml
# Single configuration file
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - db
  db:
    image: postgres:13
    volumes:
      - myapp-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  myapp-data:
```

```bash
# Single command to start everything
docker-compose up -d
```

## 2. Explain the structure of a docker-compose.yml file.

### Answer:

### Basic Structure:
```yaml
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

networks:
  default:
    driver: bridge
```

### Key Sections:
1. **version**: Compose file format version
2. **services**: Define application services
3. **volumes**: Define persistent storage
4. **networks**: Define custom networks

## 3. How do you manage environment variables in Docker Compose?

### Answer:

### Environment Variable Methods:

#### 1. Direct Definition
```yaml
services:
  web:
    image: nginx
    environment:
      - NODE_ENV=production
      - DEBUG=false
      - API_URL=https://api.example.com
```

#### 2. Environment File
```yaml
services:
  web:
    image: nginx
    env_file:
      - .env
      - .env.production
```

#### 3. Variable Substitution
```yaml
services:
  web:
    image: nginx
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - API_URL=${API_URL}
    ports:
      - "${PORT:-3000}:80"
```

#### 4. External Environment Files
```bash
# .env file
NODE_ENV=production
API_URL=https://api.example.com
PORT=8080
```

```yaml
services:
  web:
    image: nginx
    env_file:
      - .env
```

## 4. Explain Docker Compose networking and service discovery.

### Answer:

### Default Networking:
- **Network Name**: `{project_name}_default`
- **Driver**: Bridge
- **Service Discovery**: Automatic DNS resolution

### Service Communication:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    depends_on:
      - api
      - db

  api:
    image: node:16
    environment:
      - DB_HOST=db
      - DB_PORT=5432

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
```

### Custom Networks:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend

  api:
    image: node:16
    networks:
      - frontend
      - backend

  db:
    image: postgres:13
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### External Networks:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - external-network

networks:
  external-network:
    external: true
```

## 5. How do you manage volumes and persistent data in Docker Compose?

### Answer:

### Volume Types:

#### 1. Named Volumes
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local
```

#### 2. Bind Mounts
```yaml
version: '3.8'
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
```

#### 3. Anonymous Volumes
```yaml
version: '3.8'
services:
  web:
    image: nginx
    volumes:
      - /var/cache/nginx
```

#### 4. External Volumes
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - external_db_data:/var/lib/postgresql/data

volumes:
  external_db_data:
    external: true
```

### Volume Configuration:
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/postgres_data
```

## 6. What are Docker Compose profiles and how do you use them?

### Answer:

### Profiles Overview:
Profiles allow you to define different sets of services for different environments or use cases.

### Profile Definition:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    profiles:
      - production
      - staging

  db:
    image: postgres:13
    profiles:
      - production
      - staging
      - development

  redis:
    image: redis:alpine
    profiles:
      - production

  dev-tools:
    image: node:16
    profiles:
      - development
```

### Using Profiles:
```bash
# Start all services
docker-compose up

# Start specific profile
docker-compose --profile production up

# Start multiple profiles
docker-compose --profile production --profile monitoring up

# Start all services except specific profile
docker-compose --profile production up
```

### Environment-specific Compose Files:
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## 7. How do you scale services in Docker Compose?

### Answer:

### Scaling Services:
```bash
# Scale specific service
docker-compose up --scale web=3

# Scale multiple services
docker-compose up --scale web=3 --scale api=2

# Scale with specific configuration
docker-compose up --scale web=3 -d
```

### Load Balancing:
```yaml
version: '3.8'
services:
  nginx:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - web

  web:
    image: nginx
    deploy:
      replicas: 3
```

### Health Checks:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 8. Explain Docker Compose override files and inheritance.

### Answer:

### Override Files:
Override files allow you to extend or override the base configuration for different environments.

### Base Configuration:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "80:80"
    environment:
      - NODE_ENV=development
```

### Development Override:
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  web:
    volumes:
      - ./src:/app/src
    environment:
      - DEBUG=true
    ports:
      - "3000:80"
```

### Production Override:
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Using Override Files:
```bash
# Development (uses override automatically)
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# Custom override
docker-compose -f docker-compose.yml -f docker-compose.custom.yml up
```

## 9. How do you handle secrets and sensitive data in Docker Compose?

### Answer:

### Docker Secrets (Swarm Mode):
```yaml
version: '3.8'
services:
  web:
    image: nginx
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Environment Files:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    env_file:
      - .env.secrets
```

### External Secret Management:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    environment:
      - VAULT_ADDR=https://vault.example.com
      - VAULT_TOKEN=${VAULT_TOKEN}
```

### Volume Mounts for Secrets:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    volumes:
      - ./secrets:/app/secrets:ro
```

## 10. What are the best practices for Docker Compose in production?

### Answer:

### Production Best Practices:

#### 1. Resource Limits
```yaml
version: '3.8'
services:
  web:
    image: nginx
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

#### 2. Health Checks
```yaml
version: '3.8'
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### 3. Restart Policies
```yaml
version: '3.8'
services:
  web:
    image: nginx
    restart: unless-stopped
```

#### 4. Logging Configuration
```yaml
version: '3.8'
services:
  web:
    image: nginx
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 5. Security Configuration
```yaml
version: '3.8'
services:
  web:
    image: nginx
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
```

#### 6. Network Security
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend

  db:
    image: postgres:13
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

---
# Dockerfile Best Practices

## 1. What are the essential Dockerfile best practices for production?

### Answer:

#### 1. Use Specific Base Image Tags
```dockerfile
# Good: Specific version
FROM node:16.14.2-alpine

# Bad: Latest tag
FROM node:latest
```

#### 2. Use Multi-Stage Builds
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npm", "start"]
```

#### 3. Optimize Layer Caching
```dockerfile
# Good: Dependencies cached separately
COPY package*.json ./
RUN npm install
COPY . .

# Bad: Dependencies invalidated by code changes
COPY . .
RUN npm install
```

#### 4. Use .dockerignore
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.DS_Store
*.log
```

#### 5. Minimize Layers
```dockerfile
# Good: Combined commands
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Bad: Separate commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
```

## 2. How do you optimize Dockerfile for security?

### Answer:

#### 1. Use Non-Root User
```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Switch to non-root user
USER nextjs
```

#### 2. Use Minimal Base Images
```dockerfile
# Good: Minimal base image
FROM alpine:latest

# Bad: Large base image with unnecessary packages
FROM ubuntu:20.04
```

#### 3. Remove Package Managers
```dockerfile
# Install packages and remove package manager
RUN apk add --no-cache curl && \
    apk del apk-tools
```

#### 4. Use Read-Only Filesystem
```dockerfile
# Use read-only filesystem
FROM alpine:latest
RUN apk add --no-cache nginx
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 5. Scan for Vulnerabilities
```bash
# Scan image for vulnerabilities
docker scan nginx:latest

# Use Trivy for comprehensive scanning
trivy image nginx:latest
```

## 3. How do you optimize Dockerfile for size and performance?

### Answer:

#### 1. Use Alpine Linux
```dockerfile
# Good: Alpine-based image
FROM node:16-alpine

# Bad: Full Ubuntu image
FROM node:16
```

#### 2. Remove Unnecessary Files
```dockerfile
# Clean up after installation
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
```

#### 3. Use Multi-Stage Builds
```dockerfile
# Build stage
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN go build -o app

# Production stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/app .
CMD ["./app"]
```

#### 4. Optimize Dependencies
```dockerfile
# Install only production dependencies
RUN npm install --only=production

# Remove dev dependencies
RUN npm prune --production
```

#### 5. Use Distroless Images
```dockerfile
# Use distroless image
FROM gcr.io/distroless/java:11
COPY app.jar /app.jar
CMD ["java", "-jar", "/app.jar"]
```

## 4. How do you handle secrets and sensitive data in Dockerfiles?

### Answer:

#### 1. Use BuildKit Secrets
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

# Mount secrets during build
RUN --mount=type=secret,id=npm_token \
    npm config set //registry.npmjs.org/:_authToken $(cat /run/secrets/npm_token)
```

#### 2. Build with Secrets
```bash
# Build with secrets
docker buildx build --secret id=npm_token,src=./npm_token .
```

#### 3. Use Environment Variables
```dockerfile
# Use environment variables for configuration
ENV NODE_ENV=production
ENV PORT=3000
```

#### 4. Avoid Hardcoded Secrets
```dockerfile
# Bad: Hardcoded secret
RUN echo "password123" | some-command

# Good: Use environment variable
RUN echo "$SECRET_PASSWORD" | some-command
```

#### 5. Use Multi-Stage Builds for Secrets
```dockerfile
# Build stage with secrets
FROM node:16-alpine AS builder
RUN --mount=type=secret,id=npm_token \
    npm install

# Production stage without secrets
FROM node:16-alpine
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["npm", "start"]
```

## 5. How do you implement health checks in Dockerfiles?

### Answer:

#### 1. Add Health Check to Dockerfile
```dockerfile
# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

#### 2. Use Appropriate Health Check Commands
```dockerfile
# HTTP health check
HEALTHCHECK CMD curl -f http://localhost/health || exit 1

# Database health check
HEALTHCHECK CMD pg_isready -U postgres || exit 1

# Custom health check script
HEALTHCHECK CMD /app/health-check.sh || exit 1
```

#### 3. Configure Health Check Parameters
```dockerfile
# Configure health check timing
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

#### 4. Use Health Check in Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 6. How do you optimize Dockerfile for different environments?

### Answer:

#### 1. Use Build Arguments
```dockerfile
# Use build arguments for environment-specific configuration
ARG NODE_ENV=production
ARG PORT=3000

ENV NODE_ENV=$NODE_ENV
ENV PORT=$PORT
```

#### 2. Build with Arguments
```bash
# Build for development
docker build --build-arg NODE_ENV=development -t myapp:dev .

# Build for production
docker build --build-arg NODE_ENV=production -t myapp:prod .
```

#### 3. Use Multi-Stage Builds for Environments
```dockerfile
# Development stage
FROM node:16-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Production stage
FROM node:16-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY . .
CMD ["npm", "start"]
```

#### 4. Use Different Base Images
```dockerfile
# Development: Full image with dev tools
FROM node:16 AS development

# Production: Minimal image
FROM node:16-alpine AS production
```

## 7. How do you handle dependencies and package management in Dockerfiles?

### Answer:

#### 1. Pin Package Versions
```dockerfile
# Good: Pin specific versions
RUN npm install express@4.18.2 lodash@4.17.21

# Bad: Install latest versions
RUN npm install express lodash
```

#### 2. Use Package Lock Files
```dockerfile
# Copy package files first
COPY package*.json ./
RUN npm ci --only=production
```

#### 3. Clean Package Cache
```dockerfile
# Clean package cache after installation
RUN npm install && npm cache clean --force
```

#### 4. Use Multi-Stage Builds for Dependencies
```dockerfile
# Dependencies stage
FROM node:16-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
CMD ["npm", "start"]
```

#### 5. Handle System Dependencies
```dockerfile
# Install system dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    && npm install \
    && apk del python3 make g++
```

## 8. How do you implement proper logging and monitoring in Dockerfiles?

### Answer:

#### 1. Configure Logging
```dockerfile
# Configure logging driver
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 2. Use Structured Logging
```dockerfile
# Use structured logging
FROM node:16-alpine
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```

#### 3. Add Monitoring Endpoints
```dockerfile
# Add health and metrics endpoints
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY health-check.sh /usr/local/bin/health-check.sh
RUN chmod +x /usr/local/bin/health-check.sh
EXPOSE 80
HEALTHCHECK CMD /usr/local/bin/health-check.sh
CMD ["nginx", "-g", "daemon off;"]
```

## 9. How do you optimize Dockerfile for CI/CD pipelines?

### Answer:

#### 1. Use Build Cache
```dockerfile
# Optimize for build cache
COPY package*.json ./
RUN npm install
COPY . .
```

#### 2. Use BuildKit Features
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

# Use BuildKit cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm install
```

#### 3. Parallel Builds
```dockerfile
# Enable parallel builds
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["npm", "start"]
```

#### 4. Use Multi-Platform Builds
```dockerfile
# Build for multiple platforms
FROM --platform=$BUILDPLATFORM node:16-alpine AS builder
WORKDIR /app
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["npm", "start"]
```

## 10. How do you handle configuration management in Dockerfiles?

### Answer:

#### 1. Use Environment Variables
```dockerfile
# Use environment variables for configuration
ENV NODE_ENV=production
ENV PORT=3000
ENV DB_HOST=localhost
ENV DB_PORT=5432
```

#### 2. Use Configuration Files
```dockerfile
# Copy configuration files
COPY config/ /app/config/
COPY nginx.conf /etc/nginx/nginx.conf
```

#### 3. Use Init Scripts
```dockerfile
# Use init script for configuration
COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh
ENTRYPOINT ["/usr/local/bin/init.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

#### 4. Use Configuration Management Tools
```dockerfile
# Use configuration management
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY config/ /etc/nginx/conf.d/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---
# Latest Features

## 1. Docker Init - Project Initialization

### Answer:
Docker Init is a new feature that automatically generates Docker-related files for your project, making it easier to containerize applications.

### Features:
- **Automatic Detection**: Detects project type (Node.js, Python, Go, etc.)
- **File Generation**: Creates Dockerfile, docker-compose.yml, and .dockerignore
- **Best Practices**: Applies Docker best practices automatically
- **Language Support**: Supports multiple programming languages

### Usage:
```bash
# Initialize Docker files in current directory
docker init

# Initialize with specific project type
docker init --template node

# Initialize with custom name
docker init --name my-app
```

### Generated Files:
```dockerfile
# Example generated Dockerfile for Node.js
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Benefits:
- **Quick Start**: Rapid project containerization
- **Best Practices**: Follows Docker recommendations
- **Consistency**: Standardized project structure
- **Learning**: Shows proper Docker patterns

## 2. Docker Ask Gordon - AI-Powered Assistance

### Answer:
Docker Ask Gordon is an AI-powered assistant integrated into Docker Desktop that helps developers with Docker-related questions and tasks.

### Features:
- **Natural Language Queries**: Ask questions in plain English
- **Code Generation**: Generate Dockerfiles and configurations
- **Troubleshooting**: Get help with Docker issues
- **Best Practices**: Receive recommendations for optimization

### Usage Examples:
```bash
# Ask questions about Docker
"How do I optimize my Dockerfile for production?"

# Get help with specific issues
"My container is running out of memory, what should I do?"

# Request code generation
"Create a Dockerfile for a Python Flask application"
```

### Capabilities:
- **Dockerfile Optimization**: Suggests improvements
- **Security Recommendations**: Identifies security issues
- **Performance Tuning**: Provides performance tips
- **Troubleshooting**: Helps debug problems

## 3. Running AI Models with Docker

### Answer:
Docker provides an excellent platform for running AI models with consistent environments and easy deployment.

### AI Model Containerization:
```dockerfile
# Example Dockerfile for AI model
FROM python:3.9-slim

WORKDIR /app

# Install AI/ML dependencies
RUN pip install torch torchvision transformers

# Copy model files
COPY model/ ./model/
COPY app.py .

# Expose API port
EXPOSE 8000

# Run AI model server
CMD ["python", "app.py"]
```

### Popular AI Models in Docker:
```bash
# Run Hugging Face models
docker run -p 8000:8000 huggingface/transformers-pytorch-gpu

# Run TensorFlow models
docker run -p 8501:8501 tensorflow/serving

# Run PyTorch models
docker run -p 8080:8080 pytorch/pytorch
```

### GPU Support:
```dockerfile
# Dockerfile with GPU support
FROM nvidia/cuda:11.8-runtime-ubuntu20.04

# Install Python and AI libraries
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Copy model and application
COPY . /app
WORKDIR /app

CMD ["python3", "app.py"]
```

### Docker Compose for AI:
```yaml
version: '3.8'
services:
  ai-model:
    build: .
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 4. Docker Multi-Platform Builds

### Answer:
Docker's multi-platform build feature allows you to create images that work on different architectures (AMD64, ARM64, etc.).

### Buildx for Multi-Platform:
```bash
# Create buildx builder
docker buildx create --name multiplatform

# Use the builder
docker buildx use multiplatform

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .

# Build and push to registry
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .
```

### Dockerfile for Multi-Platform:
```dockerfile
FROM --platform=$BUILDPLATFORM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npm", "start"]
```

### Platform-Specific Builds:
```bash
# Build for specific platform
docker buildx build --platform linux/amd64 -t myapp:amd64 .

# Build for ARM64
docker buildx build --platform linux/arm64 -t myapp:arm64 .

# Build for Windows
docker buildx build --platform windows/amd64 -t myapp:windows .
```

### Benefits:
- **Cross-Platform**: Support multiple architectures
- **Efficiency**: Single build process for multiple platforms
- **Compatibility**: Works on different hardware
- **Deployment**: Deploy to various environments

## 5. Docker BuildKit and Advanced Build Features

### Answer:
Docker BuildKit is the next-generation build engine that provides advanced features for building Docker images.

### BuildKit Features:
- **Parallel Builds**: Build multiple stages in parallel
- **Build Cache**: Advanced caching mechanisms
- **Secret Mounts**: Secure secret handling during builds
- **SSH Agent**: SSH key forwarding during builds

### Enable BuildKit:
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Or use buildx
docker buildx build .
```

### Advanced Dockerfile Features:
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

# Mount secrets during build
RUN --mount=type=secret,id=npm_token \
    npm config set //registry.npmjs.org/:_authToken $(cat /run/secrets/npm_token)

# Mount SSH keys
RUN --mount=type=ssh \
    git clone git@github.com:user/repo.git

# Mount cache
RUN --mount=type=cache,target=/root/.npm \
    npm install
```

### Build with Secrets:
```bash
# Build with secrets
docker buildx build --secret id=npm_token,src=./npm_token .

# Build with SSH
docker buildx build --ssh default .
```

### Benefits:
- **Performance**: Faster builds with parallel execution
- **Security**: Secure secret handling
- **Flexibility**: Advanced build features
- **Efficiency**: Better caching and optimization

---

# Advanced Topics

## 1. Docker Swarm vs Kubernetes - When to Use Which?

### Answer:

### Docker Swarm
**Pros:**
- Simple setup and management
- Native Docker integration
- Built-in service discovery
- Easy scaling and load balancing
- Good for small to medium deployments

**Cons:**
- Limited advanced features
- Smaller ecosystem
- Less flexibility for complex scenarios
- Limited monitoring and logging

### Kubernetes
**Pros:**
- Rich feature set
- Large ecosystem
- Advanced networking and storage
- Extensive monitoring and logging
- Better for complex, large-scale deployments

**Cons:**
- Complex setup and management
- Steep learning curve
- Resource intensive
- Overkill for simple applications

### When to Choose:

| Scenario | Recommendation | Reason |
|----------|----------------|---------|
| Small team, simple apps | Docker Swarm | Easier to manage |
| Large enterprise | Kubernetes | More features and ecosystem |
| Rapid prototyping | Docker Swarm | Quick setup |
| Production at scale | Kubernetes | Better tooling and support |
| Docker expertise | Docker Swarm | Leverage existing knowledge |
| Cloud-native apps | Kubernetes | Better cloud integration |

## 2. Container Runtime Security - Beyond Basic Docker

### Answer:

#### 1. Container Runtime Security
```bash
# Use gVisor for additional isolation
docker run --runtime=runsc nginx

# Use Kata Containers for VM-level isolation
docker run --runtime=kata nginx
```

#### 2. Image Security Scanning
```bash
# Scan for vulnerabilities
docker scan nginx:latest

# Use Trivy for comprehensive scanning
trivy image nginx:latest

# Check for secrets in images
trivy image --security-checks secret nginx:latest
```

#### 3. Runtime Security Monitoring
```bash
# Monitor container behavior
docker exec container_name ps aux
docker exec container_name netstat -tlnp
docker exec container_name lsof -i
```

#### 4. Network Security
```bash
# Use encrypted networks
docker network create --driver overlay --opt encrypted secure-network

# Implement network policies
docker run --network secure-network --cap-drop NET_RAW nginx
```

#### 5. Storage Security
```bash
# Use encrypted volumes
docker volume create --driver local --opt type=tmpfs --opt device=tmpfs encrypted-vol

# Implement access controls
docker run --user 1000:1000 --read-only nginx
```

## 3. Docker Performance Optimization

### Answer:

#### 1. Image Optimization
```dockerfile
# Multi-stage builds
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npm", "start"]
```

#### 2. Container Resource Optimization
```bash
# Set appropriate resource limits
docker run --memory=512m --cpus=1.0 nginx

# Use tmpfs for temporary files
docker run --tmpfs /tmp:noexec,nosuid,size=100m nginx

# Optimize I/O
docker run --device-read-bps /dev/sda:1mb nginx
```

#### 3. Storage Driver Optimization
```bash
# Use overlay2 storage driver
dockerd --storage-driver=overlay2

# Configure storage options
dockerd --storage-opt overlay2.override_kernel_check=true
```

#### 4. Network Optimization
```bash
# Use host networking for performance
docker run --network host nginx

# Optimize bridge network
docker network create --driver bridge --opt com.docker.network.bridge.enable_icc=false mynetwork
```

#### 5. Registry Optimization
```bash
# Use local registry mirror
dockerd --registry-mirror=https://mirror.example.com

# Implement registry caching
docker run -d -p 5000:5000 --name registry registry:2
```

## 4. Docker in CI/CD Pipelines

### Answer:

#### 1. Build Optimization
```yaml
# GitHub Actions example
name: Build and Push
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      
      - name: Build image
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: myapp:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

#### 2. Multi-stage Builds
```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
CMD ["npm", "start"]
```

#### 3. Security Scanning
```yaml
# Security scanning in CI
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
```

#### 4. Testing in Containers
```yaml
# Run tests in container
- name: Run tests
  run: |
    docker run --rm -v $(pwd):/app -w /app node:16-alpine npm test
```

## 5. Docker Monitoring and Observability

### Answer:

#### 1. Container Metrics
```bash
# Use cAdvisor for container metrics
docker run -d -p 8080:8080 --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro gcr.io/cadvisor/cadvisor

# Monitor with Prometheus
docker run -d -p 9090:9090 prom/prometheus
```

#### 2. Log Management
```bash
# Configure log driver
docker run --log-driver=json-file --log-opt max-size=10m nginx

# Use syslog driver
docker run --log-driver=syslog nginx

# Use fluentd driver
docker run --log-driver=fluentd nginx
```

#### 3. Health Checks
```dockerfile
# Add health check to Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

#### 4. Distributed Tracing
```bash
# Use Jaeger for tracing
docker run -d -p 16686:16686 jaegertracing/all-in-one
```

---

# Practical Scenarios

## 1. Scenario: Container Won't Start - Debugging Steps

### Problem:
A container fails to start with exit code 1. How do you debug this issue?

### Debugging Steps:

#### 1. Check Container Logs
```bash
# View container logs
docker logs container_name

# Follow logs in real-time
docker logs -f container_name

# View logs with timestamps
docker logs -t container_name
```

#### 2. Inspect Container Configuration
```bash
# Inspect container details
docker inspect container_name

# Check container status
docker ps -a

# View container events
docker events --filter container=container_name
```

#### 3. Test Container Manually
```bash
# Run container interactively
docker run -it image_name /bin/bash

# Run with different entrypoint
docker run --entrypoint /bin/bash image_name

# Check if image exists
docker images | grep image_name
```

#### 4. Check Resource Constraints
```bash
# Check available resources
docker system df
docker system info

# Check if ports are available
netstat -tlnp | grep :80
```

#### 5. Validate Dockerfile
```bash
# Build image with verbose output
docker build --no-cache -t test-image .

# Check Dockerfile syntax
docker build --target debug .
```

## 2. Scenario: High Memory Usage in Container

### Problem:
Container is consuming excessive memory. How do you investigate and resolve?

### Investigation Steps:

#### 1. Monitor Container Resources
```bash
# View container stats
docker stats container_name

# Monitor specific container
docker stats --no-stream container_name

# Check container memory usage
docker exec container_name cat /proc/meminfo
```

#### 2. Identify Memory Leaks
```bash
# Check process memory usage
docker exec container_name ps aux --sort=-%mem

# Monitor memory over time
watch -n 1 'docker stats --no-stream container_name'

# Check for memory leaks in application
docker exec container_name cat /proc/self/status | grep VmRSS
```

#### 3. Set Memory Limits
```bash
# Set memory limit
docker run --memory=512m nginx

# Set memory limit with swap
docker run --memory=512m --memory-swap=1g nginx

# Set OOM kill policy
docker run --oom-kill-disable nginx
```

#### 4. Optimize Application
```bash
# Check application configuration
docker exec container_name cat /app/config.json

# Monitor garbage collection
docker exec container_name jstat -gc 1

# Check for memory leaks
docker exec container_name valgrind --tool=memcheck /app/binary
```

## 3. Scenario: Container Network Connectivity Issues

### Problem:
Containers cannot communicate with each other or external services.

### Troubleshooting Steps:

#### 1. Check Network Configuration
```bash
# List networks
docker network ls

# Inspect network
docker network inspect network_name

# Check container network
docker inspect container_name | grep -A 20 "NetworkSettings"
```

#### 2. Test Network Connectivity
```bash
# Test DNS resolution
docker exec container_name nslookup google.com

# Test connectivity
docker exec container_name ping -c 3 8.8.8.8

# Check port connectivity
docker exec container_name telnet hostname port
```

#### 3. Verify Port Mapping
```bash
# Check port mappings
docker port container_name

# Test port accessibility
curl -I http://localhost:8080

# Check if port is listening
docker exec container_name netstat -tlnp
```

#### 4. Network Debugging
```bash
# Check routing table
docker exec container_name ip route

# Check network interfaces
docker exec container_name ip addr

# Test with different network
docker run --network host nginx
```

## 4. Scenario: Docker Image Build Failures

### Problem:
Docker image build fails with various errors.

### Common Issues and Solutions:

#### 1. Base Image Issues
```dockerfile
# Problem: Base image not found
FROM nonexistent:latest

# Solution: Use valid base image
FROM ubuntu:20.04
```

#### 2. Package Installation Failures
```dockerfile
# Problem: Package not found
RUN apt-get install -y nonexistent-package

# Solution: Update package list first
RUN apt-get update && apt-get install -y package-name
```

#### 3. Permission Issues
```dockerfile
# Problem: Permission denied
COPY . /app
RUN chmod +x /app/script.sh

# Solution: Set proper permissions
COPY --chown=app:app . /app
RUN chmod +x /app/script.sh
```

#### 4. Build Context Issues
```bash
# Problem: Large build context
docker build .

# Solution: Use .dockerignore
echo "node_modules" >> .dockerignore
echo "*.log" >> .dockerignore
```

## 5. Scenario: Container Performance Issues

### Problem:
Container performance is slow or inconsistent.

### Performance Analysis:

#### 1. Resource Monitoring
```bash
# Monitor CPU usage
docker stats --no-stream container_name

# Check CPU limits
docker inspect container_name | grep -i cpu

# Monitor I/O
docker exec container_name iostat -x 1
```

#### 2. Application Profiling
```bash
# Profile CPU usage
docker exec container_name top -p 1

# Check memory usage
docker exec container_name free -h

# Monitor disk I/O
docker exec container_name iotop
```

#### 3. Optimize Container Configuration
```bash
# Set CPU limits
docker run --cpus="1.5" nginx

# Set I/O limits
docker run --device-read-bps /dev/sda:1mb nginx

# Use tmpfs for temporary files
docker run --tmpfs /tmp:noexec,nosuid,size=100m nginx
```

---

## Summary

This comprehensive guide covers 90+ Docker interview questions across 9 categories:

- **Basic Concepts**: Fundamental Docker knowledge
- **Docker Architecture**: Deep dive into Docker's internal structure
- **Docker Networking**: Container networking and communication
- **Docker Security**: Security best practices and threat mitigation
- **Docker Compose**: Multi-container application orchestration
- **Dockerfile Best Practices**: Optimized container image creation
- **Latest Features**: Cutting-edge Docker capabilities
- **Advanced Topics**: Complex scenarios and enterprise use cases
- **Practical Scenarios**: Real-world troubleshooting and problem-solving

Each question includes detailed explanations, practical examples, and code snippets to help you understand and demonstrate Docker expertise in interviews and real-world scenarios.

**Good luck with your Docker interviews! 🐳**