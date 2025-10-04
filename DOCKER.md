# Docker Setup for AdaptLearn

This guide will help you build and run the AdaptLearn platform using Docker.

## Prerequisites

- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Get Docker Compose](https://docs.docker.com/compose/install/))

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kirby86ka/Edutech.git
cd Edutech
```

### 2. Set Up Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
SESSION_SECRET=your_secure_random_string
ADMIN_API_KEY=your_admin_key
AI_API_KEY=your_ai_key
```

### 3. Build and Run with Docker Compose

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Start the backend API on port 8000
- Start the frontend on port 5000

### 4. Access the Application

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Stop the Application

```bash
docker-compose down
```

## Manual Docker Build

If you prefer to build and run manually:

### Build the Image

```bash
docker build -t adaptlearn:latest .
```

### Run the Container

```bash
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e SESSION_SECRET=your_session_secret \
  --name adaptlearn \
  adaptlearn:latest
```

## Available Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Restart Services

```bash
docker-compose restart
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build
```

### Remove Everything (including volumes)

```bash
docker-compose down -v
```

## Docker Image Details

### Multi-Stage Build

The Dockerfile uses a multi-stage build:

1. **Stage 1**: Builds the React frontend using Node.js
2. **Stage 2**: Sets up Python backend and copies frontend build

### Exposed Ports

- **8000**: FastAPI backend
- **5000**: Nginx frontend

### Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `SESSION_SECRET`: Secret key for session management

Optional:
- `ADMIN_API_KEY`: Admin API authentication (default: admin-key-123)
- `AI_API_KEY`: AI agent authentication (default: ai-key-456)

## Health Checks

Both services have health checks configured:

- **Backend**: Checks `/api/subjects` endpoint every 30s
- **Frontend**: Checks Nginx server every 30s

## Troubleshooting

### Port Already in Use

If ports 5000 or 8000 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "3000:80"  # Change frontend port to 3000
  - "9000:8000"  # Change backend port to 9000
```

### View Container Logs

```bash
docker logs adaptlearn-backend
docker logs adaptlearn-frontend
```

### Enter Container Shell

```bash
docker exec -it adaptlearn-backend /bin/sh
```

### Check Container Status

```bash
docker ps
```

## Production Deployment

For production, consider:

1. Use proper secrets management (not .env files)
2. Set up reverse proxy (Nginx/Traefik) with SSL
3. Configure proper CORS origins
4. Use production-grade database instead of in-memory storage
5. Set up monitoring and logging
6. Use container orchestration (Kubernetes, Docker Swarm)

## Network Architecture

The services communicate through a Docker network called `adaptlearn-network`:

```
Frontend (Nginx) :5000 
    ↓
    API Proxy → Backend (FastAPI) :8000
```

Frontend requests to `/api/*` are automatically proxied to the backend service.
