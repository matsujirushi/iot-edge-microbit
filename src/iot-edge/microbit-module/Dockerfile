FROM ubuntu:xenial-20180417

WORKDIR /app

# pip

RUN apt-get update && \
    apt-get install -y --no-install-recommends python-pip && \
    pip install -U pip && \
    chmod -R a+rx /usr/local/lib/python2.7/site-packages && \
    rm -rf /var/lib/apt/lists/*

# azure-iothub-device-client

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt && \
    rm -f requirements.txt

# BluefruitLE

RUN apt-get update && \
    apt-get install -y --no-install-recommends git python-dbus python-gi && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/donatieng/Adafruit_Python_BluefruitLE.git && \
    cd Adafruit_Python_BluefruitLE && \
    python setup.py install
RUN rm -rf ./Adafruit_Python_BluefruitLE

COPY . .

CMD [ "python", "-u", "./main.py" ]
