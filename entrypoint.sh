#!/bin/bash
set -e

# Start Ollama's background server
ollama serve &
sleep 5

# If llava wasn't successfully baked into the image during the Docker build
# (the RUN step in the Dockerfile can silently fail in some environments),
# pull it now instead. This makes the container self-healing at the cost of
# a slower first startup in that fallback case.
if ! ollama list | grep -q llava; then
  echo "llava not found in image, pulling now (this may take a few minutes)..."
  ollama pull llava
fi

exec uvicorn api:app --host 0.0.0.0 --port 7860