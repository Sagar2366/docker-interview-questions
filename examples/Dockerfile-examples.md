# Dockerfile Examples

## 1. Basic Node.js Application

### Simple Node.js App
```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### Multi-stage Node.js Build
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npm", "start"]
```

## 2. Python Application

### Basic Python App
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

### Python with Virtual Environment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

## 3. Java Application

### Spring Boot Application
```dockerfile
FROM openjdk:11-jre-slim

WORKDIR /app

COPY target/app.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
```

### Multi-stage Java Build
```dockerfile
# Build stage
FROM maven:3.8-openjdk-11 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Production stage
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=builder /app/target/app.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

## 4. Nginx Web Server

### Basic Nginx
```dockerfile
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Nginx with SSL
```dockerfile
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY ssl/ /etc/nginx/ssl/
COPY html/ /usr/share/nginx/html/

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

## 5. Database Applications

### PostgreSQL
```dockerfile
FROM postgres:13-alpine

ENV POSTGRES_DB=myapp
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["postgres"]
```

### MySQL
```dockerfile
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=myapp
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
```

## 6. Go Application

### Basic Go App
```dockerfile
FROM golang:1.19-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o app

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/app .
EXPOSE 8080
CMD ["./app"]
```

### Go with CGO
```dockerfile
FROM golang:1.19-alpine AS builder

RUN apk add --no-cache gcc musl-dev
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 go build -o app

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/app .
EXPOSE 8080
CMD ["./app"]
```

## 7. PHP Application

### Basic PHP App
```dockerfile
FROM php:8.1-fpm-alpine

WORKDIR /var/www/html

RUN apk add --no-cache \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev

RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd pdo pdo_mysql

COPY . .

EXPOSE 9000

CMD ["php-fpm"]
```

### PHP with Nginx
```dockerfile
FROM php:8.1-fpm-alpine

WORKDIR /var/www/html

RUN apk add --no-cache \
    nginx \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev

RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd pdo pdo_mysql

COPY nginx.conf /etc/nginx/nginx.conf
COPY . .

EXPOSE 80

CMD ["sh", "-c", "php-fpm -D && nginx -g 'daemon off;'"]
```

## 8. Rust Application

### Basic Rust App
```dockerfile
FROM rust:1.65-alpine AS builder

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release

COPY src ./src
RUN touch src/main.rs
RUN cargo build --release

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/target/release/app .
EXPOSE 8080
CMD ["./app"]
```

## 9. Security-Focused Dockerfile

### Secure Node.js App
```dockerfile
FROM node:16-alpine

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy application code
COPY --chown=nextjs:nodejs . .

# Switch to non-root user
USER nextjs

EXPOSE 3000

CMD ["npm", "start"]
```

### Secure Python App
```dockerfile
FROM python:3.9-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["python", "app.py"]
```

## 10. Multi-Architecture Dockerfile

### Multi-arch Node.js App
```dockerfile
FROM --platform=$BUILDPLATFORM node:16-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npm", "start"]
```

## Best Practices

### 1. Use .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.nyc_output
.coverage
.coverage/
```

### 2. Optimize Layer Caching
```dockerfile
# Bad: Changes to code invalidate package installation
COPY . .
RUN npm install

# Good: Package installation cached separately
COPY package*.json ./
RUN npm install
COPY . .
```

### 3. Use Multi-stage Builds
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["npm", "start"]
```

### 4. Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

### 5. Labels
```dockerfile
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="My application"
```
