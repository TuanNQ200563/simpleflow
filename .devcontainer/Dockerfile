FROM python:3.11-slim AS python-base

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.1 \
    POETRY_HOME="/opt/poetry" \
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt" \
    VENV_PATH="/opt/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Base image for installing poetry
FROM python-base AS poetry-base

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    git

RUN curl -sSL https://install.python-poetry.org | python

# `builder-base` stage is used to build deps + create our virtual environment
FROM poetry-base AS builder-base

RUN apt-get update && \
    apt-get install --no-install-recommends -y  \
    # deps for building python deps
    build-essential \
    libpq-dev \
    pkg-config \
    git

# Copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH

COPY ./poetry.lock ./pyproject.toml ./README.md ./

RUN poetry install --only main

# `development` image is used during development / testing
FROM python-base as development

COPY --from=poetry-base $POETRY_HOME $POETRY_HOME

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev build-essential git bash curl tar sudo default-jre nodejs npm && \
    useradd -m -d /home/app -s /bin/bash app && \
    echo '%app ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers && \
    curl -sS https://starship.rs/install.sh | sh -s -- --yes && \
    echo 'eval "$(starship init bash)"' >>/home/app/.bashrc && \
    rm -rf /var/lib/apt/lists/*

USER app

WORKDIR /workspace

COPY . .
FROM python:3.11-slim AS python-base

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.1 \
    POETRY_HOME="/opt/poetry" \
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt" \
    VENV_PATH="/opt/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Base image for installing poetry
FROM python-base AS poetry-base

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    git

RUN curl -sSL https://install.python-poetry.org | python

# `builder-base` stage is used to build deps + create our virtual environment
FROM poetry-base AS builder-base

RUN apt-get update && \
    apt-get install --no-install-recommends -y  \
    # deps for building python deps
    build-essential \
    libpq-dev \
    pkg-config \
    git

# Copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH

COPY ./poetry.lock ./pyproject.toml ./README.md ./

RUN poetry install --only main

# `development` image is used during development / testing
FROM python-base as development

COPY --from=poetry-base $POETRY_HOME $POETRY_HOME

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev build-essential git bash curl tar sudo default-jre nodejs npm && \
    useradd -m -d /home/app -s /bin/bash app && \
    echo '%app ALL=(ALL) NOPASSWD:ALL' >>/etc/sudoers && \
    curl -sS https://starship.rs/install.sh | sh -s -- --yes && \
    echo 'eval "$(starship init bash)"' >>/home/app/.bashrc && \
    rm -rf /var/lib/apt/lists/*

USER app

WORKDIR /workspace

COPY . .
