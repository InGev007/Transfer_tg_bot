FROM python:3

RUN adduser nonroot
USER nonroot

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python","-u","./bot.py" ]
