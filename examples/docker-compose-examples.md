# Docker Compose Examples

## 1. Basic Web Application

### Simple LAMP Stack
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - php

  php:
    image: php:8.1-fpm-alpine
    volumes:
      - ./html:/var/www/html
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: myapp
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 2. Node.js Application with Database

### Full-Stack Node.js App
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=myapp
      - DB_USER=user
      - DB_PASSWORD=password
    depends_on:
      - db
      - redis

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 3. Microservices Architecture

### Multi-Service Application
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
      - frontend

  frontend:
    build: ./frontend
    environment:
      - API_URL=http://api:3000
    depends_on:
      - api

  api:
    build: ./api
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=myapp
      - DB_USER=user
      - DB_PASSWORD=password
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

  worker:
    build: ./worker
    environment:
      - DB_HOST=db
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

## 4. Development Environment

### Development Setup with Hot Reload
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DB_HOST=db
    depends_on:
      - db
    command: npm run dev

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"

volumes:
  postgres_data:
```

## 5. Production-Ready Setup

### Production Configuration
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=myapp
      - DB_USER=user
      - DB_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    depends_on:
      - db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
  redis_data:
```

## 6. Monitoring Stack

### Monitoring with Prometheus and Grafana
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
```

## 7. CI/CD Pipeline

### CI/CD with Jenkins
```yaml
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_data:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - JAVA_OPTS=-Djenkins.install.runSetupWizard=false
    depends_on:
      - sonarqube

  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions
    environment:
      - SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true

  nexus:
    image: sonatype/nexus3
    ports:
      - "8081:8081"
    volumes:
      - nexus_data:/nexus-data
    environment:
      - INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m

volumes:
  jenkins_data:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:
  nexus_data:
```

## 8. Database Clustering

### PostgreSQL Cluster
```yaml
version: '3.8'

services:
  postgres-master:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_REPLICATION_USER: replicator
      POSTGRES_REPLICATION_PASSWORD: replicator_password
    volumes:
      - postgres_master_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    command: >
      postgres
      -c wal_level=replica
      -c max_wal_senders=3
      -c max_replication_slots=3
      -c hot_standby=on

  postgres-slave:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      PGUSER: postgres
    volumes:
      - postgres_slave_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    depends_on:
      - postgres-master
    command: >
      bash -c "
      until pg_basebackup -h postgres-master -D /var/lib/postgresql/data -U replicator -v -P -W
      do
        echo 'Waiting for master to be available...'
        sleep 1s
      done
      echo 'standby_mode = on' >> /var/lib/postgresql/data/recovery.conf
      echo 'primary_conninfo = \"host=postgres-master port=5432 user=replicator\"' >> /var/lib/postgresql/data/recovery.conf
      postgres
      "

volumes:
  postgres_master_data:
  postgres_slave_data:
```

## 9. Load Balancing

### Load Balanced Application
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web1
      - web2
      - web3

  web1:
    build: .
    environment:
      - INSTANCE_ID=1
    depends_on:
      - db

  web2:
    build: .
    environment:
      - INSTANCE_ID=2
    depends_on:
      - db

  web3:
    build: .
    environment:
      - INSTANCE_ID=3
    depends_on:
      - db

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 10. Security-Focused Setup

### Secure Multi-Service Application
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=myapp
      - DB_USER=user
      - DB_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    depends_on:
      - db
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    user: "999:999"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    user: "999:999"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'
        reservations:
          memory: 128M
          cpus: '0.1'

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    driver: bridge
    internal: false
```
