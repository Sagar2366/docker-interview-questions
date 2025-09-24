# Docker Architecture Diagram

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Docker CLI    │    │   API Client    │
│   (docker cmd)  │    │   (REST API)    │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌──────────▼───────┐
          │  Docker Daemon   │
          │    (dockerd)     │
          └──────────┬───────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│containerd│    │ Images  │    │Registry │
│         │    │ Storage │    │         │
└────┬────┘    └─────────┘    └─────────┘
     │
     ▼
┌─────────┐
│  runc   │
└────┬────┘
     │
     ▼
┌─────────┐
│Container│
└─────────┘
```

## Container Runtime Stack

```
Docker CLI
    │
    ▼
Docker Daemon (dockerd)
    │
    ▼
containerd (high-level runtime)
    │
    ▼
containerd-shim (process manager)
    │
    ▼
runc (low-level runtime)
    │
    ▼
Container Process
```

## Docker Networking Architecture

```
Host Network Interface
    │
    ▼
┌─────────────────────────────────────┐
│           Docker Host               │
│                                     │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   docker0   │  │  Custom     │  │
│  │  (bridge)   │  │  Networks   │  │
│  │             │  │             │  │
│  │ Container A │  │ Container C │  │
│  │ Container B │  │ Container D │  │
│  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────┘
```

## Docker Storage Layers

```
Container Layer (Read-Write)
    │
    ▼
┌─────────────────┐
│  Image Layer 3  │ (Read-Only)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  Image Layer 2  │ (Read-Only)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  Image Layer 1  │ (Read-Only)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  Base Image     │ (Read-Only)
└─────────────────┘
```

## Docker Namespaces

```
Host System
    │
    ├── PID Namespace (Process Isolation)
    ├── Network Namespace (Network Isolation)
    ├── Mount Namespace (Filesystem Isolation)
    ├── IPC Namespace (IPC Isolation)
    ├── UTS Namespace (Hostname Isolation)
    └── User Namespace (User ID Isolation)
```

## Docker cgroups

```
/sys/fs/cgroup/
    │
    ├── cpu/          (CPU limits)
    ├── memory/       (Memory limits)
    ├── blkio/        (I/O limits)
    ├── net_cls/      (Network limits)
    └── devices/      (Device access)
```
