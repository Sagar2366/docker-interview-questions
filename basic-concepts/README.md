# Basic Docker Concepts

## 1. What is Docker and how does it differ from Virtual Machines?

### Answer:
Docker is a containerization platform that allows you to package applications and their dependencies into lightweight, portable containers. Unlike virtual machines, Docker containers share the host OS kernel and run as isolated processes.

### Visual Comparison:
```
Virtual Machines                    Docker Containers
┌─────────────────────────────┐    ┌─────────────────────────────┐
│        Application          │    │        Application          │
├─────────────────────────────┤    ├─────────────────────────────┤
│         Guest OS            │    │        Docker Engine        │
├─────────────────────────────┤    ├─────────────────────────────┤
│        Hypervisor           │    │         Host OS             │
├─────────────────────────────┤    ├─────────────────────────────┤
│         Host OS             │    │        Hardware             │
├─────────────────────────────┤    └─────────────────────────────┘
│        Hardware             │
└─────────────────────────────┘
```

### Key Differences:

| Aspect | Docker Containers | Virtual Machines |
|--------|------------------|------------------|
| **Resource Usage** | Lightweight, shares OS kernel | Heavy, requires full OS |
| **Startup Time** | Seconds | Minutes |
| **Isolation** | Process-level | Hardware-level |
| **Performance** | Near-native | Hypervisor overhead |
| **Size** | MBs | GBs |
| **Density** | 100s per host | 10s per host |
| **Portability** | High (same kernel) | Medium (hypervisor dependent) |

### Practical Examples:
```bash
# Docker container - starts instantly
time docker run --rm hello-world
# Output: real 0m2.1s

# Check container resource usage
docker stats --no-stream
# Shows minimal CPU/Memory usage

# Multiple containers sharing resources
docker run -d --name web1 nginx
docker run -d --name web2 nginx
docker run -d --name web3 nginx
# All share the same host kernel
```

### When to Use Each:
- **Docker**: Microservices, CI/CD, development environments
- **VMs**: Legacy applications, different OS requirements, strong isolation needs

## 2. Explain Docker's architecture and its main components.

### Answer:
Docker follows a client-server architecture with these main components:

### Docker Architecture Diagram:
```
┌─────────────────┐     REST API     ┌─────────────────┐
│  Docker Client  │ ◄──────────────► │  Docker Daemon  │
│                 │                  │   (dockerd)     │
│ • docker build  │                  │                 │
│ • docker pull   │                  │ ┌─────────────┐ │
│ • docker run    │                  │ │ containerd  │ │
└─────────────────┘                  │ └─────────────┘ │
                                     │ ┌─────────────┐ │
┌─────────────────┐                  │ │    runc     │ │
│ Docker Registry │                  │ └─────────────┘ │
│                 │                  └─────────────────┘
│ • Docker Hub    │                           │
│ • Private Reg   │                           ▼
│ • ECR/GCR       │                  ┌─────────────────┐
└─────────────────┘                  │   Containers    │
                                     │                 │
                                     │ ┌─────┐ ┌─────┐ │
                                     │ │App1 │ │App2 │ │
                                     │ └─────┘ └─────┘ │
                                     └─────────────────┘
```

### Component Details:

#### 1. **Docker Client** (`docker` CLI)
- **Purpose**: User interface to Docker
- **Communication**: REST API calls to daemon
- **Location**: Can be local or remote

```bash
# Client commands
docker version    # Shows client and server versions
docker info       # Displays system information
docker --help     # Lists available commands
```

#### 2. **Docker Daemon** (`dockerd`)
- **Purpose**: Core Docker service
- **Responsibilities**: 
  - Manages containers, images, networks, volumes
  - Handles API requests
  - Communicates with containerd

```bash
# Daemon management
sudo systemctl status docker    # Check daemon status
sudo systemctl start docker     # Start daemon
journalctl -u docker.service    # View daemon logs
```

#### 3. **containerd**
- **Purpose**: High-level container runtime
- **Functions**: Container lifecycle management
- **Standards**: OCI compliant

#### 4. **runc**
- **Purpose**: Low-level container runtime
- **Functions**: Creates and runs containers
- **Standards**: OCI runtime specification

#### 5. **Docker Registry**
- **Purpose**: Stores and distributes images
- **Types**: Public (Docker Hub) or Private

```bash
# Registry operations
docker pull nginx:latest        # Pull from registry
docker push myapp:v1.0          # Push to registry
docker search ubuntu            # Search registry
```

### Communication Flow:
```
User Command → Docker Client → REST API → Docker Daemon → containerd → runc → Container
```

## 3. What is a Dockerfile and what are its key instructions?

### Answer:
A Dockerfile is a text file containing step-by-step instructions to build a Docker image. It's like a recipe that defines how to create a container image.

### Dockerfile Build Process:
```
Dockerfile ──build──► Docker Image ──run──► Container
    │                      │                   │
    │                      │                   │
┌───▼────┐            ┌────▼────┐         ┌────▼────┐
│FROM    │            │ Layer 1 │         │Running  │
│RUN     │   ────►    │ Layer 2 │  ────►  │Process  │
│COPY    │            │ Layer 3 │         │         │
│CMD     │            │ Layer N │         │         │
└────────┘            └─────────┘         └─────────┘
```

### Essential Dockerfile Instructions:

#### **FROM** - Base Image
```dockerfile
# Always first instruction
FROM node:16-alpine          # Specific version (recommended)
FROM ubuntu:20.04            # OS base
FROM scratch                 # Empty base (advanced)
```

#### **WORKDIR** - Working Directory
```dockerfile
WORKDIR /app                 # Sets working directory
# All subsequent commands run from /app
```

#### **COPY vs ADD** - File Operations
```dockerfile
# COPY (preferred) - simple file copy
COPY package*.json ./        # Copy specific files
COPY src/ ./src/            # Copy directories

# ADD - advanced features (URLs, tar extraction)
ADD https://example.com/file.tar.gz /tmp/
ADD archive.tar.gz /opt/     # Auto-extracts
```

#### **RUN** - Execute Commands
```dockerfile
# Install packages
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Multiple commands in one layer (efficient)
RUN npm install && npm cache clean --force
```

#### **EXPOSE** - Document Ports
```dockerfile
EXPOSE 3000              # Documents port (doesn't publish)
EXPOSE 80 443            # Multiple ports
```

#### **ENV** - Environment Variables
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV PATH=/app/bin:$PATH
```

#### **USER** - Security
```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs              # Switch to non-root user
```

### Complete Example with Best Practices:
```dockerfile
# Multi-stage build example
FROM node:16-alpine AS builder
WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine AS production
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --chown=nextjs:nodejs package*.json ./

# Switch to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["npm", "start"]
```

### Layer Optimization:
```dockerfile
# ❌ Bad - creates many layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean

# ✅ Good - single layer
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## 4. What is the difference between CMD and ENTRYPOINT?

### Answer:
Both CMD and ENTRYPOINT define what command runs when a container starts, but they behave differently with runtime arguments.

### Behavior Comparison:

| Aspect | CMD | ENTRYPOINT |
|--------|-----|------------|
| **Override** | Completely replaced by `docker run` args | Cannot be overridden |
| **Runtime Args** | Replace entire CMD | Appended to ENTRYPOINT |
| **Purpose** | Default command/args | Fixed command |
| **Flexibility** | High | Low |
| **Use Case** | Optional defaults | Required executable |

### Visual Representation:
```
CMD Behavior:
┌─────────────┐    docker run    ┌─────────────┐
│ CMD ["app"] │ ──────────────►  │ "new-cmd"   │
└─────────────┘    new-cmd       └─────────────┘
                                 (CMD replaced)

ENTRYPOINT Behavior:
┌─────────────────-─┐    docker run    ┌──────────────────┐
│ ENTRYPOINT ["app"]│ ──────────────►  │ "app" + "args"   │
└───────────────────┘    args          └──────────────────┘
                                      (args appended)
```

### Practical Examples:

#### **CMD Examples:**
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

#### **ENTRYPOINT Examples:**
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

### **Combined Usage (Best Practice):**
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

### **Real-World Examples:**

#### **Web Server (CMD):**
```dockerfile
FROM nginx:alpine
CMD ["nginx", "-g", "daemon off;"]
# Allows: docker run nginx-image nginx-debug
```

#### **Database (ENTRYPOINT + CMD):**
```dockerfile
FROM postgres:13
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]
# Always runs entrypoint script, but can change database command
```

#### **CLI Tool (ENTRYPOINT):**
```dockerfile
FROM alpine
COPY mytool /usr/local/bin/
ENTRYPOINT ["mytool"]
# Always runs mytool, arguments passed to it
```

### **Shell vs Exec Form:**
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

### **Best Practices:**
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

#### **1. Layer Creation:**
```dockerfile
FROM ubuntu:20.04          # Layer 1 (base)
RUN apt-get update         # Layer 2 (package index)
RUN apt-get install -y git # Layer 3 (git installation)
WORKDIR /app              # Layer 4 (directory creation)
COPY app.py .             # Layer 5 (file copy)
CMD ["python", "app.py"]  # Layer 6 (metadata only)
```

#### **2. Layer Sharing:**
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

### **Copy-on-Write (CoW) Mechanism:**
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
└───────────────────────────────────────────┘
```

### **Layer Caching Benefits:**

#### **Build Cache Example:**
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

### **Practical Commands:**

#### **View Image Layers:**
```bash
# Show image history
docker history nginx:alpine

# Detailed layer information
docker image inspect nginx:alpine

# Show layer sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

#### **Analyze Layer Changes:**
```bash
# Show changes in container
docker diff container_name

# Export container changes
docker export container_name > container.tar

# Save image layers
docker save nginx:alpine > nginx.tar
```

### **Layer Optimization Strategies:**

#### **1. Order Instructions by Change Frequency:**
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

#### **2. Combine Related Commands:**
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

#### **3. Use Multi-stage Builds:**
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

### **Layer Limits and Considerations:**
- **Maximum layers**: 127 layers per image
- **Layer size**: Each layer adds to total image size
- **Cache invalidation**: Changes invalidate all subsequent layers
- **Security**: Each layer can introduce vulnerabilities

### **Troubleshooting Layer Issues:**
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

### **Why Volumes are Important:**
- **Data Persistence**: Data survives container lifecycle
- **Performance**: Better I/O than container filesystem
- **Sharing**: Multiple containers can share data
- **Backup**: Easy to backup and restore
- **Portability**: Independent of host filesystem

### **Volume Types Comparison:**

```
Volume Types:

1. Named Volumes (Recommended)
┌─────────────────────────────────────┐
│ Host: /var/lib/docker/volumes/      │
│       mydata/_data                  │
├─────────────────────────────────────┤
│ Container: /app/data                │
└─────────────────────────────────────┘

2. Anonymous Volumes
┌─────────────────────────────────────┐
│ Host: /var/lib/docker/volumes/      │
│       abc123.../_data               │
├─────────────────────────────────────┤
│ Container: /app/data                │
└─────────────────────────────────────┘

3. Bind Mounts
┌─────────────────────────────────────┐
│ Host: /home/user/data               │
├─────────────────────────────────────┤
│ Container: /app/data                │
└─────────────────────────────────────┘

4. tmpfs Mounts (Memory)
┌─────────────────────────────────────┐
│ Host: RAM                           │
├─────────────────────────────────────┤
│ Container: /app/temp                │
└─────────────────────────────────────┘
```

### **Volume Types in Detail:**

#### **1. Named Volumes (Recommended)**
```bash
# Create named volume
docker volume create mydata

# Use named volume
docker run -d -v mydata:/app/data nginx

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata
```

**Benefits:**
- Managed by Docker
- Easy to backup
- Portable across hosts
- Better performance

#### **2. Anonymous Volumes**
```bash
# Create anonymous volume
docker run -d -v /app/data nginx

# Docker generates random name
docker volume ls
# DRIVER    VOLUME NAME
# local     a1b2c3d4e5f6...
```

**Use Cases:**
- Temporary data
- Cache directories
- Build artifacts

#### **3. Bind Mounts**
```bash
# Bind mount host directory
docker run -d -v /host/data:/app/data nginx

# Bind mount with read-only
docker run -d -v /host/config:/app/config:ro nginx

# Bind mount current directory
docker run -d -v $(pwd):/app nginx
```

**Use Cases:**
- Development (live code editing)
- Configuration files
- Log files
- Shared host resources

#### **4. tmpfs Mounts (Memory)**
```bash
# Mount tmpfs (Linux only)
docker run -d --tmpfs /app/temp nginx

# With size limit
docker run -d --tmpfs /app/temp:size=100m nginx
```

**Use Cases:**
- Sensitive data
- Temporary processing
- High-speed cache

### **Volume Management Commands:**

#### **Volume Operations:**
```bash
# Create volume
docker volume create --driver local myvolume

# List volumes
docker volume ls

# Inspect volume details
docker volume inspect myvolume

# Remove volume
docker volume rm myvolume

# Remove unused volumes
docker volume prune

# Remove all volumes
docker volume rm $(docker volume ls -q)
```

#### **Volume with Options:**
```bash
# Create volume with options
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.1,rw \
  --opt device=:/path/to/dir \
  nfs-volume
```

### **Practical Examples:**

#### **Database Persistence:**
```bash
# PostgreSQL with named volume
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:13

# Data persists even if container is removed
docker rm -f postgres
docker run -d --name postgres2 -v pgdata:/var/lib/postgresql/data postgres:13
# Data is still there!
```

#### **Development Environment:**
```bash
# Bind mount for live development
docker run -d \
  --name dev-server \
  -v $(pwd):/app \
  -v node_modules:/app/node_modules \
  -p 3000:3000 \
  node:16-alpine \
  npm run dev
```

#### **Configuration Management:**
```bash
# Read-only config bind mount
docker run -d \
  --name nginx \
  -v /host/nginx.conf:/etc/nginx/nginx.conf:ro \
  -p 80:80 \
  nginx
```

### **Docker Compose Volume Examples:**

```yaml
version: '3.8'
services:
  web:
    image: nginx
    volumes:
      - web-data:/usr/share/nginx/html    # Named volume
      - ./config:/etc/nginx:ro            # Bind mount (read-only)
      - /tmp                              # Anonymous volume
  
  db:
    image: postgres:13
    volumes:
      - db-data:/var/lib/postgresql/data  # Named volume
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  web-data:     # Named volume definition
  db-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /host/db/data
```

### **Volume Backup and Restore:**

#### **Backup Volume:**
```bash
# Backup named volume
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/mydata-backup.tar.gz -C /data .
```

#### **Restore Volume:**
```bash
# Restore volume from backup
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  alpine \
  tar xzf /backup/mydata-backup.tar.gz -C /data
```

### **Performance Considerations:**

| Mount Type | Performance | Use Case |
|------------|-------------|----------|
| **Named Volume** | Best | Production data |
| **Anonymous Volume** | Good | Temporary data |
| **Bind Mount** | Good* | Development |
| **tmpfs** | Fastest | Temporary/sensitive |

*Bind mount performance depends on host filesystem

### **Security Best Practices:**
```bash
# Use read-only mounts when possible
docker run -v /host/config:/app/config:ro nginx

# Limit volume access with user mapping
docker run --user 1000:1000 -v mydata:/data nginx

# Use tmpfs for sensitive data
docker run --tmpfs /app/secrets nginx
```

### **Troubleshooting Volumes:**
```bash
# Check volume usage
docker system df -v

# Find containers using volume
docker ps -a --filter volume=mydata

# Check volume mount points
docker inspect container_name | grep -A 10 "Mounts"

# Access volume data directly
docker run --rm -v mydata:/data alpine ls -la /data
```

## 7. What is the difference between docker run and docker start?

### Answer:
Understanding the difference between `docker run` and `docker start` is crucial for container lifecycle management.

### Container Lifecycle:
```
Image ──docker run──► Container (Running) ──docker stop──► Container (Stopped)
  │                         │                                      │
  │                         │                                      │
  └─────────────────────────┼──────────────────────────────────────┘
                            │
                    docker start ◄─────────────────────────────────┘
```

### Command Comparison:

| Aspect | docker run | docker start |
|--------|------------|---------------|
| **Purpose** | Creates and starts new container | Starts existing stopped container |
| **Source** | Uses image as template | Uses existing container |
| **Parameters** | Can pass new parameters | Uses existing configuration |
| **Container ID** | Always creates new container | Reuses existing container |
| **Flexibility** | High (full configuration) | Low (existing config only) |
| **Use Case** | First-time container creation | Restart stopped containers |

### Practical Examples:

#### **docker run - Create and Start:**
```bash
# Create and start new container
docker run -d --name web -p 80:80 nginx
# Creates new container with ID: abc123...

# Run another container from same image
docker run -d --name web2 -p 8080:80 nginx
# Creates different container with ID: def456...

# Run with different configuration
docker run -d --name web3 -p 9090:80 -e ENV=prod nginx
```

#### **docker start - Start Existing:**
```bash
# Stop the container
docker stop web

# Start the existing container
docker start web
# Uses same container ID: abc123...
# Uses same configuration: -p 80:80

# Cannot change configuration
docker start web -p 8080:80  # ❌ This won't work
```

### Container States Diagram:
```
┌─────────────┐    docker run      ┌─────────────┐
│    Image    │ ─────────────────► │   Running   │
│             │                    │  Container  │
└─────────────┘                    └──────┬──────┘
                                          │
                                   docker stop
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │   Stopped   │
                                   │  Container  │
                                   └──────┬──────┘
                                          │
                                   docker start
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │   Running   │
                                   │  Container  │
                                   └─────────────┘
```

### Advanced Usage:

#### **Interactive Containers:**
```bash
# Run interactive container
docker run -it --name ubuntu-shell ubuntu bash
# Exit container (stops it)
exit

# Start stopped interactive container
docker start ubuntu-shell
# Container starts but not attached

# Start and attach to container
docker start -ai ubuntu-shell
# Now you're back in the shell
```

#### **Container Restart Policies:**
```bash
# Run with restart policy
docker run -d --name web --restart unless-stopped nginx

# Container will auto-start after docker daemon restart
sudo systemctl restart docker
# Container 'web' automatically starts
```

### Monitoring Container States:
```bash
# List all containers (running and stopped)
docker ps -a

# Check container status
docker inspect web --format '{{.State.Status}}'

# View container logs
docker logs web

# Follow logs in real-time
docker logs -f web
```

### Best Practices:
1. **Use docker run** for new containers with specific configurations
2. **Use docker start** to restart existing containers
3. **Name your containers** for easier management
4. **Use restart policies** for production containers
5. **Monitor container states** regularly

## 8. How do you remove Docker containers and images?

### Answer:
Proper cleanup of Docker resources is essential for maintaining system performance and disk space.

### Container Removal Process:
```
Running Container ──docker stop──► Stopped Container ──docker rm──► Removed
       │                                    │                         ▲
       │                                    │                         │
       └────────────docker rm -f────────────┴─────────────────────────┘
                    (force remove)
```

### Container Removal Commands:

#### **Remove Individual Containers:**
```bash
# Remove stopped container
docker rm container_name
docker rm container_id

# Remove running container (force)
docker rm -f container_name

# Remove multiple containers
docker rm container1 container2 container3

# Remove with confirmation
docker rm -f $(docker ps -q --filter "name=web")
```

#### **Bulk Container Removal:**
```bash
# Remove all stopped containers
docker container prune

# Remove all containers (running and stopped)
docker rm -f $(docker ps -aq)

# Remove containers older than 24 hours
docker container prune --filter "until=24h"

# Remove containers with specific label
docker container prune --filter "label=environment=test"
```

### Image Removal Process:
```
Image ──has containers──► Cannot Remove (Error)
  │
  └──no containers──► docker rmi ──► Removed
                           │
                    ┌──────▼───────┐
                    │ Remove layers│
                    │ (if unused)  │
                    └──────────────┘
```

### Image Removal Commands:

#### **Remove Individual Images:**
```bash
# Remove by name
docker rmi nginx:latest

# Remove by ID
docker rmi abc123def456

# Force remove (even with containers)
docker rmi -f nginx:latest

# Remove multiple images
docker rmi nginx:latest ubuntu:20.04 node:16-alpine
```

#### **Bulk Image Removal:**
```bash
# Remove unused images (dangling)
docker image prune

# Remove all unused images
docker image prune -a

# Remove images older than 24 hours
docker image prune --filter "until=24h"

# Remove all images (dangerous!)
docker rmi -f $(docker images -q)
```

### Advanced Cleanup Strategies:

#### **System-wide Cleanup:**
```bash
# Remove everything unused
docker system prune

# Remove everything including volumes
docker system prune -a --volumes

# Show disk usage
docker system df

# Detailed disk usage
docker system df -v
```

#### **Selective Cleanup:**
```bash
# Remove containers by status
docker rm $(docker ps -q --filter "status=exited")

# Remove images by pattern
docker rmi $(docker images --filter "reference=myapp:*" -q)

# Remove containers by label
docker rm $(docker ps -aq --filter "label=environment=test")

# Remove images without tags (dangling)
docker rmi $(docker images -f "dangling=true" -q)
```

### Volume and Network Cleanup:

#### **Volume Cleanup:**
```bash
# Remove unused volumes
docker volume prune

# Remove specific volume
docker volume rm volume_name

# Remove all volumes (dangerous!)
docker volume rm $(docker volume ls -q)
```

#### **Network Cleanup:**
```bash
# Remove unused networks
docker network prune

# Remove specific network
docker network rm network_name

# Remove custom networks only
docker network rm $(docker network ls --filter "type=custom" -q)
```

### Cleanup Automation:

#### **Cleanup Script:**
```bash
#!/bin/bash
# cleanup-docker.sh

echo "Starting Docker cleanup..."

# Remove stopped containers
echo "Removing stopped containers..."
docker container prune -f

# Remove unused images
echo "Removing unused images..."
docker image prune -a -f

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove unused networks
echo "Removing unused networks..."
docker network prune -f

echo "Cleanup completed!"
docker system df
```

#### **Cron Job for Regular Cleanup:**
```bash
# Add to crontab (crontab -e)
# Run cleanup every Sunday at 2 AM
0 2 * * 0 /path/to/cleanup-docker.sh
```

### Safety Considerations:

#### **Before Removing:**
```bash
# Check what will be removed
docker container prune --dry-run
docker image prune -a --dry-run
docker system prune --dry-run

# Backup important data
docker run --rm -v mydata:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# List containers using image
docker ps -a --filter "ancestor=nginx:latest"
```

### Troubleshooting Removal Issues:

#### **Common Errors:**
```bash
# Error: container is running
docker stop container_name
docker rm container_name

# Error: image is being used
docker ps -a --filter "ancestor=image_name"
docker rm -f $(docker ps -aq --filter "ancestor=image_name")
docker rmi image_name

# Error: image has dependent child images
docker rmi -f image_name

# Error: volume is in use
docker ps -a --filter "volume=volume_name"
docker rm -f $(docker ps -aq --filter "volume=volume_name")
docker volume rm volume_name
```

### Best Practices:
1. **Regular cleanup** to prevent disk space issues
2. **Use labels** for easier selective cleanup
3. **Backup important data** before cleanup
4. **Test with --dry-run** first
5. **Automate cleanup** with scripts and cron jobs
6. **Monitor disk usage** with `docker system df`

## 9. What is Docker Hub and how do you use it?

### Answer:
Docker Hub is the world's largest public registry for Docker images, serving as the default registry for Docker Engine.

### Docker Hub Architecture:
```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Hub                               │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Official       │   Community     │    Private              │
│  Images         │   Images        │    Repositories         │
│                 │                 │                         │
│ • nginx         │ • user/myapp    │ • company/internal      │
│ • ubuntu        │ • org/project   │ • team/private-app      │
│ • postgres      │ • dev/custom    │ • user/secret-project   │
└─────────────────┴─────────────────┴─────────────────────────┘
                            │
                            ▼
                 ┌─────────────────┐
                 │  Local Docker   │
                 │     Engine      │
                 └─────────────────┘
```

### Docker Hub Features:

#### **1. Public Repositories**
- **Official Images**: Maintained by Docker and vendors
- **Community Images**: Created by developers worldwide
- **Free**: Unlimited public repositories
- **Automated Builds**: Build from source code

#### **2. Private Repositories**
- **Security**: Private access control
- **Teams**: Collaborate with team members
- **Paid Plans**: Limited free private repos
- **Enterprise**: Advanced features

#### **3. Additional Features**
- **Webhooks**: Trigger actions on push/pull
- **Build Triggers**: Automatic builds
- **Vulnerability Scanning**: Security analysis
- **Access Tokens**: API authentication

### Basic Docker Hub Operations:

#### **Pulling Images:**
```bash
# Pull latest version
docker pull nginx
docker pull nginx:latest

# Pull specific version
docker pull nginx:1.21-alpine

# Pull from specific user/organization
docker pull username/myapp:v1.0

# Pull with full registry URL
docker pull docker.io/library/nginx:latest
```

#### **Searching Images:**
```bash
# Search for images
docker search nginx
docker search --limit 10 python

# Search with filters
docker search --filter stars=100 nginx
docker search --filter is-official=true ubuntu
```

#### **Image Information:**
```bash
# View image details
docker inspect nginx:latest

# View image history
docker history nginx:latest

# List local images
docker images
docker images nginx
```

### Publishing to Docker Hub:

#### **Account Setup:**
```bash
# Login to Docker Hub
docker login
# Enter username and password

# Login with token
echo $DOCKER_TOKEN | docker login --username myuser --password-stdin

# Logout
docker logout
```

#### **Pushing Images:**
```bash
# Build your image
docker build -t myapp .

# Tag for Docker Hub
docker tag myapp:latest username/myapp:latest
docker tag myapp:latest username/myapp:v1.0

# Push to Docker Hub
docker push username/myapp:latest
docker push username/myapp:v1.0

# Push all tags
docker push username/myapp --all-tags
```

### Repository Management:

#### **Repository Naming:**
```
Naming Convention:
[registry]/[namespace]/[repository]:[tag]

Examples:
• docker.io/library/nginx:latest     (Official)
• docker.io/username/myapp:v1.0      (User)
• docker.io/company/product:latest   (Organization)
• registry.company.com/team/app:dev  (Private Registry)
```

#### **Tagging Strategy:**
```bash
# Semantic versioning
docker tag myapp:latest username/myapp:1.0.0
docker tag myapp:latest username/myapp:1.0
docker tag myapp:latest username/myapp:1
docker tag myapp:latest username/myapp:latest

# Environment tags
docker tag myapp:latest username/myapp:dev
docker tag myapp:latest username/myapp:staging
docker tag myapp:latest username/myapp:prod

# Feature tags
docker tag myapp:latest username/myapp:feature-auth
docker tag myapp:latest username/myapp:hotfix-security
```

### Automated Builds:

#### **GitHub Integration:**
```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v3
      with:
        context: .
        push: true
        tags: |
          username/myapp:latest
          username/myapp:${{ github.sha }}
```

### Security Best Practices:

#### **Access Tokens:**
```bash
# Create access token in Docker Hub settings
# Use token instead of password
echo $DOCKER_TOKEN | docker login --username myuser --password-stdin

# Store token securely
export DOCKER_TOKEN="dckr_pat_..."
```

#### **Image Scanning:**
```bash
# Scan image for vulnerabilities
docker scan username/myapp:latest

# Scan with specific severity
docker scan --severity high username/myapp:latest

# Enable scanning in Docker Hub
# Go to repository settings → Security
```

### Alternative Registries:

#### **Other Public Registries:**
```bash
# Google Container Registry
docker pull gcr.io/project/image:tag

# Amazon ECR Public
docker pull public.ecr.aws/registry/image:tag

# GitHub Container Registry
docker pull ghcr.io/username/image:tag

# Quay.io
docker pull quay.io/username/image:tag
```

#### **Private Registry Setup:**
```bash
# Run private registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for private registry
docker tag myapp:latest localhost:5000/myapp:latest

# Push to private registry
docker push localhost:5000/myapp:latest

# Pull from private registry
docker pull localhost:5000/myapp:latest
```

### Docker Hub API:

#### **API Usage:**
```bash
# Get repository information
curl -s https://hub.docker.com/v2/repositories/library/nginx/

# List tags
curl -s https://hub.docker.com/v2/repositories/library/nginx/tags/

# Get specific tag info
curl -s https://hub.docker.com/v2/repositories/library/nginx/tags/latest/
```

### Troubleshooting:

#### **Common Issues:**
```bash
# Authentication failed
docker login
# Check username/password

# Push denied
# Check repository name and permissions
docker tag myapp username/myapp:latest

# Rate limiting
# Docker Hub has pull rate limits
# Use authentication to increase limits

# Network issues
# Check firewall and proxy settings
docker pull --debug nginx
```

### Best Practices:
1. **Use official images** when possible
2. **Pin specific versions** in production
3. **Scan images** for vulnerabilities
4. **Use access tokens** instead of passwords
5. **Implement proper tagging** strategy
6. **Keep images small** and secure
7. **Document your images** with README
8. **Use multi-stage builds** to reduce size

## 10. Explain Docker networking modes.

### Answer:
Docker provides multiple networking modes to handle different use cases, from simple single-host setups to complex multi-host deployments.

### Docker Networking Architecture:
```
┌─────────────────────────────────────────────────────────────┐
│                    Host System                              │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Container A │  │ Container B │  │ Container C │        │
│  │   Bridge    │  │    Host     │  │    None     │        │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘        │
│         │                │                                  │
│  ┌──────▼──────┐        │         ┌─────────────┐        │
│  │   docker0   │        │         │  No Network │        │
│  │   Bridge    │        │         │  Interface  │        │
│  └──────┬──────┘        │         └─────────────┘        │
│         │                │                                  │
│  ┌──────▼────────────────▼─────────────────────────────┐  │
│  │              Host Network Interface                 │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Network Modes Detailed:

#### **1. Bridge Network (Default)**
```
Bridge Network Topology:

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Container A │    │ Container B │    │ Container C │
│ 172.17.0.2  │    │ 172.17.0.3  │    │ 172.17.0.4  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                   ┌──────▼──────┐
                   │   docker0   │
                   │ 172.17.0.1  │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │ Host Network│
                   │ 192.168.1.x │
                   └─────────────┘
```

**Characteristics:**
- **Isolation**: Containers isolated from host
- **Communication**: Containers can communicate with each other
- **Port Mapping**: Required for external access
- **DNS**: Automatic container name resolution

```bash
# Default bridge network
docker run -d --name web nginx

# Custom bridge network (recommended)
docker network create mynetwork
docker run -d --name web --network mynetwork nginx
docker run -d --name db --network mynetwork postgres

# Containers can communicate by name
docker exec web ping db
```

#### **2. Host Network**
```
Host Network Topology:

┌─────────────────────────────────────────┐
│              Host System                │
│                                         │
│  ┌─────────────┐                        │
│  │ Container   │                        │
│  │ (no network │                        │
│  │ namespace)  │                        │
│  └─────────────┘                        │
│         │                               │
│         │ (shares host network)         │
│         │                               │
│  ┌──────▼──────────────────────────┐    │
│  │        Host Network             │    │
│  │        192.168.1.x              │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Characteristics:**
- **No Isolation**: Container uses host's network directly
- **Performance**: Best network performance
- **Port Conflicts**: Cannot run multiple containers on same port
- **Security**: Less secure due to direct host access

```bash
# Host network mode
docker run -d --network host nginx
# nginx accessible directly on host's port 80

# No port mapping needed
curl localhost:80
```

#### **3. None Network**
```
None Network Topology:

┌─────────────────────────────────────────┐
│              Host System                │
│                                         │
│  ┌─────────────┐                        │
│  │ Container   │                        │
│  │             │                        │
│  │ No Network  │                        │
│  │ Interface   │                        │
│  └─────────────┘                        │
│                                         │
│  (Container completely isolated)        │
│                                         │
└─────────────────────────────────────────┘
```

**Characteristics:**
- **Complete Isolation**: No network access
- **Security**: Maximum network security
- **Custom Networking**: Manual network configuration required
- **Use Cases**: Batch processing, security-sensitive applications

```bash
# None network mode
docker run -d --network none alpine sleep 3600

# Container has no network interface
docker exec container_name ip addr show
# Only loopback interface
```

#### **4. Overlay Network (Swarm)**
```
Overlay Network Topology:

┌─────────────────┐         ┌─────────────────┐
│    Host A       │         │    Host B       │
│                 │         │                 │
│ ┌─────────────┐ │         │ ┌─────────────┐ │
│ │ Container 1 │ │         │ │ Container 2 │ │
│ └──────┬──────┘ │         │ └──────┬──────┘ │
│        │        │         │        │        │
│ ┌──────▼──────┐ │         │ ┌──────▼──────┐ │
│ │   Overlay   │ │◄────────┤ │   Overlay   │ │
│ │   Network   │ │  VXLAN  │ │   Network   │ │
│ └─────────────┘ │         │ └─────────────┘ │
└─────────────────┘         └─────────────────┘
```

**Characteristics:**
- **Multi-Host**: Spans multiple Docker hosts
- **Encryption**: Built-in encryption support
- **Service Discovery**: Automatic service discovery
- **Load Balancing**: Built-in load balancing

```bash
# Initialize swarm
docker swarm init

# Create overlay network
docker network create --driver overlay myoverlay

# Deploy service on overlay network
docker service create --network myoverlay --replicas 3 nginx
```

#### **5. Macvlan Network**
```
Macvlan Network Topology:

┌─────────────────────────────────────────┐
│              Host System                │
│                                         │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ Container A │  │ Container B │       │
│  │ MAC: aa:bb  │  │ MAC: cc:dd  │       │
│  │192.168.1.10 │  │192.168.1.11 │       │
│  └──────┬──────┘  └──────┬──────┘       │
│         │                │              │
│         └────────┬───────┘              │
│                  │                      │
│           ┌──────▼──────┐               │
│           │ Physical NIC│               │
│           │192.168.1.x  │               │
│           └─────────────┘               │
└─────────────────────────────────────────┘
```

**Characteristics:**
- **Direct Access**: Containers get direct network access
- **MAC Addresses**: Each container gets unique MAC address
- **Legacy Support**: Good for legacy applications
- **VLAN Support**: Supports VLAN tagging

```bash
# Create macvlan network
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macvlan-net

# Run container with macvlan
docker run -d --network macvlan-net --ip=192.168.1.100 nginx
```

### Network Management Commands:

#### **Network Operations:**
```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Create custom network
docker network create --driver bridge mynetwork

# Remove network
docker network rm mynetwork

# Connect container to network
docker network connect mynetwork container_name

# Disconnect container from network
docker network disconnect mynetwork container_name
```

#### **Network Troubleshooting:**
```bash
# Check container network settings
docker inspect container_name | grep -A 20 "NetworkSettings"

# Test connectivity between containers
docker exec container1 ping container2

# Check network interfaces in container
docker exec container_name ip addr show

# Check routing table
docker exec container_name ip route show

# Check DNS resolution
docker exec container_name nslookup container2
```

### Network Security:

#### **Network Isolation:**
```bash
# Create isolated networks
docker network create --internal secure-network

# Containers on internal network cannot reach internet
docker run -d --network secure-network nginx
```

#### **Firewall Integration:**
```bash
# Docker modifies iptables rules
sudo iptables -L DOCKER

# Custom firewall rules
sudo iptables -I DOCKER-USER -s 172.17.0.0/16 -j DROP
```

### Best Practices:
1. **Use custom bridge networks** instead of default bridge
2. **Implement network segmentation** for security
3. **Use overlay networks** for multi-host deployments
4. **Monitor network performance** and troubleshoot issues
5. **Secure networks** with proper firewall rules
6. **Use DNS names** instead of IP addresses
7. **Plan IP address ranges** to avoid conflicts
8. **Document network architecture** for complex setups

## Follow-up Questions:
- How would you optimize a Dockerfile for production?
- What are the security implications of different Docker networking modes?
- How do you handle secrets in Docker containers?
- What is the difference between docker-compose and docker stack?
