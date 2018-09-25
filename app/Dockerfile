FROM python:3.6

ADD . /users

WORKDIR /users

RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]