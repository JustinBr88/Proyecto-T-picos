# syntax=docker/dockerfile:1

# Imagen de DESARROLLO de Fancy Hotel: servidor de Flask con recarga automática y
# las dependencias de test (para correr pytest dentro del contenedor).
# No está pensada para producción.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Primero las dependencias: esta capa se reutiliza mientras los requirements no cambien.
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements-dev.txt

# Usuario sin privilegios: la app no necesita ser root. /app también es suyo
# (pytest escribe su caché ahí).
RUN useradd --create-home --uid 10001 app && chown app:app /app
COPY --chown=app:app . .
USER app

EXPOSE 5000

# Al arrancar: carga datos de prueba si la base está vacía (no borra nada) y
# levanta el servidor. 0.0.0.0 es dentro del contenedor; compose.yaml sólo lo
# publica en localhost.
CMD ["sh", "-c", "flask --app fancyhotel seed-db --if-empty && exec flask --app fancyhotel run --host 0.0.0.0 --port 5000"]
