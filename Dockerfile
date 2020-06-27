FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
COPY ./network_speed_test.py ./speedtest.py ./ 
CMD [ "python", "./network_speed_test.py" ]
