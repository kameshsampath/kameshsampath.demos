FROM gitpod/workspace-full

ENV POETRY_VERSION 1.1.6

# TODO install podman and do in container builds
RUN sudo apt-get -y update \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && mkdir -p ~/.local/share/fonts \
    && mkdir -p ~/.local/share/fonts \
    && cd ~/.local/share/fonts \
    && curl -fLo "Fira Mono Regular Nerd Font Complete Mono" https://github.com/ryanoasis/nerd-fonts/blob/master/patched-fonts/FiraMono/Regular/complete/Fira%20Mono%20Regular%20Nerd%20Font%20Complete%20Mono.otf \
    && curl -fLo "JetBrains Mono Regular Nerd Font Complete Mono" https://github.com/ryanoasis/nerd-fonts/blob/master/patched-fonts/JetBrainsMono/Ligatures/Regular/complete/JetBrains%20Mono%20Regular%20Nerd%20Font%20Complete%20Mono.ttf \
    && bash "$HOME"/.poetry/env \
    && ${HOME}/.poetry/bin/poetry config virtualenvs.create "true" \
    && ${HOME}/.poetry/bin/poetry config virtualenvs.in-project "true"

RUN echo "export PATH=\"\${HOME}/.poetry/bin\":\$PATH" >> /home/gitpod/.bashrc
