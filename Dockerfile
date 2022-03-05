FROM python:3.9

WORKDIR /app

# https://github.com/twintproject/twint#march-2-2021-update
# From the author: "Noticed a lot of people are having issues installing (including me). Please use the Dockerfile temporarily while I look into them."
#RUN cd /root && git clone --depth=1 https://github.com/twintproject/twint.git \
#    && cd twint \
#	&& pip3 install . -r requirements.txt

COPY requirements.txt .
COPY requirements.in .

RUN cd /app \
    && pip3 install pip-tools \
    && pip-sync \
    && pip3 install --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

COPY . .

ENV FLASK_APP=twipeater.py

EXPOSE 5000

CMD /usr/local/bin/flask run --host=0.0.0.0
