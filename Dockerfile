FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates \
    chromium-driver chromium \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

RUN GECKODRIVER_VERSION=0.34.0 && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz" && \
    tar -xzf "geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz" -C /usr/local/bin && \
    rm "geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz"

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PATH="/usr/lib/chromium:/usr/bin:${PATH}"

