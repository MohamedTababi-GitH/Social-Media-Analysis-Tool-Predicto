FROM python:3.10-slim



RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

#create wd for container
WORKDIR /app

#copy req file
COPY requirements-docker.txt .
RUN pip install --upgrade pip
#install dependencies
RUN pip install --no-cache-dir -r requirements-docker.txt
RUN python -m nltk.downloader stopwords
COPY . /app
EXPOSE 5000

#cmd to run the app
CMD [ "python", "predicto_app.py" ]
