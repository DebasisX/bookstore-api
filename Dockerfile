FROM python:3.10-slim

# Set environment variables

# to remove bycode cache .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# for print and logging
ENV PYTHONUNBUFFERED 1 

WORKDIR /app

RUN mkdir /data

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python", "app.py"]
