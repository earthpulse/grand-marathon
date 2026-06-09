FROM ghcr.io/astral-sh/uv:0.6.17-python3.12-bookworm-slim

WORKDIR /app

# Install system dependencies required for WeasyPrint and GDAL, and clean up in one layer
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        g++ \
        libgdal-dev \
        libcairo2 \
        pango1.0-tools \
        libpango1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        libxml2 \
        libxslt1.1 \
        libjpeg62-turbo \
        fonts-liberation \
        fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN uv venv

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN uv pip install -r requirements.txt

COPY . api/

# Use uv to run your app (no need for a separate venv in most Docker use cases)
CMD ["uv", "run", "python3", "api/main.py", "--host", "0.0.0.0", "--port", "8000"]