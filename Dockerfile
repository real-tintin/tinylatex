FROM minidocks/texlive

ARG IMAGE_ROOT
ARG CONFIG_FROM

ENV CONFIG_TO "${IMAGE_ROOT}/config.json"
ENV FONT_ROOT "/root/.fonts"

WORKDIR ${IMAGE_ROOT}

RUN apk update
RUN apk add --no-cache \
    python3 \
    py3-pip \
    msttcorefonts-installer \
    fontconfig

RUN tlmgr update --self

RUN mkdir ${FONT_ROOT}

COPY ./src ${IMAGE_ROOT}
RUN pip install -r requirements.txt

COPY ${CONFIG_FROM} ${CONFIG_TO}
RUN python3 cli.py config ${CONFIG_TO}

RUN fc-cache --force
