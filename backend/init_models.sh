#!/bin/sh

echo "🚀 Ollama Model Provisioning startet..."

sleep 5

# Liste gewünschter Modelle
MODELS="llama3"

for model in $MODELS; do
  echo "🔍 Prüfe Modell: $model"

  ollama list | grep "$model" > /dev/null

  if [ $? -ne 0 ]; then
    echo "⬇️ Lade Modell: $model"
    ollama pull $model
  else
    echo "✅ Modell vorhanden: $model"
  fi
done

echo "✅ Model Provisioning fertig"
