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

### 1. Container Cannot Reach Internet
```bash
# Check DNS resolution
docker exec container_name nslookup google.com

# Check routing
docker exec container_name ip route

# Check network configuration
docker network inspect bridge
```

### 2. Containers Cannot Communicate
```bash
# Check if containers are on same network
docker network inspect network_name

# Test connectivity
docker exec container1 ping container2

# Check firewall rules
iptables -L DOCKER-USER
```

### 3. Port Not Accessible
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

## Follow-up Questions:
- How would you implement service mesh with Docker?
- What are the performance implications of different networking modes?
- How do you monitor Docker network traffic?
- What is the difference between Docker networking and Kubernetes networking?
