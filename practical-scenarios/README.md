# Practical Docker Scenarios

## 1. Scenario: Container Won't Start - Debugging Steps

### Problem:
A container fails to start with exit code 1. How do you debug this issue?

### Debugging Steps:

### 1. Check Container Logs
```bash
# View container logs
docker logs container_name

# Follow logs in real-time
docker logs -f container_name

# View logs with timestamps
docker logs -t container_name
```

### 2. Inspect Container Configuration
```bash
# Inspect container details
docker inspect container_name

# Check container status
docker ps -a

# View container events
docker events --filter container=container_name
```

### 3. Test Container Manually
```bash
# Run container interactively
docker run -it image_name /bin/bash

# Run with different entrypoint
docker run --entrypoint /bin/bash image_name

# Check if image exists
docker images | grep image_name
```

### 4. Check Resource Constraints
```bash
# Check available resources
docker system df
docker system info

# Check if ports are available
netstat -tlnp | grep :80
```

### 5. Validate Dockerfile
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

### 1. Monitor Container Resources
```bash
# View container stats
docker stats container_name

# Monitor specific container
docker stats --no-stream container_name

# Check container memory usage
docker exec container_name cat /proc/meminfo
```

### 2. Identify Memory Leaks
```bash
# Check process memory usage
docker exec container_name ps aux --sort=-%mem

# Monitor memory over time
watch -n 1 'docker stats --no-stream container_name'

# Check for memory leaks in application
docker exec container_name cat /proc/self/status | grep VmRSS
```

### 3. Set Memory Limits
```bash
# Set memory limit
docker run --memory=512m nginx

# Set memory limit with swap
docker run --memory=512m --memory-swap=1g nginx

# Set OOM kill policy
docker run --oom-kill-disable nginx
```

### 4. Optimize Application
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

### 1. Check Network Configuration
```bash
# List networks
docker network ls

# Inspect network
docker network inspect network_name

# Check container network
docker inspect container_name | grep -A 20 "NetworkSettings"
```

### 2. Test Network Connectivity
```bash
# Test DNS resolution
docker exec container_name nslookup google.com

# Test connectivity
docker exec container_name ping -c 3 8.8.8.8

# Check port connectivity
docker exec container_name telnet hostname port
```

### 3. Verify Port Mapping
```bash
# Check port mappings
docker port container_name

# Test port accessibility
curl -I http://localhost:8080

# Check if port is listening
docker exec container_name netstat -tlnp
```

### 4. Network Debugging
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

### 1. Base Image Issues
```dockerfile
# Problem: Base image not found
FROM nonexistent:latest

# Solution: Use valid base image
FROM ubuntu:20.04
```

### 2. Package Installation Failures
```dockerfile
# Problem: Package not found
RUN apt-get install -y nonexistent-package

# Solution: Update package list first
RUN apt-get update && apt-get install -y package-name
```

### 3. Permission Issues
```dockerfile
# Problem: Permission denied
COPY . /app
RUN chmod +x /app/script.sh

# Solution: Set proper permissions
COPY --chown=app:app . /app
RUN chmod +x /app/script.sh
```

### 4. Build Context Issues
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

### 1. Resource Monitoring
```bash
# Monitor CPU usage
docker stats --no-stream container_name

# Check CPU limits
docker inspect container_name | grep -i cpu

# Monitor I/O
docker exec container_name iostat -x 1
```

### 2. Application Profiling
```bash
# Profile CPU usage
docker exec container_name top -p 1

# Check memory usage
docker exec container_name free -h

# Monitor disk I/O
docker exec container_name iotop
```

### 3. Optimize Container Configuration
```bash
# Set CPU limits
docker run --cpus="1.5" nginx

# Set I/O limits
docker run --device-read-bps /dev/sda:1mb nginx

# Use tmpfs for temporary files
docker run --tmpfs /tmp:noexec,nosuid,size=100m nginx
```

## 6. Scenario: Docker Registry Authentication Issues

### Problem:
Cannot push/pull images from private registry.

### Authentication Solutions:

### 1. Login to Registry
```bash
# Login to Docker Hub
docker login

# Login to private registry
docker login registry.example.com

# Login with specific credentials
docker login -u username -p password registry.example.com
```

### 2. Configure Registry
```bash
# Add insecure registry
dockerd --insecure-registry registry.example.com:5000

# Configure registry in daemon.json
{
  "insecure-registries": ["registry.example.com:5000"]
}
```

### 3. Handle Authentication
```bash
# Use authentication token
docker login -u token -p $TOKEN registry.example.com

# Use service account
docker login -u _json_key -p "$(cat key.json)" registry.example.com
```

## 7. Scenario: Container Data Persistence Issues

### Problem:
Container data is lost after container restart.

### Data Persistence Solutions:

### 1. Use Named Volumes
```bash
# Create named volume
docker volume create mydata

# Use named volume
docker run -v mydata:/app/data nginx

# Inspect volume
docker volume inspect mydata
```

### 2. Use Bind Mounts
```bash
# Mount host directory
docker run -v /host/data:/app/data nginx

# Mount with read-only
docker run -v /host/data:/app/data:ro nginx
```

### 3. Backup and Restore
```bash
# Backup volume
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu tar xzf /backup/backup.tar.gz -C /
```

## 8. Scenario: Multi-Container Application Deployment

### Problem:
Need to deploy a complex multi-container application.

### Deployment Strategy:

### 1. Use Docker Compose
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
    image: node:16
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

### 2. Health Checks
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
```

### 3. Service Dependencies
```yaml
version: '3.8'
services:
  web:
    image: nginx
    depends_on:
      api:
        condition: service_healthy
      db:
        condition: service_started
```

## 9. Scenario: Container Security Hardening

### Problem:
Need to secure containers for production deployment.

### Security Hardening:

### 1. Run as Non-Root
```dockerfile
# Create non-root user
RUN adduser -D -s /bin/sh appuser
USER appuser
```

### 2. Use Read-Only Filesystem
```bash
# Run with read-only filesystem
docker run --read-only nginx

# Use tmpfs for writable directories
docker run --read-only --tmpfs /tmp nginx
```

### 3. Drop Capabilities
```bash
# Drop all capabilities
docker run --cap-drop ALL nginx

# Add specific capabilities
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx
```

### 4. Use Security Profiles
```bash
# Use AppArmor profile
docker run --security-opt apparmor=docker-default nginx

# Use seccomp profile
docker run --security-opt seccomp=profile.json nginx
```

## 10. Scenario: Container Monitoring and Logging

### Problem:
Need to monitor container health and collect logs.

### Monitoring Setup:

### 1. Container Health Checks
```dockerfile
# Add health check to Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

### 2. Log Management
```bash
# Configure log driver
docker run --log-driver=json-file --log-opt max-size=10m nginx

# Use syslog driver
docker run --log-driver=syslog nginx
```

### 3. Metrics Collection
```bash
# Export container metrics
docker run -p 8080:8080 prom/prometheus

# Use cAdvisor for container metrics
docker run -p 8080:8080 --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro gcr.io/cadvisor/cadvisor
```

## Follow-up Questions:
- How would you implement blue-green deployment with Docker?
- What are the best practices for container backup and disaster recovery?
- How do you handle container secrets in production?
- What is the difference between Docker and container orchestration platforms?
