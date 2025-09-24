# Docker Compose

## 1. What is Docker Compose and how does it differ from Docker?

### Answer:

### Docker Compose Overview:
Docker Compose is a tool for defining and running multi-container Docker applications. It uses YAML files to configure application services, networks, and volumes.

### Key Differences:

| Aspect | Docker | Docker Compose |
|--------|--------|----------------|
| **Scope** | Single container | Multi-container applications |
| **Configuration** | Command line | YAML file |
| **Orchestration** | Manual | Automated |
| **Networking** | Manual setup | Automatic |
| **Scaling** | Manual | Built-in scaling |

### When to Use:
- **Docker**: Single container, simple applications
- **Docker Compose**: Multi-service applications, development environments

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

### 1. Direct Definition
```yaml
services:
  web:
    image: nginx
    environment:
      - NODE_ENV=production
      - DEBUG=false
      - API_URL=https://api.example.com
```

### 2. Environment File
```yaml
services:
  web:
    image: nginx
    env_file:
      - .env
      - .env.production
```

### 3. Variable Substitution
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

### 4. External Environment Files
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

### 1. Named Volumes
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

### 2. Bind Mounts
```yaml
version: '3.8'
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
```

### 3. Anonymous Volumes
```yaml
version: '3.8'
services:
  web:
    image: nginx
    volumes:
      - /var/cache/nginx
```

### 4. External Volumes
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

### 1. Resource Limits
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
      start_period: 40s
```

### 3. Restart Policies
```yaml
version: '3.8'
services:
  web:
    image: nginx
    restart: unless-stopped
```

### 4. Logging Configuration
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

### 5. Security Configuration
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

### 6. Network Security
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

## Follow-up Questions:
- How do you migrate from Docker Compose to Kubernetes?
- What are the limitations of Docker Compose for production?
- How do you implement CI/CD with Docker Compose?
- What is the difference between Docker Compose and Docker Swarm?
