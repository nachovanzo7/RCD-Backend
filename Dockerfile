FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1

WORKDIR /app
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=rcdproject.rcdproject.settings

# Instala dependencias necesarias del sistema
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Instalación de dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el código fuente
COPY . /app/

# Archivos estáticos de Django
RUN python manage.py collectstatic --noinput

# Puerto recomendado para Render
EXPOSE 8000

# Comando de arranque compatible con Render
CMD ["gunicorn", "rcdproject.rcdproject.wsgi:application", "--bind", "0.0.0.0:8000"]
