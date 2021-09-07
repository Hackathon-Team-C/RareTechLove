# image
FROM php:7.2-apache

# Set php.ini
COPY ./php.ini /usr/local/etc/php/

# Set apache conf (Before tag:5.4-apache)
# COPY ./apache2.conf /etc/apache2/
# COPY ./sites/*.conf /etc/apache2/sites-available/

# Set apache conf (After tag:5.5-apache)
ENV APACHE_DOCUMENT_ROOT /var/www/html
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Install MySQL connection module
RUN apt-get update \
  && apt-get install -y libpq-dev vim \
  && docker-php-ext-install pdo_mysql pdo_pgsql mysqli mbstring

# RUN rm /etc/apache2/sites-available/000-default.conf
# RUN rm /etc/apache2/ports.conf

# COPY ./.conf/000-default.conf etc/apache2/sites-available
# COPY ./.conf/ports.conf /etc/apache2