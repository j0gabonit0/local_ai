# Nextcloud AI RAG System

Lokales KI-System mit Nextcloud Integration (DSGVO-konform)

## Features
- Nextcloud als Datenquelle (10.0.5.15)
- Rechtebasierter Zugriff (Gruppen)
- Lokale KI (Ollama + Llama3)
- Streaming Chat UI
- Chat History pro User
- Automatischer Watcher

## Start

```bash
docker compose up -d --build

---

# 🐳 5. Docker Setup

```bash id="g7"
cat > docker-compose.yml << 'EOF'
version: "3.9"

services:

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - NEXTCLOUD_URL=http://10.0.5.15
      - NEXTCLOUD_USER=ai_user
      - NEXTCLOUD_PASSWORD=APP_PASSWORD_HIER
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama

  frontend:
    image: nginx
    ports:
      - "3000:80"
    volumes:
      - ./frontend:/usr/share/nginx/html

volumes:
  ollama:
