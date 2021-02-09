FROM python:3.9.1-slim-buster
ENV PYTHONUNBUFFERED 1

# Copy source files
RUN mkdir -p /www/app
COPY . /www/app/
WORKDIR /www/app
# Install pipenv and dependencies
RUN pip install --upgrade pip pipenv && pipenv install --dev --system --deploy
RUN chown -R www-data:www-data /www/app

# start server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/www/app/start-server.sh"]