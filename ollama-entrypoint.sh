#!/bin/sh

echo "🚀 Starting Ollama..."
ollama serve &

echo "⏳ Waiting for Ollama API..."
sleep 5

echo "📦 Pulling llama3 model (if not exists)..."
ollama pull llama3

echo "✅ Ready!"

wait
