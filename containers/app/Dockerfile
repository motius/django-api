FROM python:3.8.0-alpine as builder

WORKDIR /build

# install dependencies
RUN apk add --no-cache git gcc musl-dev postgresql-dev \
	libjpeg-turbo-dev zlib-dev

COPY requirements.txt requirements-devel.txt ./
RUN pip3 wheel \
		--no-cache-dir \
		--no-deps \
		--wheel-dir wheels \
		-r requirements.txt \
		-r requirements-devel.txt

FROM python:3.8.0-alpine

WORKDIR /usr/src/app

COPY --from=builder /build/wheels /wheels

RUN addgroup -S app && adduser -u 1000 -S app -G app && \
	apk add --no-cache libpq zlib libjpeg-turbo curl && \
	pip install --no-cache /wheels/*

COPY . /usr/src/app/
RUN	chown -R app:app /usr/src/app/

USER app
EXPOSE 8000

# The default command is only used for local development
ENTRYPOINT ["/usr/src/app/containers/app/entrypoint.sh"]
CMD ["python3 manage.py runserver 0.0.0.0:8000"]