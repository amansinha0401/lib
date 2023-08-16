# Use the official Python image as a base
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# docker build -t my-django-app .
# docker tag my-django-app:latest my-django-app:new-version
# docker push my-django-app:new-version

# Pull the updated image:
# docker pull my-django-app:new-version

# Run a new container based on the updated image:
# docker run -it --rm -p 8000:8000 my-django-app:new-version
