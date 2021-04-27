FROM nanome/plugin-env

ENV ARGS=''
WORKDIR /app

# TODO: install non-pip dependencies here

ARG CACHEBUST
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python run.py ${ARGS}
