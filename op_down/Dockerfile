# Use Python 3.12 slim image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /django-app

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Run npm to build Tailwind CSS
RUN npm install && npm run build:css

# Collect static files for Django
RUN python3 manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=op_down.settings

# Run Gunicorn to serve the Django app
CMD ["gunicorn", "op_down.wsgi:application", "--bind", "0.0.0.0:8000"]
