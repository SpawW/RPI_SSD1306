FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y supervisor git build-essential && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/SpawW/RPI_SSD1306.git .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob

COPY app.py .

COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

CMD ["supervisord", "-n"]
