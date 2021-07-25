FROM python:3.8.5-slim as builder

ENV WORKDIR=/usr/src/itorum_test

WORKDIR ${WORKDIR}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir ${WORKDIR}/wheels -r requirements.txt

FROM python:3.8.5-slim

ENV USER itorum
ENV GROUP developer
ENV HOME=/home/itorum
ENV PROJECTPATH=/home/itorum/itorum_test
ENV BUILDERWORKDIR=/usr/src/itorum_test

RUN useradd -m -d /home/${USER} ${USER}

RUN groupadd ${GROUP} \
    && usermod -aG ${GROUP} ${USER}

RUN mkdir ${PROJECTPATH}

WORKDIR ${PROJECTPATH}

RUN apt-get -yqq update && apt-get install -yqq --no-install-recommends \
    libpq-dev nano \
    && apt-get purge -yqq --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder ${BUILDERWORKDIR}/wheels /wheels
COPY --from=builder ${BUILDERWORKDIR}/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . ${PROJECTPATH}

RUN chgrp developer -R ${PROJECTPATH} \
    && chmod -R 775 ${PROJECTPATH}

USER ${USER}
