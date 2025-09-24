# Basic Docker Concepts

## 1. What is Docker and how does it differ from Virtual Machines?

### Answer:
Docker is a containerization platform that allows you to package applications and their dependencies into lightweight, portable containers. Unlike virtual machines, Docker containers share the host OS kernel and run as isolated processes.

### Key Differences:

| Aspect | Docker Containers | Virtual Machines |
|--------|------------------|------------------|
| **Resource Usage** | Lightweight, shares OS kernel | Heavy, requires full OS |
| **Startup Time** | Seconds | Minutes |
| **Isolation** | Process-level | Hardware-level |
| **Performance** | Near-native | Hypervisor overhead |
| **Size** | MBs | GBs |

### Code Example:
```bash
# Docker container
docker run -d nginx

# VM would require full OS installation
```

## 2. Explain Docker's architecture and its main components.

### Answer:
Docker follows a client-server architecture with these main components:

1. **Docker Client**: CLI tool for interacting with Docker
2. **Docker Daemon**: Background service managing containers
3. **Docker Registry**: Repository for Docker images
4. **Docker Images**: Read-only templates for containers
5. **Docker Containers**: Running instances of images

## 3. What is a Dockerfile and what are its key instructions?

### Answer:
A Dockerfile is a text file containing instructions to build a Docker image. Key instructions include:

- `FROM`: Base image
- `RUN`: Execute commands during build
- `COPY/ADD`: Copy files into image
- `WORKDIR`: Set working directory
- `EXPOSE`: Document port exposure
- `CMD/ENTRYPOINT`: Default command to run

### Example Dockerfile:
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## 4. What is the difference between CMD and ENTRYPOINT?

### Answer:

| CMD | ENTRYPOINT |
|-----|------------|
| Can be overridden | Cannot be overridden |
| Default command | Main command |
| `docker run` replaces it | `docker run` appends to it |

### Examples:
```dockerfile
# CMD - can be overridden
CMD ["echo", "Hello World"]
# docker run image echo "Goodbye" → "Goodbye"

# ENTRYPOINT - cannot be overridden
ENTRYPOINT ["echo", "Hello"]
# docker run image World → "Hello World"
```

## 5. Explain Docker layers and how they work.

### Answer:
Docker images are built in layers. Each instruction in a Dockerfile creates a new layer. Layers are cached and reused, making builds faster and more efficient.

### Benefits:
- **Caching**: Unchanged layers are reused
- **Efficiency**: Only changed layers are rebuilt
- **Sharing**: Common layers shared between images

### Example:
```dockerfile
FROM ubuntu:20.04          # Layer 1
RUN apt-get update         # Layer 2
RUN apt-get install -y git # Layer 3
COPY app.py /app/          # Layer 4
```

## 6. What are Docker volumes and why are they important?

### Answer:
Docker volumes are the preferred way to persist data in Docker containers. They provide:

- **Data Persistence**: Survive container deletion
- **Performance**: Better I/O performance than bind mounts
- **Portability**: Managed by Docker
- **Backup**: Easy to backup and restore

### Types of Volumes:
1. **Named Volumes**: Managed by Docker
2. **Anonymous Volumes**: Temporary, auto-generated names
3. **Bind Mounts**: Mount host directories

### Examples:
```bash
# Named volume
docker run -v mydata:/app/data nginx

# Bind mount
docker run -v /host/path:/container/path nginx

# Anonymous volume
docker run -v /app/data nginx
```

## 7. What is the difference between docker run and docker start?

### Answer:

| docker run | docker start |
|------------|--------------|
| Creates and starts new container | Starts existing stopped container |
| Uses image as template | Uses existing container |
| Can pass new parameters | Uses existing configuration |
| Always creates new container | Reuses existing container |

### Examples:
```bash
# Create and start new container
docker run -d --name web nginx

# Start existing stopped container
docker start web

# docker run with new container
docker run -d --name web2 nginx
```

## 8. How do you remove Docker containers and images?

### Answer:

### Remove Containers:
```bash
# Remove stopped container
docker rm container_name

# Remove running container (force)
docker rm -f container_name

# Remove all stopped containers
docker container prune

# Remove all containers
docker rm $(docker ps -aq)
```

### Remove Images:
```bash
# Remove specific image
docker rmi image_name

# Remove unused images
docker image prune

# Remove all images
docker rmi $(docker images -q)
```

## 9. What is Docker Hub and how do you use it?

### Answer:
Docker Hub is the default public registry for Docker images. It provides:

- **Public Images**: Official and community images
- **Private Repositories**: For organizations
- **Automated Builds**: Build from GitHub/Bitbucket
- **Webhooks**: Integration with CI/CD

### Usage:
```bash
# Pull image from Docker Hub
docker pull nginx

# Push image to Docker Hub
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest

# Search images
docker search nginx
```

## 10. Explain Docker networking modes.

### Answer:
Docker provides several networking modes:

1. **Bridge** (default): Isolated network for containers
2. **Host**: Use host's network directly
3. **None**: No networking
4. **Overlay**: Multi-host networking
5. **Macvlan**: Assign MAC address to container

### Examples:
```bash
# Bridge network (default)
docker run -d nginx

# Host network
docker run -d --network host nginx

# Custom bridge network
docker network create mynetwork
docker run -d --network mynetwork nginx

# None network
docker run -d --network none nginx
```

## Follow-up Questions:
- How would you optimize a Dockerfile for production?
- What are the security implications of different Docker networking modes?
- How do you handle secrets in Docker containers?
- What is the difference between docker-compose and docker stack?
