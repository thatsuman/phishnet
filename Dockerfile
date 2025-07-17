FROM python:3.10-slim-bullseye
WORKDIR /app
COPY . /app

# Install AWS CLI via pip for better compatibility
RUN pip install awscli

RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]