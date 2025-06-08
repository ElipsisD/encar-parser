#!/bin/bash

VNC_PASSWD_FILE="$HOME/.vnc/passwd"
mkdir -p "$(dirname "$VNC_PASSWD_FILE")"

echo "[INFO] Установка VNC пароля"
x11vnc -storepasswd "$VNC_PASS" "$VNC_PASSWD_FILE"

echo "[INFO] Запуск виртуального дисплея (Xvfb)..."
Xvfb :0 -screen 0 ${GEOMETRY} &

echo "[INFO] Запуск оконного менеджера (Fluxbox)..."
fluxbox &

echo "[INFO] Запуск VNC-сервера (x11vnc)..."
x11vnc -display :0 -forever -usepw -shared -rfbport 5900 &

sleep 2

echo "[INFO] Запуск Selenium-приложения..."
python /app/app.py

#google-chrome --no-sandbox --disable-dev-shm-usage --disable-gpu &
#tail -f /dev/null
