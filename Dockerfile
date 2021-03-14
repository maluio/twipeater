FROM python:3.9

WORKDIR /app

RUN cd /root && git clone --depth=1 https://github.com/twintproject/twint.git \
    && cd twint \
	&& pip3 install . -r requirements.txt

COPY requirements.txt .

RUN cd /app \
    && pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=twipeater.py

EXPOSE 5000

CMD /usr/local/bin/flask run --host=0.0.0.0
