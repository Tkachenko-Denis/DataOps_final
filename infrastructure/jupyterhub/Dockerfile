FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /srv/jupyterhub

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    jupyterhub==5.3.0 \
    jupyterlab==4.4.1 \
    notebook==7.4.1

RUN npm install -g configurable-http-proxy

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

EXPOSE 8000

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
