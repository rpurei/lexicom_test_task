FROM python:3.10
ENV POETRY_VERSION=1.5.0
ENV POETRY_VENV=/opt/poetry
ENV POETRY_CACHE_DIR=$POETRY_VENV/.cache
ENV PIP_ROOT_USER_ACTION=ignore

RUN rm /bin/sh && ln -s /bin/bash /bin/sh && python3 -m venv $POETRY_VENV && $POETRY_VENV/bin/python3 -m pip install --upgrade pip && $POETRY_VENV/bin/pip install wheel setuptools pip poetry==${POETRY_VERSION}

COPY ./app /opt/lexicom/app
WORKDIR /opt/lexicom/app
RUN $POETRY_VENV/bin/poetry config virtualenvs.create false && $POETRY_VENV/bin/poetry install --no-interaction --no-ansi
ENTRYPOINT ["/opt/lexicom/app/server_run.sh"]
