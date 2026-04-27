FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

WORKDIR /app

# Copy everything first
COPY . .

# Build React frontend
RUN cd frontend && npm install && npm run build

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy built React into backend static folder
RUN mkdir -p backend/static && cp -r frontend/dist/. backend/static/

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--app-dir", "backend"]