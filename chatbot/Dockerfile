FROM python:3.12-slim

RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install streamlit requests

COPY app.py .

ENV OLLAMA_URL=http://host.docker.internal:11434

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]