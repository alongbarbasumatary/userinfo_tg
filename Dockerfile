# Use a lightweight official Python image
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port Render expects
EXPOSE 8080

# The environment variables TELEGRAM_TOKEN and BOT_URL
# should be set in Render's Environment Variables dashboard

# Command to start the bot
CMD ["python", "app.py"]
