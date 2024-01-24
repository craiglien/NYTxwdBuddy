FROM node:21-bullseye

RUN npm install -g npm@10.3.0

RUN npm install -g @marp-team/marp-cli

EXPOSE 8080

RUN marp --version

CMD ["marp", "--server", "--host", "0.0.0.0", "/slides"]
