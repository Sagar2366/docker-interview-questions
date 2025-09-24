# Docker Architecture

## 1. Explain Docker's client-server architecture in detail.

### Answer:
Docker uses a client-server architecture that separates the user interface from the container management engine, enabling flexible deployment and remote management.

### Complete Docker Architecture:
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           Docker Architecture                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐     REST API/gRPC     ┌─────────────────────────────────────┐  │
│  │  Docker Client  │◄────────────────────►│         Docker Daemon              │  │
│  │                 │                       │         (dockerd)                   │  │
│  │ • docker build  │                       │                                     │  │
│  │ • docker run    │                       │ ┌─────────────────────────────────┐ │  │
│  │ • docker pull   │                       │ │        API Server              │ │  │
│  │ • docker push   │                       │ │  • REST API endpoints          │ │  │
│  │ • docker ps     │                       │ │  • Authentication              │ │  │
│  └─────────────────┘                       │ │  • Request routing             │ │  │
│                                             │ └─────────────────────────────────┘ │  │
│  ┌─────────────────┐                       │                                     │  │
│  │ Docker Compose  │                       │ ┌─────────────────────────────────┐ │  │
│  │                 │                       │ │     Object Management           │ │  │
│  │ • Multi-service │                       │ │  • Images                      │ │  │
│  │ • Orchestration │                       │ │  • Containers                  │ │  │
│  └─────────────────┘                       │ │  • Networks                    │ │  │
│                                             │ │  • Volumes                     │ │  │
│  ┌─────────────────┐                       │ └─────────────────────────────────┘ │  │
│  │   Third-party   │                       │                                     │  │
│  │     Tools       │                       │ ┌─────────────────────────────────┐ │  │
│  │                 │                       │ │      Runtime Interface          │ │  │
│  │ • Portainer     │                       │ │                                 │ │  │
│  │ • Kubernetes    │                       │ │        containerd               │ │  │
│  │ • CI/CD Tools   │                       │ │                                 │ │  │
│  └─────────────────┘                       │ └─────────────┬───────────────────┘ │  │
│                                             └───────────────┼─────────────────────┘  │
│                                                             │                        │
│  ┌─────────────────────────────────────────────────────────┼─────────────────────┐  │
│  │                    Container Runtime Layer               │                     │  │
│  │                                                          ▼                     │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           │  │
│  │  │  containerd-    │    │  containerd-    │    │  containerd-    │           │  │
│  │  │     shim        │    │     shim        │    │     shim        │           │  │
│  │  └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘           │  │
│  │            │                      │                      │                   │  │
│  │            ▼                      ▼                      ▼                   │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           │  │
│  │  │      runc       │    │      runc       │    │      runc       │           │  │
│  │  └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘           │  │
│  │            │                      │                      │                   │  │
│  │            ▼                      ▼                      ▼                   │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           │  │
│  │  │   Container 1   │    │   Container 2   │    │   Container 3   │           │  │
│  │  │                 │    │                 │    │                 │           │  │
│  │  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │           │  │
│  │  │ │ Application │ │    │ │ Application │ │    │ │ Application │ │           │  │
│  │  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │           │  │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘           │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────┘

                                        ▲
                                        │
                                        │ Pull/Push Images
                                        │
                                        ▼
                              ┌─────────────────┐
                              │ Docker Registry │
                              │                 │
                              │ • Docker Hub    │
                              │ • Private Reg   │
                              │ • ECR/GCR/ACR   │
                              │ • Harbor        │
                              └─────────────────┘
```

### Architecture Components Deep Dive:

#### **1. Docker Client** (`docker` CLI)
- **Purpose**: User interface to Docker ecosystem
- **Communication**: REST API over Unix socket or TCP
- **Features**:
  - Command-line interface
  - Remote daemon connection
  - Plugin system support
  - Context switching

```bash
# Client configuration examples
docker version                    # Shows client and server versions
docker context ls                 # List available contexts
docker context use remote-host    # Switch to remote Docker host
docker -H tcp://remote:2376 ps    # Connect to remote daemon
```

#### **2. Docker Daemon** (`dockerd`)
- **Purpose**: Core Docker service and API server
- **Responsibilities**:
  - API request handling
  - Image management
  - Container lifecycle
  - Network management
  - Volume management
  - Plugin management

```bash
# Daemon management
sudo systemctl status docker      # Check daemon status
sudo systemctl start docker       # Start daemon
sudo systemctl enable docker      # Enable auto-start
journalctl -u docker.service -f   # Follow daemon logs
```

#### **3. containerd**
- **Purpose**: High-level container runtime
- **Functions**:
  - Container lifecycle management
  - Image management and storage
  - Runtime abstraction
  - Plugin architecture

#### **4. runc**
- **Purpose**: Low-level OCI runtime
- **Functions**:
  - Container creation and execution
  - Namespace and cgroup management
  - Security enforcement
  - OCI specification compliance

### Communication Flow Detailed:
```
User Command
     │
     ▼
┌─────────────────┐
│  Docker Client  │
└─────────┬───────┘
          │ HTTP/REST API
          ▼
┌─────────────────┐
│ Docker Daemon   │
│   (dockerd)     │
└─────────┬───────┘
          │ gRPC
          ▼
┌─────────────────┐
│   containerd    │
└─────────┬───────┘
          │ OCI Runtime API
          ▼
┌─────────────────┐
│      runc       │
└─────────┬───────┘
          │ System Calls
          ▼
┌─────────────────┐
│ Linux Kernel    │
│ • Namespaces    │
│ • cgroups       │
│ • Capabilities  │
└─────────────────┘
```

## 2. What is containerd and how does it relate to Docker?

### Answer:
containerd is a high-level container runtime that serves as the core container runtime for Docker. It was extracted from Docker to create a more modular and standardized container ecosystem.

### containerd Architecture:
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              containerd                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │   Docker CLI    │    │   Kubernetes    │    │   Other Tools   │                │
│  │                 │    │     (CRI)       │    │                 │                │
│  └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘                │
│            │                      │                      │                        │
│            └──────────────────────┼──────────────────────┘                        │
│                                   │                                               │
│                                   ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                        containerd API                                      │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │     Images      │    │   Containers    │    │    Snapshots    │                │
│  │                 │    │                 │    │                 │                │
│  │ • Pull/Push     │    │ • Create        │    │ • Layer Mgmt    │                │
│  │ • Store         │    │ • Start/Stop    │    │ • CoW Support   │                │
│  │ • Metadata      │    │ • Monitor       │    │ • Diff Service  │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                │
│  │    Runtime      │    │     Events      │    │    Plugins      │                │
│  │                 │    │                 │    │                 │                │
│  │ • OCI Runtime   │    │ • Pub/Sub       │    │ • Extensible    │                │
│  │ • Shim Mgmt     │    │ • Streaming     │    │ • Custom Logic  │                │
│  │ • Task API      │    │ • Monitoring    │    │ • Third-party   │                │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │ containerd-shim │
                         │                 │
                         │ • Process Mgmt  │
                         │ • I/O Handling  │
                         │ • Exit Status   │
                         └─────────┬───────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │      runc       │
                         │                 │
                         │ • OCI Runtime   │
                         │ • Container     │
                         │   Creation      │
                         └─────────┬───────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │   Container     │
                         │   Process       │
                         └─────────────────┘
```

### Docker's Runtime Evolution:
```
Docker 1.11+ Runtime Stack:

┌─────────────────┐
│  Docker Client  │
└─────────┬───────┘
          │ REST API
          ▼
┌─────────────────┐
│ Docker Daemon   │ ◄─── Manages high-level operations
│   (dockerd)     │      (networking, volumes, etc.)
└─────────┬───────┘
          │ gRPC
          ▼
┌─────────────────┐
│   containerd    │ ◄─── Container lifecycle management
│                 │      Image management
└─────────┬───────┘      Storage management
          │ Runtime API
          ▼
┌─────────────────┐
│containerd-shim  │ ◄─── Process supervision
│                 │      I/O handling
└─────────┬───────┘      Daemonless containers
          │ exec
          ▼
┌─────────────────┐
│      runc       │ ◄─── OCI runtime implementation
│                 │      Namespace/cgroup setup
└─────────┬───────┘      Security enforcement
          │ clone/exec
          ▼
┌─────────────────┐
│   Container     │ ◄─── Actual application process
│   Process       │
└─────────────────┘
```

### containerd Features:

#### **1. Container Lifecycle Management**
```bash
# Direct containerd usage (ctr command)
ctr images pull docker.io/library/nginx:latest
ctr containers create docker.io/library/nginx:latest nginx-container
ctr tasks start nginx-container
ctr tasks list
ctr tasks kill nginx-container
ctr containers delete nginx-container
```

#### **2. Image Management**
```bash
# Image operations with containerd
ctr images list
ctr images pull docker.io/library/alpine:latest
ctr images push myregistry.com/myimage:latest
ctr images remove docker.io/library/alpine:latest
```

#### **3. Snapshot Management**
```bash
# Snapshot operations
ctr snapshots list
ctr snapshots usage
ctr snapshots remove snapshot-name
```

### Benefits of containerd:

#### **1. Modularity and Independence**
- Can be used without Docker daemon
- Kubernetes uses containerd directly (CRI)
- Smaller attack surface
- Independent versioning and updates

#### **2. Industry Standardization**
- CNCF graduated project
- OCI compliant
- Vendor neutral
- Wide ecosystem support

#### **3. Performance Optimization**
- Optimized for container operations
- Reduced overhead
- Better resource utilization
- Faster container startup

#### **4. Ecosystem Compatibility**
```
containerd Ecosystem:

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Docker      │    │   Kubernetes    │    │     Podman      │
│                 │    │                 │    │                 │
│ Uses containerd │    │ Uses containerd │    │ Alternative to  │
│ for runtime     │    │ via CRI         │    │ Docker/contain. │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────┐
                    │   containerd    │
                    │                 │
                    │ • Runtime       │
                    │ • Image Mgmt    │
                    │ • Storage       │
                    └─────────────────┘
```

### containerd vs Docker Daemon:

| Aspect | containerd | Docker Daemon |
|--------|------------|---------------|
| **Scope** | Container runtime | Full container platform |
| **Features** | Core runtime only | Networking, volumes, compose |
| **API** | gRPC | REST API |
| **Size** | Smaller | Larger |
| **Use Case** | Kubernetes, minimal setups | Development, full features |
| **Networking** | Basic | Advanced (bridge, overlay) |
| **Storage** | Snapshots | Volumes, bind mounts |

### Practical Examples:

#### **Using containerd directly:**
```bash
# Install containerd tools
sudo apt install containerd.io

# Configure containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Start containerd service
sudo systemctl start containerd
sudo systemctl enable containerd

# Use ctr (containerd CLI)
ctr version
ctr images pull docker.io/library/hello-world:latest
ctr run --rm docker.io/library/hello-world:latest hello
```

#### **Kubernetes with containerd:**
```yaml
# Kubernetes node configuration
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
containerRuntime: remote
containerRuntimeEndpoint: unix:///run/containerd/containerd.sock
```

### Migration and Compatibility:

#### **Docker to containerd migration:**
```bash
# Check current runtime
docker info | grep -i runtime

# Images are compatible
docker images
ctr images list

# Containers need to be recreated
docker export container_name | ctr images import - myimage:latest
```

## 3. Explain the role of runc in Docker's architecture.

### Answer:
runc is the low-level container runtime that actually creates and runs containers. It's the component that interfaces directly with the Linux kernel to set up the container environment.

### runc in the Container Stack:
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        Container Runtime Hierarchy                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐                                                               │
│  │  Docker Client  │ ◄─── User Interface                                          │
│  └─────────┬───────┘                                                               │
│            │ REST API                                                              │
│            ▼                                                                       │
│  ┌─────────────────┐                                                               │
│  │ Docker Daemon   │ ◄─── High-level operations (networking, volumes, images)    │
│  │   (dockerd)     │                                                               │
│  └─────────┬───────┘                                                               │
│            │ gRPC                                                                  │
│            ▼                                                                       │
│  ┌─────────────────┐                                                               │
│  │   containerd    │ ◄─── Container lifecycle, image management                  │
│  └─────────┬───────┘                                                               │
│            │ Runtime API                                                           │
│            ▼                                                                       │
│  ┌─────────────────┐                                                               │
│  │containerd-shim  │ ◄─── Process supervision, daemonless containers             │
│  └─────────┬───────┘                                                               │
│            │ exec()                                                                │
│            ▼                                                                       │
│  ┌─────────────────┐                                                               │
│  │      runc       │ ◄─── OCI runtime, kernel interface                         │
│  │                 │                                                               │
│  │ ┌─────────────┐ │      ┌─────────────────────────────────────────────────┐    │
│  │ │   Setup:    │ │      │            Linux Kernel                      │    │
│  │ │             │ │      │                                                 │    │
│  │ │• Namespaces │ │◄────►│ • PID Namespace                                │    │
│  │ │• cgroups    │ │      │ • Network Namespace                            │    │
│  │ │• Capabilities│ │      │ • Mount Namespace                              │    │
│  │ │• Seccomp    │ │      │ • IPC Namespace                                │    │
│  │ │• AppArmor   │ │      │ • UTS Namespace                                │    │
│  │ │• SELinux    │ │      │ • User Namespace                               │    │
│  │ └─────────────┘ │      │                                                 │    │
│  └─────────┬───────┘      │ • CPU cgroup                                   │    │
│            │              │ • Memory cgroup                                │    │
│            │              │ • I/O cgroup                                   │    │
│            │              │ • Network cgroup                               │    │
│            │              │                                                 │    │
│            │              │ • Capabilities                                 │    │
│            │              │ • Seccomp filters                              │    │
│            │              │ • LSM (AppArmor/SELinux)                       │    │
│            │              └─────────────────────────────────────────────────┘    │
│            │                                                                      │
│            ▼                                                                      │
│  ┌─────────────────┐                                                              │
│  │   Container     │ ◄─── Isolated application process                          │
│  │   Process       │                                                              │
│  │                 │                                                              │
│  │ ┌─────────────┐ │                                                              │
│  │ │ Application │ │                                                              │
│  │ │   Binary    │ │                                                              │
│  │ └─────────────┘ │                                                              │
│  └─────────────────┘                                                              │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### runc Responsibilities:

#### **1. OCI Runtime Specification Implementation**
runc implements the Open Container Initiative (OCI) runtime specification, which defines:
- Container configuration format
- Runtime lifecycle operations
- Container process management
- Security and isolation requirements

```bash
# OCI bundle structure
/path/to/bundle/
├── config.json          # Container configuration
├── runtime.json         # Runtime configuration (optional)
└── rootfs/             # Container root filesystem
    ├── bin/
    ├── etc/
    ├── lib/
    └── ...
```

#### **2. Namespace Management**
runc creates and manages Linux namespaces for container isolation:

```
Namespace Isolation:

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              Host System                                           │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                         Container                                           │  │
│  │                                                                             │  │
│  │  PID Namespace:     │  Network Namespace:  │  Mount Namespace:            │  │
│  │  ┌─────────────┐    │  ┌─────────────┐     │  ┌─────────────┐             │  │
│  │  │ PID 1: init │    │  │ eth0: veth  │     │  │ /: rootfs   │             │  │
│  │  │ PID 2: app  │    │  │ lo: loopback│     │  │ /proc: proc │             │  │
│  │  └─────────────┘    │  └─────────────┘     │  │ /sys: sysfs │             │  │
│  │                     │                      │  └─────────────┘             │  │
│  │                                                                             │  │
│  │  IPC Namespace:     │  UTS Namespace:      │  User Namespace:             │  │
│  │  ┌─────────────┐    │  ┌─────────────┐     │  ┌─────────────┐             │  │
│  │  │ Msg Queues  │    │  │ Hostname    │     │  │ UID mapping │             │  │
│  │  │ Semaphores  │    │  │ Domain name │     │  │ GID mapping │             │  │
│  │  │ Shared Mem  │    │  └─────────────┘     │  └─────────────┘             │  │
│  │  └─────────────┘    │                      │                               │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### **3. cgroups Resource Management**
runc configures cgroups to limit and monitor container resources:

```
cgroups Hierarchy:

/sys/fs/cgroup/
├── cpu/
│   └── docker/
│       └── container_id/
│           ├── cpu.cfs_quota_us      # CPU limit
│           ├── cpu.cfs_period_us     # CPU period
│           └── cpu.shares            # CPU weight
├── memory/
│   └── docker/
│       └── container_id/
│           ├── memory.limit_in_bytes # Memory limit
│           ├── memory.usage_in_bytes # Current usage
│           └── memory.oom_control    # OOM settings
├── blkio/
│   └── docker/
│       └── container_id/
│           ├── blkio.throttle.read_bps_device   # Read bandwidth
│           └── blkio.throttle.write_bps_device  # Write bandwidth
└── devices/
    └── docker/
        └── container_id/
            └── devices.list         # Allowed devices
```

### runc Operations:

#### **1. Container Creation Process**
```bash
# runc container lifecycle
runc create container_id --bundle /path/to/bundle
# Creates container but doesn't start it

runc start container_id
# Starts the container process

runc state container_id
# Shows container state

runc kill container_id SIGTERM
# Sends signal to container

runc delete container_id
# Removes container
```

#### **2. Direct runc Usage**
```bash
# Create OCI bundle from Docker image
mkdir -p /tmp/mycontainer/rootfs
docker export $(docker create nginx) | tar -C /tmp/mycontainer/rootfs -xf -

# Generate config.json
runc spec --bundle /tmp/mycontainer

# Edit config.json as needed
vim /tmp/mycontainer/config.json

# Run container with runc
cd /tmp/mycontainer
sudo runc run mycontainer
```

### Security Features Implemented by runc:

#### **1. Capabilities Management**
```json
// config.json - capabilities configuration
{
  "process": {
    "capabilities": {
      "bounding": [
        "CAP_CHOWN",
        "CAP_DAC_OVERRIDE",
        "CAP_FSETID"
      ],
      "effective": [
        "CAP_CHOWN",
        "CAP_DAC_OVERRIDE"
      ],
      "inheritable": [],
      "permitted": [
        "CAP_CHOWN",
        "CAP_DAC_OVERRIDE"
      ]
    }
  }
}
```

#### **2. Seccomp Profiles**
```json
// config.json - seccomp configuration
{
  "linux": {
    "seccomp": {
      "defaultAction": "SCMP_ACT_ERRNO",
      "architectures": ["SCMP_ARCH_X86_64"],
      "syscalls": [
        {
          "names": ["read", "write", "open", "close"],
          "action": "SCMP_ACT_ALLOW"
        }
      ]
    }
  }
}
```

#### **3. AppArmor/SELinux Integration**
```json
// config.json - LSM configuration
{
  "process": {
    "apparmorProfile": "docker-default",
    "selinuxLabel": "system_u:system_r:container_t:s0"
  }
}
```

### runc vs Other Runtimes:

| Runtime | Type | Use Case | Features |
|---------|------|----------|----------|
| **runc** | OCI | Standard containers | Full OCI compliance |
| **crun** | OCI | Fast startup | C implementation |
| **kata-runtime** | OCI | Secure containers | VM-based isolation |
| **gvisor** | OCI | Secure containers | User-space kernel |
| **firecracker** | Custom | Serverless | Micro-VMs |

### Debugging and Troubleshooting:

#### **1. Container State Inspection**
```bash
# Check container state
runc state container_id

# List all containers
runc list

# Get container events
runc events container_id

# Execute command in container
runc exec container_id /bin/sh
```

#### **2. Runtime Debugging**
```bash
# Enable debug logging
runc --debug run container_id

# Check system calls
strace -f runc run container_id

# Monitor cgroups
watch cat /sys/fs/cgroup/memory/docker/container_id/memory.usage_in_bytes
```

### Key Features Summary:

#### **1. OCI Compliance**
- Implements OCI Runtime Specification v1.0+
- Standard container format support
- Portable across different platforms
- Vendor-neutral implementation

#### **2. Security**
- Comprehensive namespace isolation
- cgroups resource limiting
- Capabilities dropping
- Seccomp system call filtering
- LSM (AppArmor/SELinux) support

#### **3. Performance**
- Minimal overhead
- Fast container startup
- Efficient resource utilization
- Direct kernel interface

#### **4. Portability**
- Works on multiple Linux distributions
- Architecture independent
- Standard OCI bundle format
- Integration with various container engines

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
