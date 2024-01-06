FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron supervisor git build-essential zlib1g-dev libjpeg-dev libopenjp2-7-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/SpawW/RPI_SSD1306.git .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN service cron start

COPY . .

COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

CMD ["supervisord", "-n"]
