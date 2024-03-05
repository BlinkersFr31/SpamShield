FROM python:3.7-alpine AS builder
RUN apk update
RUN apk add git
RUN apk add linux-headers
RUN apk add musl-dev
RUN apk add gcc
RUN apk add libffi-dev
WORKDIR /
#ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN git clone https://github.com/BlinkersFr31/SpamShield.git
RUN pip install --user -r SpamShield/requirements.txt

FROM python:3.7-alpine
COPY --from=builder /SpamShield /opt
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
WORKDIR /opt/SpamShield/SpamShield
RUN sed -i "s/allowed.example.test/URL_FINALE/g" settings.py
WORKDIR /opt/SpamShield
ENTRYPOINT ["python", "manage.py"]
RUN python3 manage.py migrate
ENV DJANGO_SUPERUSER_PASSWORD=PASSWORD
RUN python3 manage.py createsuperuser --noinput --username adminS --email MAIL
CMD ["runserver", "0.0.0.0:8000"]
