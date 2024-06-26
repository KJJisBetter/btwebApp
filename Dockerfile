FROM python:3.12.4-slim-bookworm

# Set the working directory
WORKDIR /btwebApp

# Copy the current directory contents into the container at /btwebApp
COPY . /btwebApp

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV flask_app=run.py

# Run app.py when the container launches
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "run:app"]