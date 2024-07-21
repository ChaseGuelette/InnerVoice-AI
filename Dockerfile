# Use an official Python runtime as a parent image
FROM python:3.12-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pip \
    build-essential

# Make portaudio available for C extensions
ENV PORTAUDIO_INCLUDE_DIR=/usr/include/portaudio
ENV PORTAUDIO_LIB_DIR=/usr/lib

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make portaudio available at runtime
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib

# Run app.py when the container launches
CMD ["python3", "app.py"]