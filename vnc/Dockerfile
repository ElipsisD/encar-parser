FROM python:3.12-slim

ENV DISPLAY=:0
ENV SCREEN=0
ENV GEOMETRY=1920x1080x24
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    fonts-liberation \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* && \
    CHROME_VERSION=$(google-chrome --product-version) && \
    wget -q --continue -P /chromedriver "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/ && \
    rm -rf /chromedriver

# Установка Python-зависимостей
RUN pip install selenium selenium-stealth requests setuptools undetected-chromedriver

# Копирование файлов
COPY entrypoint.sh /entrypoint.sh
COPY app.py /app/app.py
RUN chmod +x /entrypoint.sh

EXPOSE 5900

CMD ["/entrypoint.sh"]
