FROM python:3.11-slim

# Install curl (needed to install Ollama) and clean up apt cache to keep the image smaller
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces requires containers to run as a non-root user (UID 1000)
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Copy requirements first and install - this lets Docker cache this layer,
# so if you only change your Python code later, this slow step gets skipped
# on rebuilds instead of reinstalling everything from scratch.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Try to pre-pull the vision model INTO the image itself, so it doesn't need
# to re-download every time the Space restarts (since the disk isn't persistent,
# but the image's own layers ARE). If this fails for any reason during build,
# entrypoint.sh below will fall back to pulling it at container startup instead.
RUN (ollama serve &) && sleep 5 && ollama pull llava; pkill ollama || true

RUN chown -R user:user /app /home/user
USER user

# Hugging Face Spaces' Docker SDK expects the app to listen on port 7860
EXPOSE 7860

COPY --chown=user:user entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]