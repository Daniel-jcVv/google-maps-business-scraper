# 1. Base: Python Oficial (Alpine) - Garantiza que Python 3 existe y funciona
FROM python:3.11-alpine

# 2. Instalar Node.js y n8n
# 'npm' viene con nodejs. 'git' es util para instalar nodos custom de n8n si se necesita.
RUN apk add --update --no-cache nodejs npm git && \
    npm install -g n8n

# 3. Crear usuario seguro 'node' (igual que la imagen oficial)
RUN addgroup -g 1000 node && \
    adduser -u 1000 -G node -s /bin/sh -D node

# 4. Configurar entorno de trabajo
USER node
WORKDIR /home/node

# 5. Punto de entrada
ENTRYPOINT ["n8n"]
