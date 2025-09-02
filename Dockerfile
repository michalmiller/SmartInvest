FROM ollama/ollama

# Serve ollama when container starts
CMD ["ollama", "serve"]
