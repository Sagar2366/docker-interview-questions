# Docker Architecture

## 1. Explain Docker's client-server architecture in detail.

### Answer:
Docker uses a client-server architecture where:

- **Docker Client**: Command-line interface that sends commands to the Docker daemon
- **Docker Daemon**: Background service that manages Docker objects (containers, images, networks, volumes)
- **Docker Registry**: Repository for storing and distributing Docker images

### Architecture Components:

1. **Docker Client** (`docker` CLI)
   - Sends commands via REST API
   - Can connect to local or remote daemon
   - Handles user input and output

2. **Docker Daemon** (`dockerd`)
   - Manages Docker objects
   - Handles container lifecycle
   - Manages images, networks, volumes
   - Exposes REST API

3. **Docker Registry**
   - Stores Docker images
   - Docker Hub (public) or private registries
   - Handles image distribution

### Communication Flow:
```
Client → REST API → Daemon → Container Runtime → Containers
```

## 2. What is containerd and how does it relate to Docker?

### Answer:
containerd is a high-level container runtime that Docker uses internally. It provides:

- **Container Lifecycle Management**: Create, start, stop, delete containers
- **Image Management**: Pull, push, store images
- **Storage Management**: Manage container filesystems
- **Network Management**: Handle container networking

### Docker's Runtime Architecture:
```
Docker CLI → Docker Daemon → containerd → runc → Container
```

### Benefits of containerd:
- **Modularity**: Can be used independently
- **Standardization**: Industry standard container runtime
- **Performance**: Optimized for container operations
- **Compatibility**: Works with Kubernetes, Docker, etc.

## 3. Explain the role of runc in Docker's architecture.

### Answer:
runc is a low-level container runtime that implements the OCI (Open Container Initiative) specification. It:

- **Creates Containers**: Spawns and runs containers
- **Manages Namespaces**: Provides process isolation
- **Handles cgroups**: Manages resource limits
- **Implements OCI**: Follows container standards

### Container Runtime Stack:
```
Docker → containerd → containerd-shim → runc → Container Process
```

### Key Features:
- **OCI Compliance**: Standard container format
- **Lightweight**: Minimal overhead
- **Secure**: Implements security features
- **Portable**: Works across different platforms

## 4. What are Docker namespaces and how do they provide isolation?

### Answer:
Docker uses Linux namespaces to provide process isolation. Each namespace type isolates a specific aspect:

### Namespace Types:

1. **PID Namespace**: Isolates process IDs
2. **Network Namespace**: Isolates network interfaces
3. **Mount Namespace**: Isolates filesystem mounts
4. **IPC Namespace**: Isolates inter-process communication
5. **UTS Namespace**: Isolates hostname and domain name
6. **User Namespace**: Isolates user and group IDs

### Example:
```bash
# View namespaces of a container
docker exec container_name ls -la /proc/self/ns/

# Create container with specific namespace
docker run --pid=host nginx  # Uses host PID namespace
```

## 5. How does Docker use cgroups for resource management?

### Answer:
cgroups (control groups) limit and monitor resource usage of containers:

### Resource Types:
- **CPU**: CPU usage limits
- **Memory**: Memory usage limits
- **I/O**: Disk I/O limits
- **Network**: Network bandwidth limits

### Examples:
```bash
# Limit CPU usage
docker run --cpus="1.5" nginx

# Limit memory
docker run --memory="512m" nginx

# Limit both
docker run --cpus="1.5" --memory="512m" nginx
```

### cgroup Hierarchy:
```
/sys/fs/cgroup/
├── cpu/
├── memory/
├── blkio/
└── net_cls/
```

## 6. Explain Docker's storage driver architecture.

### Answer:
Docker uses storage drivers to manage how images and containers are stored on the host filesystem.

### Common Storage Drivers:

1. **overlay2** (Recommended)
   - Uses overlay filesystem
   - Good performance
   - Efficient storage usage

2. **aufs**
   - Union filesystem
   - Good compatibility
   - Slower than overlay2

3. **devicemapper**
   - Block-level storage
   - Good for production
   - More complex setup

4. **btrfs**
   - Copy-on-write filesystem
   - Good performance
   - Requires btrfs filesystem

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

# View container layer
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

### Network Components:
```
Host Network
├── docker0 (Bridge)
│   ├── Container A (172.17.0.2)
│   └── Container B (172.17.0.3)
└── Custom Bridge
    ├── Container C (172.18.0.2)
    └── Container D (172.18.0.3)
```

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

## Follow-up Questions:
- How would you troubleshoot Docker daemon issues?
- What are the security implications of Docker's architecture?
- How do you monitor Docker daemon performance?
- What is the difference between Docker and Podman?
