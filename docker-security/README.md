# Docker Security

## 1. What are the main security concerns with Docker containers?

### Answer:
Docker security involves multiple layers of protection, from the container runtime to the host system. Understanding these security concerns is crucial for production deployments.

### Docker Security Model:
```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    Docker Security Layers                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                Application Layer                                                           │    │
│  │                                                                                                             │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │    │
│  │  │   Container A   │    │   Container B   │    │   Container C   │    │   Container D   │                │    │
│  │  │                 │    │                 │    │                 │    │                 │                │    │
│  │  │ • App Code      │    │ • App Code      │    │ • App Code      │    │ • App Code      │                │    │
│  │  │ • Dependencies  │    │ • Dependencies  │    │ • Dependencies  │    │ • Dependencies  │                │    │
│  │  │ • Config        │    │ • Config        │    │ • Config        │    │ • Config        │                │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘                │    │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘    │
│                                                    │                                                              │
│                                          Security Boundaries                                                      │
│                                                    │                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                              Container Runtime Layer                                                       │    │
│  │                                                                                                             │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │    │
│  │  │   Namespaces    │    │    cgroups      │    │  Capabilities   │    │    Seccomp     │                │    │
│  │  │                 │    │                 │    │                 │    │                 │                │    │
│  │  │ • PID           │    │ • CPU limits    │    │ • Drop privs    │    │ • Syscall       │                │    │
│  │  │ • Network       │    │ • Memory limits │    │ • Minimal caps  │    │   filtering     │                │    │
│  │  │ • Mount         │    │ • I/O limits    │    │ • No root       │    │ • Attack        │                │    │
│  │  │ • IPC           │    │ • Device access │    │   access        │    │   prevention    │                │    │
│  │  │ • UTS           │    │                 │    │                 │    │                 │                │    │
│  │  │ • User          │    │                 │    │                 │    │                 │                │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘                │    │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘    │
│                                                    │                                                              │
│                                                    │                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                Host System Layer                                                           │    │
│  │                                                                                                             │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │    │
│  │  │   AppArmor/     │    │   File System   │    │    Network      │    │   Audit &       │                │    │
│  │  │    SELinux      │    │    Security     │    │    Security     │    │   Monitoring    │                │    │
│  │  │                 │    │                 │    │                 │    │                 │                │    │
│  │  │ • MAC policies  │    │ • Read-only FS  │    │ • Firewall      │    │ • Log analysis  │                │    │
│  │  │ • Profile       │    │ • Mount         │    │ • Network       │    │ • Intrusion     │                │    │
│  │  │   enforcement   │    │   restrictions  │    │   segmentation  │    │   detection     │                │    │
│  │  │ • Access        │    │ • Tmpfs for     │    │ • TLS           │    │ • Compliance    │                │    │
│  │  │   control       │    │   secrets       │    │   encryption    │    │   monitoring    │                │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘                │    │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Primary Security Concerns:

#### **1. Container Escape Vulnerabilities**
```
Container Escape Attack Vectors:

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                Host System                                                  │
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                            Container                                                │    │
│  │                                                                                     │    │
│  │  ┌─────────────────┐                                                              │    │
│  │  │   Malicious     │  1. Kernel Exploits                                         │    │
│  │  │   Application   │  ────────────────────────────────────────────────────────► │    │
│  │  │                 │                                                              │    │
│  │  └─────────────────┘  2. Privileged Container                                    │    │
│  │           │            ────────────────────────────────────────────────────────► │    │
│  │           │                                                                       │    │
│  │           │            3. Capability Abuse                                       │    │
│  │           │            ────────────────────────────────────────────────────────► │    │
│  │           │                                                                       │    │
│  │           │            4. Volume Mount Abuse                                     │    │
│  │           └────────────────────────────────────────────────────────────────────► │    │
│  │                                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                                   │
│                                        │ Successful Escape                                 │
│                                        ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                        Host Access Gained                                          │    │
│  │                                                                                     │    │
│  │  • Full filesystem access                                                          │    │
│  │  • Network access to other containers                                              │    │
│  │  • Ability to modify host configuration                                            │    │
│  │  • Access to sensitive host data                                                   │    │
│  │  • Potential lateral movement                                                      │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

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

#### **2. Image Security Vulnerabilities**
```
Image Security Threat Model:

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              Image Supply Chain                                            │
│                                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   Base Image    │    │   Dependencies  │    │   Application   │    │   Final Image   │ │
│  │                 │    │                 │    │     Code        │    │                 │ │
│  │ • OS packages   │    │ • Libraries     │    │ • Source code   │    │ • Layered       │ │
│  │ • System libs   │    │ • Frameworks    │    │ • Binaries      │    │   filesystem    │ │
│  │ • CVEs          │    │ • Transitive    │    │ • Config files  │    │ • Metadata      │ │
│  │ • Backdoors     │    │   deps          │    │ • Secrets       │    │ • Signatures    │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│           │                       │                       │                       │        │
│           ▼                       ▼                       ▼                       ▼        │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                            Vulnerability Sources                                       │ │
│  │                                                                                         │ │
│  │  • Known CVEs in base OS                    • Malicious packages                      │ │
│  │  • Outdated system packages                 • Supply chain attacks                    │ │
│  │  • Vulnerable application dependencies      • Embedded secrets/credentials            │ │
│  │  • Misconfigurations                        • Unsigned or tampered images             │ │
│  │  • Excessive privileges                      • Trojan horse applications               │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

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

#### **3. Runtime Security Threats**
```
Runtime Attack Surface:

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                Container Runtime                                            │
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                              Attack Vectors                                        │    │
│  │                                                                                     │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐              │    │
│  │  │   Privileged    │    │   Resource      │    │   Network       │              │    │
│  │  │   Containers    │    │   Exhaustion    │    │   Attacks       │              │    │
│  │  │                 │    │                 │    │                 │              │    │
│  │  │ • --privileged  │    │ • CPU bombing   │    │ • Port scanning │              │    │
│  │  │ • Host PID      │    │ • Memory leaks  │    │ • ARP spoofing  │              │    │
│  │  │ • Host network  │    │ • Disk filling  │    │ • DNS poisoning │              │    │
│  │  │ • Volume mounts │    │ • Fork bombs    │    │ • MITM attacks  │              │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘              │    │
│  │                                                                                     │    │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐              │    │
│  │  │   Data          │    │   Lateral       │    │   Host          │              │    │
│  │  │   Exfiltration  │    │   Movement      │    │   Compromise    │              │    │
│  │  │                 │    │                 │    │                 │              │    │
│  │  │ • Volume access │    │ • Container     │    │ • Daemon        │              │    │
│  │  │ • Network       │    │   hopping       │    │   exploitation  │              │    │
│  │  │   sniffing      │    │ • Shared        │    │ • Kernel        │              │    │
│  │  │ • Log access    │    │   resources     │    │   vulnerabilities│              │    │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

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

#### **1. Defense in Depth Strategy:**
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

#### **2. Image Security Scanning:**
```bash
# Vulnerability scanning pipeline
docker build -t myapp:latest .
docker scan myapp:latest
trivy image myapp:latest
grype myapp:latest

# Fail build on high/critical vulnerabilities
docker scan --severity high myapp:latest || exit 1
```

#### **3. Runtime Monitoring:**
```bash
# Container behavior monitoring
docker exec container_name ps aux
docker exec container_name netstat -tlnp
docker exec container_name lsof -i

# Resource monitoring
docker stats --no-stream
docker system events --filter container=myapp
```

#### **4. Secrets Management:**
```bash
# Docker secrets (Swarm mode)
echo "mysecret" | docker secret create app_secret -
docker service create --secret app_secret myapp

# External secrets management
docker run -e VAULT_ADDR=https://vault.example.com myapp
```

### Security Compliance and Standards:

#### **CIS Docker Benchmark:**
```bash
# Run CIS Docker Benchmark
docker run --rm --net host --pid host --userns host \
  --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security
```

#### **Security Policies:**
```yaml
# Pod Security Policy example
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

## 2. How do you secure Docker images and what is image scanning?

### Answer:

### Image Security Measures:

### 1. Use Official Base Images
```dockerfile
# Good: Use official, minimal base images
FROM node:16-alpine

# Bad: Use large, potentially vulnerable images
FROM ubuntu:20.04
```

### 2. Keep Images Updated
```dockerfile
# Pin specific versions
FROM node:16.14.2-alpine

# Regularly update base images
FROM node:18-alpine
```

### 3. Minimize Attack Surface
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

### 1. Namespace Isolation
```bash
# View container namespaces
docker exec container_name ls -la /proc/self/ns/

# Run container with specific namespace
docker run --pid=host nginx  # Uses host PID namespace
```

### 2. cgroups Resource Limits
```bash
# Limit memory usage
docker run --memory=512m nginx

# Limit CPU usage
docker run --cpus=1.0 nginx

# Limit I/O operations
docker run --device-read-bps /dev/sda:1mb nginx
```

### 3. Capabilities
```bash
# Drop all capabilities
docker run --cap-drop ALL nginx

# Add specific capabilities
docker run --cap-add NET_BIND_SERVICE nginx

# List container capabilities
docker exec container_name capsh --print
```

### 4. Seccomp Profiles
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

### 1. Container Configuration
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

### 2. Network Security
```bash
# Use custom networks
docker network create --internal secure-network

# Limit port exposure
docker run -p 127.0.0.1:8080:80 nginx

# Use TLS for communication
docker run -p 443:443 -v /certs:/certs nginx
```

### 3. Image Security
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

### 4. Runtime Security
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

### 1. Pre-build Scanning
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

### 2. Base Image Scanning
```bash
# Scan base images regularly
docker scan node:16-alpine
docker scan nginx:alpine
docker scan postgres:13-alpine
```

### 3. Dependency Scanning
```bash
# Scan for vulnerable dependencies
npm audit
pip check
go list -json -m all | nancy sleuth
```

### 4. Runtime Security Monitoring
```bash
# Monitor container behavior
docker exec container_name ps aux
docker exec container_name netstat -tlnp
docker exec container_name lsof -i
```

## 7. Explain Docker's security features: AppArmor, SELinux, and seccomp.

### Answer:

### 1. AppArmor
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

### 2. SELinux
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

### 3. seccomp
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

### 1. TLS Configuration
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

### 2. API Access Control
```bash
# Restrict API access
dockerd -H unix:///var/run/docker.sock -H tcp://127.0.0.1:2376

# Use firewall rules
iptables -A INPUT -p tcp --dport 2376 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 2376 -j DROP
```

### 3. User Authentication
```bash
# Create Docker group
sudo groupadd docker
sudo usermod -aG docker $USER

# Restrict socket permissions
sudo chmod 660 /var/run/docker.sock
sudo chown root:docker /var/run/docker.sock
```

### 4. Daemon Configuration
```json
{
  "hosts": ["unix:///var/run/docker.sock"],
  "tls": true,
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem",
  "tlsverify": true,
  "tlscacert": "/etc/docker/ca.pem"
}
```

## 9. What are Docker security vulnerabilities and how do you mitigate them?

### Answer:

### Common Vulnerabilities:

### 1. Container Escape
- **Risk**: Breaking out of container isolation
- **Mitigation**: Use non-privileged containers, security profiles

```bash
# Mitigate container escape
docker run --user 1000:1000 nginx
docker run --security-opt seccomp=profile.json nginx
docker run --read-only nginx
```

### 2. Privilege Escalation
- **Risk**: Gaining root access
- **Mitigation**: Drop capabilities, use non-root users

```bash
# Prevent privilege escalation
docker run --cap-drop ALL nginx
docker run --user 1000:1000 nginx
```

### 3. Resource Exhaustion
- **Risk**: DoS attacks, resource starvation
- **Mitigation**: Set resource limits

```bash
# Limit resources
docker run --memory=512m --cpus=1.0 nginx
docker run --pids-limit=100 nginx
```

### 4. Network Attacks
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

### 1. Container Monitoring
```bash
# Monitor container processes
docker exec container_name ps aux

# Monitor network connections
docker exec container_name netstat -tlnp

# Monitor file system changes
docker exec container_name find / -type f -newer /tmp/timestamp
```

### 2. Audit Logging
```bash
# Enable audit logging
dockerd --log-driver=json-file --log-opt max-size=10m

# Monitor Docker daemon logs
journalctl -u docker.service -f

# Audit container events
docker events --filter container=container_name
```

### 3. Security Scanning
```bash
# Regular image scanning
docker scan nginx:latest

# Runtime security monitoring
docker exec container_name cat /proc/self/status

# Network security monitoring
docker exec container_name ss -tlnp
```

### 4. Compliance Monitoring
```bash
# Check container compliance
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/docker-bench-security

# CIS Docker Benchmark
docker run --rm --net host --pid host --userns host \
  --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /usr/bin/containerd:/usr/bin/containerd:ro \
  -v /usr/bin/runc:/usr/bin/runc:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security
```

## Follow-up Questions:
- How would you implement zero-trust security with Docker?
- What are the security implications of Docker in Kubernetes?
- How do you handle secrets rotation in Docker containers?
- What is the difference between Docker security and container security?
