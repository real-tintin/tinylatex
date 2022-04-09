FROM debian:bullseye

# Setup env
ARG IMAGE_ROOT
ARG CONFIG_FROM

ENV CONFIG_TO "${IMAGE_ROOT}/config.json"
ENV FONT_ROOT "/root/.fonts"

WORKDIR ${IMAGE_ROOT}

RUN mkdir ${FONT_ROOT}

RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    ghostscript \
    wget \
    fontconfig

# Install & setup tinytex (https://yihui.org/tinytex/)
RUN wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
ENV PATH="${PATH}:/root/bin"
RUN tlmgr update --self

# Setup python tool
COPY ./src ${IMAGE_ROOT}
RUN pip install -r requirements.txt

# Setup env from config
COPY ${CONFIG_FROM} ${CONFIG_TO}
RUN python3 cli.py config ${CONFIG_TO}

# Re-build the font cache
RUN fc-cache --force
