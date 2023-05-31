FROM python:3.9.5


ENV PYTHONIOENCODING=UTF-8

# Creating workspace
ENV WORKSPACE=/usr/src/app

RUN mkdir -p $WORKSPACE
WORKDIR $WORKSPACE

# Project dependency
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . $WORKSPACE

CMD ["python","app.py"]
