FROM python:3.10

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    flask-mysqldb \
    mysqlclient \
    python-dateutil \
    werkzeug

EXPOSE 5000

CMD ["python", "Gridspace/main.py"]