# Настройка NIFI

1) Остановить контейнеры и удалить их в папке где запущен контейнер Nifi

```angular2html
docker-compose down
```

2) Удалите Docker volume:

```angular2html
docker volume rm nifi_data
```

3) Удалите оставшиеся файлы и папки:

```angular2html
sudo rm -rf /opt/nifi
```

Создание скрипта для установки и настройки NiFi `setup_nifi.sh`
```angular2html
#!/bin/bash

# Установка необходимых пакетов
sudo apt-get update
sudo apt-get install -y wget curl

# Удаление старых данных и остановка контейнеров
docker-compose -f /opt/nifi/docker-compose.yml down
docker volume rm nifi_data
sudo rm -rf /opt/nifi

# Создание папок
sudo mkdir -p /opt/nifi
sudo chown $USER:$USER /opt/nifi

# Переход в папку /opt/nifi
cd /opt/nifi

# Создание Docker Compose файла
cat <<EOL > docker-compose.yml
version: '3.8'

services:
  nifi:
    image: apache/nifi:latest
    container_name: nifi_nifi_1
    ports:
      - "8010:8080"
    environment:
      - NIFI_WEB_HTTP_PORT=8080
    user: "root"
    volumes:
      - nifi_data:/opt/nifi/nifi-current/data
    restart: always
    
volumes:
  nifi_data:
    driver: local
EOL

# Имя контейнера
CONTAINER_NAME=nifi_nifi_1

# Запуск Docker Compose из правильной директории
docker-compose -f /opt/nifi/docker-compose.yml up -d

echo "NiFi setup complete. You can access NiFi at http://localhost:8010/nifi"

```

Проверка доступности папки

Переходим внутрь контейнера
```angular2html
docker exec -it nifi_nifi_1 bash
```
```angular2html
chown -R nifi:nifi /opt/nifi/nifi-current/data
```
```angular2html
chmod -R 775 /opt/nifi/nifi-current/data

```
```angular2html
echo "This is a test file from NiFi container" > /opt/nifi/nifi-current/data/testfile_from_nifi.txt
```
Скачиваем jar
```angular2html
wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar -P /opt/nifi/nifi-current/data/
```
