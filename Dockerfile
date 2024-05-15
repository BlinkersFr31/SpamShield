FROM python:3.7-alpine AS builder
RUN apk update
RUN apk add curl
RUN apk add linux-headers
RUN apk add musl-dev
RUN apk add gcc
RUN apk add libffi-dev
RUN apk add dos2unix
RUN apk add git
WORKDIR /
#ADD "https://api.github.com/repos/BlinkersFr31/SpamShield/commits?per_page=1" latest_commit
RUN git clone https://github.com/BlinkersFr31/SpamShield.git
RUN pip install --user -r SpamShield/requirements.txt
RUN sed -i "s/allowed.example.test/spamshield.s.brondino.fr/g" SpamShield/SpamShield/SpamShield/settings.py
WORKDIR /SpamShield/SpamShield
RUN mkdir data
RUN dos2unix entrypoint.sh
RUN chmod +x entrypoint.sh

FROM python:3.7-alpine
COPY --from=builder /SpamShield /opt
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
WORKDIR /opt/SpamShield
ENTRYPOINT ["/opt/SpamShield/entrypoint.sh"]
CMD ["start"]
