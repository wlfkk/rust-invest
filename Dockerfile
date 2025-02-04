FROM python:3.10
COPY . /app/
RUN pip install -r /app/requirements.txt
RUN chmod 0644 /app/job.sh
RUN apt-get update
RUN apt-get -y install cron
RUN crontab -l | { cat; echo "0 0 * * * bash /app/job.sh"; } | crontab -
RUN cron
CMD ["python3.10", "app/main.py"]
