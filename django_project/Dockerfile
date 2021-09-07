# BUILDER #
 
FROM python:3.9.7-buster as builder
 
WORKDIR /usr/src/app
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
RUN apt-get update && \
    apt-get -y install gcc \
    libmariadb-dev \
    git \
    zip \
    unzip \
    vim \
    libpng-dev \
    libpq-dev

RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
 
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt



# FINAL #
 
FROM python:3.9.7-buster
 
RUN mkdir -p /home/app
 
# RUN addgroup --system app && adduser --system app -g app
 
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME
 
RUN apt-get update && \
    apt-get -y install libpq-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*
 
# COPY ./entrypoint.sh $APP_HOME
 
COPY . $APP_HOME

# RUN chown -R app:app $APP_HOME
 
# USER app
 
# ENTRYPOINT ["/home/app/web/entrypoint.sh"]