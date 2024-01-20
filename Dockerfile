# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /fyle-interview-intern-backend

# Copy the current directory contents into the container at /fyle-interview-intern-backend
COPY . /fyle-interview-intern-backend

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV FLASK_APP=core/server.py
ENV NAME fyle

# Make port 7755 available to the world outside this container
EXPOSE 7755

# Remove the existing SQLite database file
RUN rm core/store.sqlite3

# Perform Flask database migration
RUN flask db upgrade -d core/migrations/



# Command to run the application
CMD ["bash", "run.sh"]


