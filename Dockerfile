FROM python:3.12.6-alpine3.20

LABEL org.opencontainers.image.title="Dreifaltigkeit"
LABEL org.opencontainers.image.description="Website of our parish and kindergarden"
LABEL org.opencontainers.image.url="https://github.com/normanjaeckel/Dreifaltigkeit"
LABEL org.opencontainers.image.source="https://github.com/normanjaeckel/Dreifaltigkeit"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY dreifaltigkeit dreifaltigkeit/
COPY dreifaltigkeit_settings.py dreifaltigkeit_wsgi.py manage.py requirements.txt ./

RUN pip install --root-user-action ignore --requirement requirements.txt
RUN python manage.py collectstatic

VOLUME /app/static

ENV DREIFALTIGKEIT_SITE_ID=parish
ENV DREIFALTIGKEIT_HOST=parish.example.com
ENV DREIFALTIGKEIT_LINK_TO_OTHER_SITE=https://kindergarden.example.com
ENV DREIFALTIGKEIT_DEBUG=
ENV DJANGO_SECRET_KEY_FILE=/run/secrets/django_secret_key
ENV POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password

EXPOSE 8000

CMD ["gunicorn", "--bind=:8000", "dreifaltigkeit_wsgi"]
