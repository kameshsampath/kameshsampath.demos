FROM gitpod/workspace-full

ENV POETRY_VERSION 1.1.6
ENV PATH "${HOME}/.poetry/bin:${PATH}"

# TODO install podman and do in container builds
RUN sudo apt-get -y update \
    && mkdir -p ~/.local/share/fonts \
    && mkdir -p ~/.local/share/fonts \
    && cd ~/.local/share/fonts \
    && curl -sSfLo "Fira Mono Regular Nerd Font Complete Mono" https://github.com/ryanoasis/nerd-fonts/blob/master/patched-fonts/FiraMono/Regular/complete/Fira%20Mono%20Regular%20Nerd%20Font%20Complete%20Mono.otf \
    && curl -sSfLo "JetBrains Mono Regular Nerd Font Complete Mono" https://github.com/ryanoasis/nerd-fonts/blob/master/patched-fonts/JetBrainsMono/Ligatures/Regular/complete/JetBrains%20Mono%20Regular%20Nerd%20Font%20Complete%20Mono.ttf \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - \
    && $HOME/.poetry/bin/poetry config virtualenvs.create "true" \
    && $HOME/.poetry/bin/poetry config virtualenvs.in-project "true"